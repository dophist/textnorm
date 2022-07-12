import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, NEMO_NOT_QUOTE ,GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class SignFst(GraphFst):
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="sign", kind="verbalize", deterministic=deterministic)
        date = pynutil.delete('sign: \"') + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete(' \"') 
        final_graph = date
        delete_tokens = self.delete_tokens(final_graph)
        self.fst = delete_tokens.optimize()