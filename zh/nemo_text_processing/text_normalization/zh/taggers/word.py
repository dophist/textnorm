import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_DIGIT,NEMO_ALPHA,NEMO_PUNCT
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
class WordFst(GraphFst):
    '''
        TODO: refine docstring, input & output exmples
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="classify", deterministic=deterministic)
        er = pynutil.insert("er_word: \"") + "儿" + pynutil.insert("\"")
        standard_charset = load_labels(get_abs_path("data/char/charset_national_standard_2013_8105.tsv"))
        standard_charset_ext = load_labels(get_abs_path("data/char/charset_extension.tsv")) #TODO: incorporate these extension chars into graph
        standard_charset_graph = "一" # TODO: use pynini.union() to avoid this 
        for word in standard_charset:
            standard_charset_graph|=pynini.accep(word[0])

        # TODO: load these from data/char/removal.tsv
        word_e = pynutil.insert("e_word: \"") + "呃" + pynutil.insert("\"")
        word_a = pynutil.insert("a_word: \"") + "啊" + pynutil.insert("\"")
        word = pynutil.insert("word: \"") + pynini.difference((standard_charset_graph|NEMO_DIGIT|NEMO_ALPHA|NEMO_PUNCT),(pynini.accep("儿")|pynini.accep("呃")|pynini.accep("啊"))) + pynutil.insert("\"")
        word_other = pynutil.insert("other: \"") + pynini.difference(NEMO_CHAR,(standard_charset_graph|NEMO_DIGIT|NEMO_ALPHA|NEMO_PUNCT|pynini.accep("儿")|pynini.accep("呃")|pynini.accep("啊"))) + pynutil.insert("\"")
        word|=er
        word|=word_e
        word|=word_a
        word|= word_other
        word = self.add_tokens(word)
        self.fst = word.optimize()