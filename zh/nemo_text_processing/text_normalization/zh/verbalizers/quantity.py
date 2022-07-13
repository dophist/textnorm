import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class QuantityFst(GraphFst):
    '''
        1.25km
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="quantity", kind="verbalize", deterministic=deterministic)   
        final_graph = pynutil.delete("quantity: \"") + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete("\"")
        final_graph = self.delete_tokens(final_graph)
        self.fst = final_graph.optimize()