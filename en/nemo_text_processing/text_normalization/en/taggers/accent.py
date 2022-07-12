import pynini
from nemo_text_processing.text_normalization.en.graph_utils import NEMO_NOT_QUOTE, GraphFst, NEMO_ALPHA, NEMO_SPACE, NEMO_SIGMA,NEMO_NOT_SPACE
from nemo_text_processing.text_normalization.en.utils import get_abs_path
from pynini.lib import pynutil


class AccentFst(GraphFst):
    """
    Finite state transducer for classifying accents, e.g. 
        "'ve" -> accent { word: "have'" } }

    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
        reverse: if True will regenerate accents in the lines
            for False will remove accents in the lines
    """

    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="accent", kind="classify", deterministic=deterministic)
        subs_graph = pynini.string_file(get_abs_path("data/accent/subs.tsv"))
        past_graph = pynini.string_file(get_abs_path("data/accent/past.tsv"))|(pynini.closure(NEMO_ALPHA)+'ed')
        item_graph = pynini.string_file(get_abs_path("data/accent/items.tsv"))
        n_word = pynini.closure(NEMO_ALPHA)
        s_word = pynini.accep('\'s')
        d_word = pynini.accep('\'d')
        other_graph = (
            pynini.difference(n_word, past_graph)
        )
        common_graph = (
            pynutil.insert("word: \"") + n_word + subs_graph + pynutil.insert("\"")
        )
        has_graph = (
            pynutil.insert("word: \"") + n_word + pynutil.insert(NEMO_SPACE) + 
            pynini.cross(s_word, 'has') + NEMO_SPACE + past_graph + pynutil.insert("\"")
        )
        is_graph = (
            pynutil.insert("word: \"") + item_graph + pynutil.insert(NEMO_SPACE) +  
            pynini.cross(s_word, 'is') + NEMO_SPACE + other_graph + pynutil.insert("\"")
        )
        had_graph = (
            pynutil.insert("word: \"") + n_word + pynutil.insert(NEMO_SPACE) + 
            pynini.cross(d_word, 'had') + NEMO_SPACE + past_graph + pynutil.insert("\"")
        )
        would_graph = (
            pynutil.insert("word: \"") + n_word + pynutil.insert(NEMO_SPACE) + 
            pynini.cross(d_word, 'would') + NEMO_SPACE + other_graph + pynutil.insert("\"")
        )
        graph = pynini.union(
            common_graph,
            has_graph,
            is_graph,
            had_graph,
            would_graph,
        ).optimize()
        graph = self.add_tokens(graph)
        self.fst = graph.optimize()
        # todo:the next word needs to be normalized