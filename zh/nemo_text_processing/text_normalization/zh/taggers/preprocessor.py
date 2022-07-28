import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst, NEMO_SIGMA
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.zh.utils import get_abs_path

class PreProcessorFst(GraphFst):
    '''
        Preprocessing of TN, now contains:
            1. interjections removal such as '啊, 呃'
            2. fullwidth -> halfwidth char conversion
    '''
    def __init__(self):
        super().__init__(name="PreProcessor", kind="processor")  

        remove_interjections = pynutil.delete(
            pynini.string_file(get_abs_path('data/blacklist/interjections.tsv'))
        )
        fullwidth_to_halfwidth = pynini.string_file(get_abs_path('data/char/fullwidth_to_halfwidth.tsv'))

        graph = remove_interjections | fullwidth_to_halfwidth 

        self.fst = pynini.cdrewrite(graph, "", "", NEMO_SIGMA).optimize()

