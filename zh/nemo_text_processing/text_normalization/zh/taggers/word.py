import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_DIGIT,NEMO_ALPHA,NEMO_PUNCT
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
class WordFst(GraphFst):
    # TODO: we should rename "Word" related stuff to Token, because we are using chars as tokens, word is for english.
    '''
        你  ->   word { word: "你" }
        这儿 ->  word { er_word: "儿" }
        の  ->   word { other: "の" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="classify", deterministic=deterministic)
        er = pynutil.insert("er_word: \"") + "儿" + pynutil.insert("\"")
        charset_std = pynini.string_file(get_abs_path("data/char/charset_national_standard_2013_8105.tsv"))
        charset_ext = pynini.string_file(get_abs_path("data/char/charset_extension.tsv"))

        charset_graph = pynini.union(charset_std , charset_ext)

        removal_word = pynini.string_file(get_abs_path("data/char/removal.tsv"))
        word_removal = pynutil.delete(removal_word)
        # TODO: 呃，啊 are still hard-coded in python code, clean these up
        word = pynutil.insert("word: \"") + pynini.difference((charset_graph|NEMO_DIGIT|NEMO_ALPHA|NEMO_PUNCT),(pynini.accep("儿")|pynini.accep("呃")|pynini.accep("啊"))) + pynutil.insert("\"")
        word_other = pynutil.insert("other: \"") + pynini.difference(NEMO_CHAR,(charset_graph|NEMO_DIGIT|NEMO_ALPHA|NEMO_PUNCT|pynini.accep("儿")|pynini.accep("呃")|pynini.accep("啊")|pynini.accep(" "))) + pynutil.insert("\"")
        word|=er
        word|= word_other
        word = self.add_tokens(word)
        self.word_removal = word_removal
        self.fst = word.optimize()