import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
class ErhuaFst(GraphFst):
    '''
        女儿  -  女儿
        这儿  - 这
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="erhua", kind="classify", deterministic=deterministic)
        whitelist = load_labels(get_abs_path("data/erhua/erhua.tsv"))
        erhua_graph = "男儿"
        for word in whitelist:
            erhua_graph|=pynini.accep(word[0])
        erhua_white = pynutil.insert("erhua: \"") + erhua_graph + pynutil.insert("\"")
        erhua_white = self.add_tokens(erhua_white)
        self.fst = erhua_white.optimize()