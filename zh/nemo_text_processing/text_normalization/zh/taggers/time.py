import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst,insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class TimeFst(GraphFst):
    '''
        1:02          -> time { hour: "1" min: "02" }
        1:02:36       -> time { hour: "1" min: "02" sec: "36" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="time", kind="classify", deterministic=deterministic)
        # TODO: how do we ensure fullwidth version of : is properly handled or converted beforehand ?
        # TODO: we can have tighter constrains, e.g.:
        #     h in [0,24), m & s in [00, 60), you can use python's range() or a .tsv file as helper
        #     then we can have time patterns like h:m, h:m:s etc
        h = pynini.closure(NEMO_DIGIT, 1)
        m = pynini.closure(NEMO_DIGIT, 2, 2)
        s = pynini.closure(NEMO_DIGIT, 1, 2)

        h_m = \
            pynutil.insert('hour: "') + h + pynutil.insert('"') + \
            pynini.cross(':', ' ') + \
            pynutil.insert('min: "') + m + pynutil.insert('"')

        h_m_s = \
            pynutil.insert('hour: "') + h + pynutil.insert('"') + \
            pynini.cross(':', ' ') + \
            pynutil.insert('min: "') + m + pynutil.insert('"') + \
            pynini.cross(':', ' ') + \
            pynutil.insert('sec: "') + s + pynutil.insert('"')

        patterns = h_m | h_m_s
        self.fst = self.add_tokens(patterns).optimize()
