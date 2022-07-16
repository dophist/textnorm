import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class NumberFst(GraphFst):
    '''
        5       -> number { number: "五"}
        12      -> number { number: "十二"}
        213     -> number { number: "二百一十三"}
        3123    -> number { number: "三千一百二十三"}
        3,123   -> number { number: "三千一百二十三"}
        51234   -> number { number: "五万一千二百三十四"}
        51,234  -> number { number: "五万一千二百三十四"}
        0.125   -> number { number: "零点一二五"}

    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="number", kind="classify", deterministic=deterministic)

        UNIT_1e01 = '十'
        UNIT_1e02 = '百'
        UNIT_1e03 = '千'
        UNIT_1e04 = '万'
        UNIT_1e08 = '亿'
        UNIT_1e12 = '兆'

        graph_digit = pynini.string_file(get_abs_path("data/number/digit.tsv"))
        graph_zero = pynini.string_file(get_abs_path("data/number/zero.tsv"))
        graph_teen = pynini.string_file(get_abs_path("data/number/digit_teen.tsv"))
        graph_digit_with_zero = graph_digit|graph_zero
        graph_no_zero = pynini.cross("0","")
        graph_digit_no_zero = graph_digit|graph_no_zero
        insert_zero = pynutil.insert('零')
        delete_punct = (pynutil.delete(",")|pynutil.delete("，"))
 
        graph_ten_u = (
            (graph_digit + pynutil.insert(UNIT_1e01) + graph_digit_no_zero)|
            (graph_zero + graph_digit)
        )
        graph_ten = (
            (graph_teen + pynutil.insert(UNIT_1e01) + graph_digit_no_zero)|
            (graph_zero + graph_digit)
        )
        graph_hundred = (
            (graph_digit + pynutil.insert(UNIT_1e02) + graph_ten_u)|
            (graph_digit + pynutil.insert(UNIT_1e02) + graph_no_zero**2)
        )
        graph_thousand = (
            ((graph_digit + pynutil.insert(UNIT_1e03) + graph_hundred)|
            (graph_digit + pynutil.insert(UNIT_1e03) + graph_zero + graph_digit + \
            pynutil.insert(UNIT_1e01) + graph_digit_no_zero)|
            (graph_digit + pynutil.insert(UNIT_1e03) + graph_zero + graph_no_zero + graph_digit)|
            (graph_digit + pynutil.insert(UNIT_1e03) + graph_no_zero**3)) 
        )
        graph_thousand_sign =(
            ((graph_digit + pynutil.insert(UNIT_1e03) + delete_punct + \
            graph_hundred)|(graph_digit + pynutil.insert(UNIT_1e03) + \
            delete_punct + graph_zero + graph_digit + \
            pynutil.insert(UNIT_1e01) + graph_digit_no_zero)|(graph_digit + pynutil.insert(UNIT_1e03) +\
            delete_punct + graph_zero + graph_no_zero + graph_digit)| \
            (graph_digit + pynutil.insert(UNIT_1e03) + delete_punct + \
            graph_no_zero**3)) 
        )
        graph_ten_thousand = (
            (graph_thousand|graph_hundred|graph_ten|graph_digit_no_zero) + \
            pynutil.insert(UNIT_1e04) + (graph_thousand|(graph_no_zero + \
            insert_zero + graph_hundred)|(graph_no_zero**2 + \
            insert_zero + (graph_digit + pynutil.insert(UNIT_1e01) + graph_digit_no_zero))|
            (graph_no_zero**3 + insert_zero + graph_digit)|(graph_no_zero**4))
        )
        graph_ten_thousand_sign = (
            (graph_thousand|graph_hundred|graph_ten|graph_digit_no_zero) + \
            pynutil.insert(UNIT_1e04) + (graph_thousand_sign|
            (graph_no_zero + delete_punct + insert_zero + \
            graph_hundred)|(graph_no_zero + delete_punct + graph_no_zero + \
            insert_zero + (graph_digit + pynutil.insert(UNIT_1e01) + graph_digit_no_zero))|
            (graph_no_zero + delete_punct + graph_no_zero**2 + insert_zero + graph_digit)|(graph_no_zero**4))
        )
        graph_numstring = (
            pynini.closure(graph_digit_with_zero,1)
            |(pynini.closure(graph_digit_with_zero,1) + pynini.cross(".","点") + pynini.closure(graph_digit_with_zero,1))
        )
        
        graph = graph_hundred | graph_thousand | graph_ten | graph_digit_with_zero | graph_ten_thousand
        graph |=graph_thousand_sign
        graph |= graph_ten_thousand_sign

        graph_decimal = (
            graph + pynini.cross('.','点') + pynini.closure(graph_digit_with_zero,1) 
        )
        graph_number = graph | graph_decimal
        self.graph_number = graph_number.optimize()
        graph_numstring = pynutil.insert("number: \"") + graph_numstring + pynutil.insert("\"")

        graph_numstring = self.add_tokens(graph_numstring)
        self.fst = graph_numstring.optimize()
        
        
        




