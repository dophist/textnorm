import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class Qj2bjFst(GraphFst):
    '''
        全角 - 半角转换
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="qj", kind="classify", deterministic=deterministic)
        qj2bj = pynini.string_file(get_abs_path("data/qj2bj/qj2bj.tsv"))
        qj = pynutil.insert("qj: \"") + qj2bj + pynutil.insert("\"")
        qj = self.add_tokens(qj)
        self.fst = qj.optimize()