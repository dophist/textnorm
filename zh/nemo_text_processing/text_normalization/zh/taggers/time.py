import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst,insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class TimeFst(GraphFst):
    '''
        1:02          -> time { h: "1" m: "02" }
        1:02:36       -> time { h: "1" m: "02" s: "36" }
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

        # 5:05, 14:30
        h_m = \
            pynutil.insert('h: "') + h + pynutil.insert('"') + \
            pynini.cross(':', ' ') + \
            pynutil.insert('m: "') + m + pynutil.insert('"')

        # 1:30:15
        h_m_s = \
            pynutil.insert('h: "') + h + pynutil.insert('"') + \
            pynini.cross(':', ' ') + \
            pynutil.insert('m: "') + m + pynutil.insert('"') + \
            pynini.cross(':', ' ') + \
            pynutil.insert('s: "') + s + pynutil.insert('"')

        patterns = h_m | h_m_s
        self.fst = self.add_tokens(patterns).optimize()
