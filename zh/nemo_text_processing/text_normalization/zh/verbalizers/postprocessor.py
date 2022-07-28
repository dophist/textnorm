import pynini
from pynini.lib import pynutil, utf8
from nemo_text_processing.text_normalization.zh.graph_utils import (
    GraphFst, 
    NEMO_CHAR, NEMO_DIGIT, NEMO_ALPHA, NEMO_PUNCT, NEMO_SIGMA
)
from nemo_text_processing.text_normalization.zh.utils import get_abs_path

class PostProcessorFst(GraphFst):
    '''
        Postprocessing of TN, now contains:
            1. punctuation removal
            2. letter case conversion
            3. oov tagger
    '''
    def __init__(self, case: str = 'upper'):
        super().__init__(name="PostProcessor", kind="processor")  

        # remove punctuations
        remove_puncts_graph = pynutil.delete(
            pynini.union(
                NEMO_PUNCT,
                pynini.string_file(get_abs_path('data/char/punctuations_zh.tsv'))
            )
        )
        remove_puncts = pynini.cdrewrite(remove_puncts_graph, "", "", NEMO_SIGMA).optimize()
        graph = remove_puncts

        # unify cases
        if case:
            if case == 'upper':
                conv_cases_graph = pynini.string_file(get_abs_path('data/char/lower_to_upper.tsv'))
            elif case == 'lower':
                conv_cases_graph = pynini.string_file(get_abs_path('data/char/upper_to_lower.tsv'))
            else:
                assert (case == None)
            conv_cases = pynini.cdrewrite(conv_cases_graph, "", "", NEMO_SIGMA).optimize()
            graph = graph @ conv_cases

        # oov tagger
        zh_charset_std = pynini.string_file(get_abs_path("data/char/charset_national_standard_2013_8105.tsv"))
        zh_charset_ext = pynini.string_file(get_abs_path("data/char/charset_extension.tsv"))
        zh_punctuations = pynini.string_file(get_abs_path("data/char/punctuations_zh.tsv")) 

        zh_charset = zh_charset_std | zh_charset_ext | zh_punctuations
        en_charset = NEMO_DIGIT | NEMO_ALPHA | NEMO_PUNCT | ' '

        charset = zh_charset | en_charset
        oov_charset = pynini.difference(utf8.VALID_UTF8_CHAR, charset)

        with open(get_abs_path("data/char/oov_tags.tsv"),"r") as f:
            tags = f.readline().strip().split('\t')
            assert(len(tags) == 2)
            ltag, rtag = tags

        tag_oov_graph = (
            pynutil.insert(ltag) + oov_charset  + pynutil.insert(rtag) 
        ) 
        tag_oov = pynini.cdrewrite(tag_oov_graph, "", "", NEMO_SIGMA).optimize()
        graph = graph @ tag_oov

        self.fst = graph.optimize()
