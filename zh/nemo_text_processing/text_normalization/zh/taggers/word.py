import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_DIGIT,NEMO_ALPHA,NEMO_PUNCT
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
class WordFst(GraphFst):
    '''
        每个不需要正则的汉字
        every normal character
        now we only need to delete "儿/呃/啊",if more character should be delete,try another new graph
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="classify", deterministic=deterministic)
        er = pynutil.insert("er_word: \"") + "儿" + pynutil.insert("\"")
        standard_charset = load_labels(get_abs_path("data/char/national_standard_2013_mandarin_charset_8105.tsv"))
        standard_charset_ext = load_labels(get_abs_path("data/char/charset_extension.tsv"))
        standard_charset_graph = "一" # TODO: ???
        for word in standard_charset:
            standard_charset_graph|=pynini.accep(word[0])

        # TODO: load from data/charset/removal.tsv
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