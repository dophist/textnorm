import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst,NEMO_NOT_QUOTE
from pynini.lib import pynutil
class MoneyFst(GraphFst):
    '''
        money { num: "一点五" cur: "元" }  ->  一点五元
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="money", kind="verbalize", deterministic=deterministic)   
        cur = pynutil.delete("cur: \"") + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete("\"")
        number = pynutil.delete("num: \"") + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete("\"") + " "
        money_graph = number + cur
        money_graph = self.delete_tokens(money_graph)
        self.fst = money_graph.optimize()