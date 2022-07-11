import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, NEMO_NOT_QUOTE ,GraphFst, insert_space,NEMO_DIGIT,NEMO_SPACE,NEMO_NOT_SPACE
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class DateFst(GraphFst):
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="date", kind="verbalize", deterministic=deterministic)
        date = pynutil.delete('year: \"二零一二 年') 
        final_graph = date
      #  delete_tokens = self.delete_tokens(final_graph)
        self.fst = final_graph.optimize()
