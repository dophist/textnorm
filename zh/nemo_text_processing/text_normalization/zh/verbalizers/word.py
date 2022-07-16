import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
class WordFst(GraphFst):
    '''
        TODO: fix example formatting
        每个汉字
        word { word: "你" } - 你
        word { er_word: "儿" } -""
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="verbalize", deterministic=deterministic)
        word = pynutil.delete("word: \"") + NEMO_NOT_SPACE + pynutil.delete("\"")

        # TODO: load these from data/char/removal.tsv
        word_e = pynutil.delete("e_word: \"") + pynutil.delete("呃") + pynutil.delete("\"")
        word_a = pynutil.delete("a_word: \"") + pynutil.delete("啊") + pynutil.delete("\"")
        er = pynutil.delete("er_word: \"") + pynutil.delete("儿") + pynutil.delete("\"")
        word_other = pynutil.delete("other: \"") + pynutil.insert("<") + NEMO_CHAR  + pynutil.insert(">") + pynutil.delete("\"")
        word|=er
        word|=word_a
        word|=word_e
        word|=word_other
        word = self.delete_tokens(word)
        self.fst = word.optimize()