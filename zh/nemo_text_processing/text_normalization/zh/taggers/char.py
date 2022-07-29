import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_DIGIT,NEMO_ALPHA,NEMO_PUNCT
from pynini.lib import pynutil, utf8
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels

class CharFst(GraphFst):
    '''
        你们好 -> char { char: "你" } char { char: "们" } char { char: "好" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="char", kind="classify", deterministic=deterministic)

        graph = pynutil.insert("char: \"") + NEMO_CHAR + pynutil.insert("\"")

        self.fst = self.add_tokens(graph).optimize()
