import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
class WordFst(GraphFst):
    '''
        每个汉字
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="verbalize", deterministic=deterministic)
        word = pynutil.delete("word: \"") + NEMO_NOT_SPACE + pynutil.delete("\"")
        er = pynutil.delete("er_word: \"") + pynutil.delete("儿") + pynutil.delete("\"")
        word|=er
        word = self.delete_tokens(word)
        self.fst = word.optimize()