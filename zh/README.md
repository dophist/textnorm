# Text Normalization For Chinese
## cases:
|  previous  |    after TN    |
|:----------:|:--------------:|
|  123.5个   | 一百二十三点五个|
|  0.2223只  | 零点二二二三只  |
|  12315     |  一二三一五     |	
|  5:02      |  五点零二分     |
|  5:2       |  五比二         |
|  5:35:36   |五点三十五分三十六秒|
| 2002/01/28 |二零零二年一月二十八日|
| 2002-01-28 |二零零二年一月二十八日|
|2002.01.28  |二零零二年一月二十八日|
|  2002/01   |二零零二年一月   |
| 02/11      | 零二年十一月    |
| 2/11       | 十一分之二      |
| O2O        |  O to O         |
| F I F A    |  FIFA          |
| 2+1=3      |  二加一等于三   |
| 这儿、门儿  | 这、门        |
|  女儿      |    女儿       |
|   안녕     |   <안><녕>     |
|  ￥1.02    | 一点零二元     |
|  25kg      |  二十五千克    |
|   ：  ？    |      :  ?      |
|  26%       |   百分之二十六 |


## structure
data/
|      tsv file             |      role                             |
|:--------------------------:|:------------------------------------:|
|./measure/measure.tsv      |Common unit symbols in Chinese format  |
|./measure/measure_zh.tsv   |Commonly used Chinese character units  |
|./erhua/erhua.tsv  	     |      Whitelist to remove paedophones  |
|./halfwidth/halfwidth      |          Fullwidth form to halfwidth  |
|./money/currency.tsv 	     |              Common currency symbols  |
|./sign/sign.tsv  	     |      Transcription of common symbols  | 
|./whitelist/whitelist.tsv  |                 Common abbreviations  |
|./number/digit.tsv  	     |         Chinese numerals one to nine  |
|./number/zero.tsv          |                Chinese numerals zero  |
|./number/digit_teen.tsv    |Chinese numerals used in the tens place|

