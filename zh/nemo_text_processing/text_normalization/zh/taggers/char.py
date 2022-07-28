import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_DIGIT,NEMO_ALPHA,NEMO_PUNCT
from pynini.lib import pynutil, utf8
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
class CharFst(GraphFst):
    '''
        你  ->   char { char: "你" }
        这儿 ->  char { erhua: "儿" }
        の  ->   char { oov: "の" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="char", kind="classify", deterministic=deterministic)

        char_erhua  = pynutil.insert("erhua: \"") + '儿' + pynutil.insert("\"")
        char_normal = pynutil.insert("char: \"") + pynini.difference(NEMO_CHAR, '儿') + pynutil.insert("\"")

        graph = (
            pynutil.add_weight(char_erhua,  0.01) |
            pynutil.add_weight(char_normal, 0.02)
        )

        self.fst = self.add_tokens(graph).optimize()
