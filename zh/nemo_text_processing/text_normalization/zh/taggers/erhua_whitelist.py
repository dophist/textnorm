import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels

class ErhuaWhitelistFst(GraphFst):
    '''
        女儿  ->  erhua { whitelist: "女儿" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="erhua", kind="classify", deterministic=deterministic)

        whitelist = pynini.string_file(get_abs_path("data/erhua/whitelist.tsv"))
        graph = (
            pynutil.insert("whitelist: \"") 
            + whitelist 
            + pynutil.insert("\"")
        )

        self.fst = self.add_tokens(graph).optimize()
