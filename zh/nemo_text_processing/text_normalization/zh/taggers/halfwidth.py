import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class HalfwidthFst(GraphFst):
    '''
        ：  -> halfwidth { halfwidth: "：" }  used unless you want to process only once
        ：  ->  :   in common case
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="halfwidth", kind="classify", deterministic=deterministic)

        fullwidth_to_halfwidth = pynini.string_file(get_abs_path("data/char/fullwidth_to_halfwidth.tsv"))
        self.graph_halfwidth = fullwidth_to_halfwidth 
        graph = (
            pynutil.insert("halfwidth: \"") 
            + fullwidth_to_halfwidth 
            + pynutil.insert("\"")
        )

        self.fst = self.add_tokens(graph).optimize()
        