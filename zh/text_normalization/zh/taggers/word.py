import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst,NEMO_NOT_SPACE
from pynini.lib import pynutil
class WordFst(GraphFst):
    '''
        每个汉字
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="classify", deterministic=deterministic)
        word = pynutil.insert("word: \"") + pynini.difference(NEMO_NOT_SPACE,"/") + pynutil.insert("\"")
        word = self.add_tokens(word)
        self.fst = word.optimize()