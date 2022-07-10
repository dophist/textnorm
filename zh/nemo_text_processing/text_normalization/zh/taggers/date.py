import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space,NEMO_DIGIT
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class DataFst(GraphFst):
    '''
        ￥1.25 --> 一点二五元
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="data", kind="classify", deterministic=deterministic)
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        zero_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/zero.tsv")))
        self.fst = (zero_graph|digit_graph)|(digit_graph|zero_graph) + "年"
