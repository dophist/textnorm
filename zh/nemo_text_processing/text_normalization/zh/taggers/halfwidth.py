import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class HalfwidthFst(GraphFst):
    '''
        ：  -> halfwidth { halfwidth: "：" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="halfwidth", kind="classify", deterministic=deterministic)
        halfwidth = pynini.string_file(get_abs_path("data/halfwidth/halfwidth.tsv"))
        graph_halfwidth = pynutil.insert("halfwidth: \"") + halfwidth + pynutil.insert("\"")
        graph_halfwidth = self.add_tokens(graph_halfwidth)
        self.fst = graph_halfwidth.optimize()