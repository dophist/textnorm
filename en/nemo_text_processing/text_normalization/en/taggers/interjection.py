import pynini
from nemo_text_processing.text_normalization.en.graph_utils import NEMO_NOT_QUOTE, GraphFst
from nemo_text_processing.text_normalization.en.utils import get_abs_path
from pynini.lib import pynutil


class InterjectionFst(GraphFst):
    """
    Finite state transducer for classifying interjections, e.g. 
        umm -> interjection { inter: "umm" } }

    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True, lm: bool = False, reverse = False):
        super().__init__(name="interjection", kind="classify", deterministic=deterministic)
        graph = pynini.string_file(get_abs_path("data/interjection/word.tsv"))
        graph = pynutil.insert("inter: \"") + graph + pynutil.insert("\"")
        graph = self.add_tokens(graph)
        self.fst = graph.optimize()
