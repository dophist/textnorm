import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst, insert_space,NEMO_DIGIT
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class DateFst(GraphFst):
    '''
        2002年 ->二零零二年
        2002-01-28  2002年1月28日
        2002/01/28
        2002/01
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="date", kind="classify", deterministic=deterministic)
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        zero_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/zero.tsv")))
        year_graph = pynini.closure(digit_graph|zero_graph,2,4)+ "年" + pynini.difference(NEMO_CHAR,(pynini.accep("后")|pynini.accep("前")))
        date_graph = pynutil.insert("year: \"") + year_graph + pynutil.insert(" \"")

        year = pynini.closure(NEMO_DIGIT,2,4) + (pynutil.delete("/")|pynutil.delete('-')|pynutil.delete('.'))
        year2 = pynini.closure(NEMO_DIGIT,4,4) + pynutil.delete("/")
        year3 = "0" + pynini.closure(NEMO_DIGIT,1,1) + pynutil.delete("/")
        month_no_day = "0" + pynini.closure(NEMO_DIGIT,1,1)
        month_no_day2 = pynini.closure(NEMO_DIGIT,1,2)
        month = pynini.closure(NEMO_DIGIT,1,2) + (pynutil.delete("/")|pynutil.delete('-')|pynutil.delete('.'))
        day = pynini.closure(NEMO_DIGIT,1,2)
        date_type1 = pynutil.insert("year: \"") + year + pynutil.insert(" \"") + insert_space\
                    + pynutil.insert("month: \"") + month + pynutil.insert(" \"") + insert_space\
                    + pynutil.insert("day: \"") + day + pynutil.insert(" \"")

        date_type2 = pynutil.insert("year: \"") + year + pynutil.insert(" \"") + insert_space\
                    + pynutil.insert("month: \"") + month_no_day + pynutil.insert(" \"")
        date_type3 = pynutil.insert("year: \"") + year2 + pynutil.insert(" \"") + insert_space\
                    + pynutil.insert("month: \"") + month_no_day2 + pynutil.insert(" \"")
        date_type4 = pynutil.insert("year: \"") + year3 + pynutil.insert(" \"") + insert_space\
                    + pynutil.insert("month: \"") + month_no_day2 + pynutil.insert(" \"")

        final_graph = date_graph|date_type1|date_type2|date_type3|date_type4
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
