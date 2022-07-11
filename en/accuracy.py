from nemo_text_processing.text_normalization.normalize import Normalizer
from normalization import normalize as np

acc = 0
m = 0
with open('data.tsv') as f:
    ff = open('test.txt', 'w')
    x = f.readlines()
    n = Normalizer('cased')
    for line in x:
        line0 = line.split('	')[0].strip()
        line1 = line.split('	')[1].strip()

        norm_line = np(line0, mode='lower')
        norm_line = n.normalize(norm_line)

        line1 = np(line1, mode='lower')
        line1 = n.normalize(line1)
        if norm_line == line1:
            acc += 1
        else:
            print(norm_line, file=ff)
        m += 1
print("acc = ", acc)
print("percent = ", acc / m)
