import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class SignFst(GraphFst):
    '''
        +、～
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="sign", kind="classify", deterministic=deterministic)
        sign_graph = pynini.string_file(get_abs_path("data/sign/sign.tsv"))
        sign_graph = pynutil.insert("sign: \"") + sign_graph + pynutil.insert(" \"")
        sign_graph = self.add_tokens(sign_graph)
        self.fst = sign_graph.optimize()