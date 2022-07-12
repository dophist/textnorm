import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space,NEMO_DIGIT
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class DateFst(GraphFst):
    '''
        ￥1.25 --> 一点二五元
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="date", kind="classify", deterministic=deterministic)
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        zero_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/zero.tsv")))
        year_graph = pynini.closure(digit_graph|zero_graph,4,4)+ " 年"
        date_graph = pynutil.insert("year: \"") + year_graph + pynutil.insert(" \"")
        date_graph = self.add_tokens(date_graph)
        self.fst = date_graph.optimize()
