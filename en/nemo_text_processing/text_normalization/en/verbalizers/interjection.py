import pynini
from nemo_text_processing.text_normalization.en.graph_utils import NEMO_NOT_QUOTE, GraphFst
from pynini.lib import pynutil


class InterjectionFst(GraphFst):
    """
    Finite state transducer for verbalizing interjections, e.g. 
        umm <- interjection { inter: "umm" } }

    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="interjection", kind="verbalize", deterministic=deterministic)
        graph = pynutil.delete("inter: \"") + pynutil.delete(pynini.closure(NEMO_NOT_QUOTE, 1)) + pynutil.delete("\"")
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
