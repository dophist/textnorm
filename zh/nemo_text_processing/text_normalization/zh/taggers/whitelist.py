import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class WhitelistFst(GraphFst):
    '''
        common use writing forms
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="whitelist", kind="classify", deterministic=deterministic)
        whitelist = pynini.string_file(get_abs_path("data/whitelist/whitelist.tsv"))
        white = pynutil.insert("whitelist: \"") + whitelist + pynutil.insert("\"")
        white = self.add_tokens(white)
        self.fst = white.optimize()