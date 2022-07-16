import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class TimeFst(GraphFst):
    '''
        time { hour: "1" min: "02" sec: "36" }  ->  一点零二分三十六秒
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="time", kind="verbalize", deterministic=deterministic)  
        # TODO: use UNIT_1e1 in utils
        NEMO_TEN = '十' 

        # TODO: refer to time tagger, we should have better implementation for time verbalizer
        graph_digit = pynini.string_file(get_abs_path("data/number/digit.tsv"))
        graph_ten = pynini.string_file(get_abs_path("data/number/digit_teen.tsv"))
        graph_zero = pynini.string_file(get_abs_path("data/number/zero.tsv"))
        graph_no_zero = pynini.cross("0","")

        graph_digit_no_zero = graph_digit|graph_no_zero
        graph_2_digit_time = (
             (graph_ten + pynutil.insert(NEMO_TEN) + graph_digit_no_zero)|
            (graph_zero + graph_digit)
        )
        graph_2_digit_zero_none = pynini.cross("0","") + pynini.cross("0","")
        graph_2_digit_zero = pynini.cross("00","零")

        clock_no_sec = pynutil.delete("hour: \"") + (graph_2_digit_time|graph_2_digit_zero|graph_digit) + \
                        pynutil.insert("点")+ pynutil.delete("\"") + " "\
                        + pynutil.delete("min: \"") + (graph_2_digit_time) + pynutil.insert("分") + pynutil.delete("\"")
        clock_no_min = pynutil.delete("hour: \"") + (graph_2_digit_time|graph_2_digit_zero|graph_digit) +\
                         pynutil.insert("点")+ pynutil.delete("\"") + " "\
                        + pynutil.delete("min: \"") + (graph_2_digit_zero_none) + pynutil.delete("\"")
        clock_with_sec = pynutil.delete("hour: \"") + (graph_2_digit_time|graph_2_digit_zero|graph_digit) + \
                        pynutil.insert("点")+ pynutil.delete("\"") + " "\
                        + pynutil.delete("min: \"") + (graph_2_digit_time|graph_2_digit_zero)  + pynutil.insert("分")+\
                        pynutil.delete("\"") + " " + pynutil.delete("sec: \"") + \
                        (graph_2_digit_time) + pynutil.insert("秒") + pynutil.delete("\"")
        clock_graph = clock_no_sec|clock_with_sec|clock_no_min

        graph_time = clock_graph
        graph_time = self.delete_tokens(graph_time)
        self.fst = graph_time.optimize()