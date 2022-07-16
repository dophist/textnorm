# Chinese Text Normalization
## 1. Supported Normalizations
### Numbers
```
共65篇，约66万字 -> 共六十五篇，约六十六万字
共计6.42万人 -> 共计六点四二万人
同比升高0.6个百分点 -> 同比升高零点六个百分点
```

### Fraction
```
总量的1/5以上 -> 总量的五分之一以上
相当于头发丝的1/16 -> 相当于头发丝的十六分之一
```

### Percentage
```
同比增长6.3% -> 同比增长百分之六点三
增幅0.4% -> 增幅百分之零点四
```

### Date
```
2002/01/28 -> 二零零二年一月二十八日
2002-01-28 -> 二零零二年一月二十八日
2002.01.28 -> 二零零二年一月二十八日
2002/01 -> 二零零二年一月
```

### Time
```
8月16号12:00之前 -> 八月十六号十二点之前
我是5:02开始的 -> 我是五点零二分开始的
于5:35:36发射 -> 于五点三十五分三十六秒发射
8:00 a.m. 准时开会 -> 八点 a m 准时开会
```

### Score
```
比分定格在78:96 -> 比分定格在七十八比九十六
英格兰跟西班牙踢了个3-2 -> 英格兰跟西班牙踢了个三比二
```

### Money
```
售价￥1.02 -> 售价一点零二元
```

### Measure
```
重达25kg -> 二十五千克
最高气温38°C -> 最高气温三十八摄氏度
实际面积120m² -> 实际面积一百二十平方米
渲染速度10ms一帧 -> 渲染速度十毫秒一帧
```

### Number series (phone, mobile numbers)
```
可以打我手机13501234567 -> 可以打我手机一三五零一二三四五六七
```


### Whitelist (customizable direct transformation)
```
CEO -> C E O
GPU -> G P U
O2O -> O to O
B2B -> B to B
```

### Char Width Conversion
Fullwidth -> Halfwidth
```
苹果ＣＥＯ宣布发布新ＩＰＨＯＮＥ -> 苹果CEO宣布发布新IPHONE
```

### Char Removal
Sometime you may want to remove certain chars like interjections/fillers "啊", "呃" etc
```
呃这个呃啊额我不知道 -> 这个我不知道
```
* you can customize the removal list via `data/char/removal.tsv`

### Erhua(儿化音) Removal
```
这儿有只鸟儿 -> 这有只鸟
这事儿不太好办 -> 这事不太好办
儿孙满堂 -> 儿孙满堂
女儿 -> 女儿
```
* You can add words to `data/char/erhua_removal_whitelist.tsv` to avoid erroneous erhua removals.

### Invalid Char Tagger
_**If enabled**_, non-standard chars(out of charset) will be tagged with '<>'
```
我们안녕 -> 我们<안><녕>
雪の花 -> 雪<の>花
```
* invalid char tagger is switched off by default
* default charset (national standard) [通用规范汉字表](https://zh.wikipedia.org/wiki/通用规范汉字表)
* you can extend charset by customizing `data/char/charset_extension.tsv`

## How To Use

