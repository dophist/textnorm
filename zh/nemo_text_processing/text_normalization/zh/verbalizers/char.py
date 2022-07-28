import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_NOT_QUOTE
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path

class CharFst(GraphFst):
    '''
        char { char: "你" }  -> 你
        char { erhua: "儿" } -> ""
        char { oov: "の" }   -> <の>
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="char", kind="verbalize", deterministic=deterministic)

        char = pynutil.delete("char: \"") + NEMO_NOT_SPACE + pynutil.delete("\"")
        erhua = pynutil.delete("erhua: \"") + pynutil.delete("儿") + pynutil.delete("\"")
        graph = char | erhua

        self.fst = self.delete_tokens(graph).optimize()
