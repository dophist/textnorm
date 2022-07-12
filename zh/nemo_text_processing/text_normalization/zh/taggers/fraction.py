import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst,insert_space,NEMO_DIGIT
# from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class FractionFst(GraphFst):
    '''
        1/5 五分之一       
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="fraction", kind="classify", deterministic=deterministic)
        numerator = pynini.closure(NEMO_DIGIT,1) + pynutil.delete('/')
        denominator = pynini.closure(NEMO_DIGIT,1)
        # preserve_order = pynutil.insert(" preserve_order: true")
        frac_graph = pynutil.insert("numerator: \"") + numerator + pynutil.insert("\"") \
        + insert_space + pynutil.insert("denominator: \"") + denominator + pynutil.insert("\"") 

        frac_graph = self.add_tokens(frac_graph)
        self.fst = frac_graph.optimize()
