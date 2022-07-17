import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class MeasureFst(GraphFst):
    '''
        1kg  -> measure { measure: "1kg" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="measure", kind="classify", deterministic=deterministic)
        measure = pynini.string_file(get_abs_path("data/measure/measure.tsv"))
        # TODO: measure_zh: 
        #     1. data/measure/measure_zh.tsv should be a list, not a two-column mapping
        #     2. misses entries such as 千米，毫米，compared with the cn_tn.py source code
        measure_zh = pynini.string_file(get_abs_path("data/measure/measure_zh.tsv"))
        graph_measure = pynutil.insert("measure: \"") + NumberFst().graph_number + (measure|measure_zh) + pynutil.insert("\"")
        graph_measure = self.add_tokens(graph_measure)
        self.fst = graph_measure.optimize()