import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_QUOTE
from pynini.lib import pynutil

class ErhuaFst(GraphFst):
    '''
        char { "char" : "这" } erhua { positive: "儿" } -> 这
        erhua { negative: "儿女" } -> 儿女
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="erhua", kind="verbalize", deterministic=deterministic)

        remove_positive = pynutil.delete("positive: \"") + pynutil.delete("儿") + pynutil.delete("\"")
        retain_negative = pynutil.delete("negative: \"") + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete("\"")
        graph = remove_positive | retain_negative

        self.fst = self.delete_tokens(graph).optimize()
