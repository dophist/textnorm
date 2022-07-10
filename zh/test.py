import pynini
import time 
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA
from nemo_text_processing.text_normalization.zh.utils import normalize
from nemo_text_processing.text_normalization.zh.taggers.money import MoneyFst
m = MoneyFst()
n = NumberFst()
text = '1/2头牛，$1000000，￥200.5'
ph = (n.fst|m.fst)
ph = pynini.cdrewrite(ph,'','',NEMO_SIGMA)
normalize(text,ph)
print(normalize(text,ph))
