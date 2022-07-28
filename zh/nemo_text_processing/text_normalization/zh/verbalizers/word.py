import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_CHAR, GraphFst,NEMO_NOT_SPACE,NEMO_NOT_QUOTE
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
class WordFst(GraphFst):
    '''
        word { word: "你" }      -> 你
        word { er_word: "儿" }   -> ""
        word { other: "の" }     -> <の>
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="word", kind="verbalize", deterministic=deterministic)
        word = pynutil.delete("word: \"") + NEMO_NOT_SPACE + pynutil.delete("\"")

        # word_removal = pynutil.delete("removal_word: \"") + pynutil.delete(NEMO_NOT_QUOTE) + pynutil.delete("\"")
        er = pynutil.delete("er_word: \"") + pynutil.delete("儿") + pynutil.delete("\"")

        with open(get_abs_path("data/char/charset_illegal_tags.tsv"),"r") as f:
            tags = f.readline().split('\t')
            assert(len(tags) == 2)
            ltag, rtag = tags

        word_other = pynutil.delete("other: \"") + pynutil.insert(ltag) + NEMO_CHAR  + pynutil.insert(rtag) + pynutil.delete("\"") 
        word|=er
        # word|=word_removal
        word|=word_other
        word = self.delete_tokens(word)
        self.fst = word.optimize()