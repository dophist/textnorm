import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA,GraphFst,NEMO_NOT_SPACE

from pynini.lib import pynutil
class NumberFst(GraphFst):
    '''
        number {number: "123 "}
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="number", kind="verbalize", deterministic=deterministic)
        number = pynutil.delete('number: \"') + pynini.closure(NEMO_NOT_SPACE) + pynutil.delete(' \"') 
        final_graph = number
        delete_tokens = self.delete_tokens(final_graph)
        self.fst = delete_tokens.optimize()