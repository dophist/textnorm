import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels

class ErhuaFst(GraphFst):
    '''
        这儿 -> erhua { positive: "这儿" }
        儿女 -> erhua { negative: "儿女" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="erhua", kind="classify", deterministic=deterministic)

        positive = pynutil.insert("positive: \"") + '儿' + pynutil.insert("\"")
        negative = (
            pynutil.insert("negative: \"") +
            pynini.string_file(get_abs_path("data/erhua/negative.tsv")) +
            pynutil.insert("\"")
        )
        graph = pynutil.add_weight(positive, 0.1) | negative

        self.fst = self.add_tokens(graph).optimize()
