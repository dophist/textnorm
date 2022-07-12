import pynini
from nemo_text_processing.text_normalization.en.graph_utils import NEMO_NOT_QUOTE, GraphFst
from nemo_text_processing.text_normalization.en.utils import get_abs_path
from pynini.lib import pynutil


class SubstituteFst(GraphFst):
    """
    Finite state transducer for classifying words need to be substitute, e.g. 
       colour -> Substitute { word: "color" } }

    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True, lm: bool = False, reverse = False):
        super().__init__(name="substitute", kind="verbalize", deterministic=deterministic)
        graph = pynutil.delete("word: \"") + pynini.closure(NEMO_NOT_QUOTE, 1) + pynutil.delete("\"")
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()


