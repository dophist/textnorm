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
        super().__init__(name="substitute", kind="classify", deterministic=deterministic)
        word_graph = pynini.string_file(
            get_abs_path("data/substitute/word.tsv")
        )
        year_graph = pynini.string_file(
            get_abs_path("data/substitute/numbers.tsv")
        )
        word_past = word_graph + 'ed'
        subs_graph =  word_graph | year_graph | word_past
        graph = pynutil.insert("word: \"") + subs_graph + pynutil.insert("\"")
        graph = self.add_tokens(graph)
        self.fst = graph.optimize()
