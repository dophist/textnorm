import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst,insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class FractionFst(GraphFst):
    '''
        1/5 五分之一       
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="fraction", kind="verbalize", deterministic=deterministic)

        
        denominator = pynutil.delete("denominator: \"") + NumberFst().final_graph + pynutil.delete("\"")
        numerator = pynutil.delete("numerator: \"") + NumberFst().final_graph + pynutil.delete("\"") 
        # frac_graph = pynutil.delete("denominator: \"") + pynini.closure(NEMO_NOT_QUOTE,1) + pynutil.delete("\"") + \
        #                 " " + pynutil.delete("numerator: \"") + pynini.closure(NEMO_NOT_QUOTE,1) + pynutil.delete("\"")
        frac_graph = denominator + pynutil.delete(" ") + pynutil.insert("分之") + numerator
        frac_graph = self.delete_tokens(frac_graph)
        self.fst = frac_graph.optimize()