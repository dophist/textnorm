import pynini
from nemo_text_processing.text_normalization.en.graph_utils import NEMO_NOT_QUOTE, GraphFst, NEMO_SPACE, NEMO_ALPHA
from nemo_text_processing.text_normalization.en.utils import get_abs_path
from pynini.lib import pynutil


class SymbolFst(GraphFst):
    """
    Finite state transducer for classifying symbols like - + /, e.g. 
       2-3=-1 -> Substitute { equation: "two minus three equals minus one" }
       www.jj-kk.com -> Substitute { website: "www dot jj dash kk dot com" } 
       www.jj-kk.com -> Substitute { website: "www dot jj dash kk dot com" } 

    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True, lm: bool = False, reverse = False):
        super().__init__(name="symbol", kind="classify", deterministic=deterministic)
        # equations
        cal_symbol_graph = (
            pynini.cross('+','plus')|
            pynini.cross('-','minus')|
            pynini.cross('/','divided by')|
            pynini.cross('*','multiply')|
            pynini.cross('=','equals')
        )
        cardinal_graph = pynini.Far(get_abs_path("data/number/cardinal_number_name.far")).get_fst()
        alpha_graph = pynini.closure(NEMO_ALPHA,1)
        item_graph = alpha_graph | cardinal_graph
        cal_symbol_space_graph = pynutil.insert(NEMO_SPACE) + cal_symbol_graph + pynutil.insert(NEMO_SPACE)
        equa_symbol = pynutil.insert(NEMO_SPACE) + pynini.cross('=','equals') + pynutil.insert(NEMO_SPACE)
        equation_graph = (
            (pynini.closure(item_graph + cal_symbol_space_graph,1)| item_graph)
            + equa_symbol
            + (pynini.closure(item_graph + cal_symbol_space_graph,1)| item_graph)
        )
        # remove dash in words
        word = pynini.closure(NEMO_ALPHA,1)
        dash_graph = (
            word
            + pynutil.delete('-')
            + word
        )
        # dash in range
        range_graph = (
            cardinal_graph
            + pynini.closure(NEMO_SPACE,0,1)
            + pynutil.insert(NEMO_SPACE)
            + pynini.cross('-','to')
            + pynini.closure(NEMO_SPACE,0,1)
            + pynutil.insert(NEMO_SPACE)
            + cardinal_graph
        )
        # x by y
        by_graph = (
            cardinal_graph
            + pynutil.insert(NEMO_SPACE)
            + (pynini.cross('x','by')|pynini.cross('×','by'))
            + pynutil.insert(NEMO_SPACE)
            + cardinal_graph
        )
        final_graph = dash_graph | range_graph | equation_graph 
        graph = pynutil.insert("content: \"") + final_graph + pynutil.insert("\"")
        graph = self.add_tokens(graph)
        self.fst = graph.optimize()
