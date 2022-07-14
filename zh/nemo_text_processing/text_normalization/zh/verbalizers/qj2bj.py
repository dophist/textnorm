import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
class Qj2bjFst(GraphFst):
    '''
        qj { qj "＠" } ->  @
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="qj", kind="verbalize", deterministic=deterministic)
        qj = pynutil.delete("qj: \"") + NEMO_NOT_SPACE + pynutil.delete("\"")
        qj = self.delete_tokens(qj)
        self.fst = qj.optimize()