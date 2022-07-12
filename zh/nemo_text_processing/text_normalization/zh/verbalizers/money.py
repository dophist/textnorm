import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class MoneyFst(GraphFst):
    '''
        ￥1.25 --> 一点二五元
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="money", kind="verbalize", deterministic=deterministic)   
        cur = pynutil.delete("cur: \"") + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete("\"")
        number = pynutil.delete("num: \"") + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete("\"") + " "
        final_graph = number + cur
        final_graph = self.delete_tokens(final_graph)
        self.fst = final_graph.optimize()