import pynini
from pynini.lib import pynutil,utf8
from pynini.lib.rewrite import top_rewrite
from nemo_text_processing.text_normalization.zh.taggers.money import MoneyFst

b = MoneyFst()
text = '我有￥1.0'
Sigma = pynini.closure(utf8.VALID_UTF8_CHAR)
pp = pynini.closure(pynutil.insert('20')+pynini.accep('s',1),1).optimize()
ppp = pynini.cdrewrite(pp,'','',Sigma)
print((text @ b).string())
