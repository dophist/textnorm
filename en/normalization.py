from concurrent.futures import process
from operator import index
import re
import webbrowser


# pre_define
TYPE_NUM = 7
num_list = ['zero','one','two','three','four','five','six','seven',
'eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen',
'sixteen','seventeen','eighteen','nineteen','twenty','thirty','forty',
'fifty','sixty','seventy','eighty','ninety','hundred','thousand']
era_list = ['hundreds','tens','twenties','thirties','forties','fifties','sixties','seventies','eighties','nineties']
inj_list = [' ah ',' oh ',' um ',' hmm ',' woo ',' hum ']
ord_list = ['zero','first','second','third','fourth','fifth','sixth','seventh','eighth','ninth',
'tenth','eleventh','twelfth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth',
'eighteenth','nineteenth','twentieth','thirtieth','fortieth','fiftieth','sixtieth','seventieth','eightieth','ninetieth','hundredth','thousandth']
month_list = ['Januarary','February','March','April','May','June','July','August','September','October','November','December']
money_list = [('$','dollar')]
past_list = ['been','become','come','done','gone','got','gotten','had']


class number_process:
    def __init__(self):
        self.num_l = []
        self.ord_l = []
        for i in range(100):
            if i <= 20:
                self.num_l += [num_list[i]]
                self.ord_l += [ord_list[i]]
            else:
                d = int(i/10)
                dd = i - d * 10
                if dd:
                    self.num_l += [num_list[18 + d] + ' ' + num_list[dd]]
                    self.ord_l += [num_list[18 + d] + ' ' + ord_list[dd]]
                else:
                    self.num_l += [num_list[18 + d]]
                    self.ord_l += [ord_list[18 + d]]

    # convert integer eg: 1 -> one 
    def int_number_convert(self, num, modd = 'uk'):
        assert(modd in ['uk','us'])
        if num < 100:
            str0 = self.num_l[num]
        elif num < 1000:
            h = int(num/100)
            count = num - h*100
            if modd == 'uk':
                str0 = self.num_l[h] + ' ' + 'hundred' + ' and ' + self.num_l[count]
            else:
                str0 = self.num_l[h] + ' ' + 'hundred ' + self.num_l[count]
        elif num < 1000000:
            k = int(num/1000)
            count = num - 1000 * k
            if count < 100:
                str0 = self.int_number_convert(k,modd) + ' thousand and ' + self.int_number_convert(count,modd)
            else:
                str0 = self.int_number_convert(k,modd) + ' thousand ' + self.int_number_convert(count,modd)
        else:
            str0 = ''
            s = str(num)
            for i in range(len(s)):
                str0 += self.int_number_convert(int(s[i]))
                str0 += ' '
        str0 = str0.replace(' and zero','')
        return str0
        
    def ord_number_convert(self, num, modd = 'uk'):
        assert(num < 1e6)
        assert(modd in ['uk','us'])
        if num < 100:
            str0 = self.ord_l[num]
        elif num < 1000:
            h = int(num/100)
            count = num - h*100
            if modd == 'uk':
                str0 = self.num_l[h] + ' ' + 'hundred' + ' and ' + self.ord_l[count]
            else:
                str0 = self.num_l[h] + ' ' + 'hundred ' + self.ord_l[count]
        elif num < 1000000:
            k = int(num/1000)
            count = num - 1000 * k
            if count < 100:
                str0 = self.int_number_convert(k,modd) + ' thousand and ' + self.ord_number_convert(count,modd)
            else:
                str0 = self.int_number_convert(k,modd) + ' thousand ' + self.ord_number_convert(count,modd)
        str0 = str0.replace(' and zero','th')
        return str0

    # process years num
    def year_convert(self, date_str):
        li = []
        assert(len(date_str)>2)
        words = date_str.split()
        for word in words:
            if word == 'O':
                ind = 0
            else:
                ind = num_list.index(word)
                if ind > 20:
                    ind = 20 + 10 * (ind - 20)
                else:
                    ind = ind
            li += [ind]     
        if li[1] > 10:
            return self.int_number_convert(li[0]*100 + sum(li[1:]))
        else:
            return self.int_number_convert(li[0]*100 + li[1]*100 + sum(li[2:]))

    # convert era:1980s -> nineteen eighties
    def era_convert(self, date_era):
        if len(date_era)>3:
            return self.int_number_convert(int(date_era[0:-3])) + ' ' + era_list[int(date_era[-3])]
        elif len(date_era)==3:
            return era_list[int(date_era[-3])]
        else:
            return date_era

    # decimal
    def demical_convert(self, fraction):
        s1,s2 = fraction.split('.')
        num1 = int(s1)
        str1 = self.int_number_convert(num1)
        str2 = ''
        for i in range(len(s2)):
            str2 += self.int_number_convert(int(s2[i])) +' '
        return str1 + ' point ' + str2
    
    # fraction
    def fraction_convert(self, fraction):
        s1,s2 = fraction.split('/')
        num1 = int(s1)
        num2 = int(s2)
        str1 = self.int_number_convert(num1)
        str2 = self.ord_number_convert(num2)
        if num1 > 1:
            str2 = str2 + 's'
        return str1 + ' ' + str2
    def remove_a(self,line):
        return line.replace(' a ',' one ')

    # percent
    def percent(self,line):
        return line.replace('%',' percent')

    # time ## need more cases
    def time_process(self,line):
        r = re.compile('\d{1,2}:\d{1,2}')
        li = r.findall(line)
        for item in li:
            item_new = item.replace(':',' ')
            it = item_new.split()
            if len(it):
                a = it[0]
                b = it[1]
                if int(b) == 0:
                    item_new = item_new.replace(b,"o'clock")
                line = line.replace(item,item_new)
        
        return line

    # convert_line
    def convert_line(self, line):
        # time
        line = self.time_process(line)
        # comma
        r = re.compile('\d+,\d+')
        ll = r.findall(line)
        for item in ll:
            item_new = item.replace(',','')
            line = line.replace(item,item_new)
        # ord 
        li = []
        r = re.compile('\d+st|\d+nd|\d+rd|\d+th')
        li = r.findall(line)
        for item in li:
            num = int(item[:-2])
            numstr = self.ord_number_convert(num)
            line = line.replace(item,numstr)
        # year
        li = []
        strstr = line.split()
        for i in range(len(strstr)-1):
            if strstr[i] in self.num_l and strstr[i+1] in self.num_l:
                if self.num_l.index(strstr[i+1]) < 10:
                    pass
                else:
                    date_str = strstr[i] + ' ' + strstr[i+1]
                    line = line.replace(date_str,self.year_convert(date_str))
                
        # era
        li = []
        r = re.compile('\d+s')
        li += r.findall(line)
        for item in li:
            line = line.replace(item, self.era_convert(item))
        # month
        li = []
        for month in month_list:
            r = re.compile(month+' '+'\d+')
            li += r.findall(line)
        for item in li:
            length = len(str(int(item[-2:])))
            num = int(item[-length:])
            numstr = self.ord_number_convert(num)
            line = line.replace(' '+ item[-length:],' '+ numstr)
            line = line.replace(item[-length:] + ' ',numstr + ' ')
        # fraction
        r = re.compile('\d+/\d+')
        li = r.findall(line)
        for item in li:
            line = line.replace(item,self.fraction_convert(item))
        # demical
        r = re.compile('\d+\.\d+')
        li = r.findall(line)
        for item in li:
            line = line.replace(item,self.demical_convert(item))
        # card_num
        li = []
        r = re.compile('\d+')
        li += r.findall(line)
        for item in li:
            line = line.replace(item,' ' + self.int_number_convert(int(item))+ ' ')
            line = line.replace('  ',' ')
        line =  self.percent(line)
        return line
        


class data_process:
    def __init__(self):
        pass
    # get_data
    def read_file(self, file_name):
        with open(file_name) as f:
            return f.readlines()

    # search according to type
    def get_type(self, type_num):
        lines = self.read_file('test.txt')
        lines_list = []
        for i in range(TYPE_NUM):
            lines_list += [[]]
        for i in range(len(lines)):
            line = lines[i].strip()
            _index = int(line[0]) - 1
            lines_list[_index] += [[i,line[1:]]]
        # type_num == -1 return all results
        if type_num == -1:   
            return lines_list
        else:
            return lines_list[type_num - 1]

    # calculate accuracy
    def calc_accuracy(self, type_num):
        gt_lines = self.read_file('gt.txt')
        test_li = self.get_type(type_num)
        for index in range(len(gt_lines)):
            gt_lines[index] = gt_lines[index].strip() 
        if type_num == -1:
            count0 = 0
            count = len(gt_lines)
            err_list = []
            for i in range(TYPE_NUM):
                for item in test_li[i]:
                    index = item[0]
                    line = item[1]
                    line = normalize(line)
                    gt_lines[index] = normalize(gt_lines[index])
                    line = line.replace(' ','')
                    gt_lines[index] = gt_lines[index].replace(' ','')
                    if line == gt_lines[index]:
                        count0 += 1
                    else:
                        err_list += [line]
            return count0/count,err_list
        else:
            count0 = 0
            count = len(test_li)
            err_list = []
            for item in test_li:
                index = item[0]
                line = item[1]
                gt_lines[index] = normalize(gt_lines[index])
                line = normalize(line)
                line = line.replace(' ','')
                gt_lines[index] = gt_lines[index].replace(' ','')
                if line == gt_lines[index]:
                    count0 += 1
                else:
                    err_list += [line]
            return count0/count,err_list
    def file_trans(self,file):
        with open(file) as f:
            with open('output.txt','w+') as ff:
                r = f.readlines()
                for i in range(len(r)):
                    r[i] = normalize(r[i].strip()).strip()+'\n'
                ff.writelines(r)
     
class sign:
    def __init__(self):
        pass
    
    # interjection
    def interjection(self,line):
        for item in inj_list:
            line = line.replace(item,' ')
        return line

    # remove en dash
    def endash_remove(self,line):
        return line.replace('-','')
    

    def sign_process(self,line):
        line = self.minus_sign(line)
        line = self.endash_remove(line)
        line = self.interjection(line)
        line = self.mult_sign(line)

        line = self.eq_sign(line)
        line = self.plus_sign(line)
        return line
    
    # need to be completed
    def mult_sign(self,line):

        line = line.replace('*',' multiply ')
        line = line.replace('×',' multiply ')
        return line
    
    def minus_sign(self,line):
        return line
    
    def plus_sign(self,line):
        return line.replace('+',' plus ')
    
    def eq_sign(self,line):
        return line.replace('=',' equals ')


class accent:
    def __init__(self):
        pass
    
    # convert ' sign

    def am_convert(self, line, c_type = 1):
        if c_type:
            return line.replace('\'m',' am')
        else:
            return line.replace(' am ','\'m ')

    def are_convert(self, line, c_type = 1):
        if c_type:
            return line.replace('\'re',' are')
        else:
            return line.replace(' are ','\'re ')

    def have_convert(self, line, c_type = 1):
        if c_type:
            return line.replace('\'ve',' have')
        else:
            return line.replace(' have','\'ve')     
    
    def nt_convert(self, line, c_type = 1):
        assert c_type == 1
        if c_type:
            line = line.replace('n\'t',' not')
            return line.replace(' ca ',' can ')
    
    def has_convert(self, line, c_type = 0):
        assert c_type == 0
        if c_type:
            return None
        else:
            return line.replace(' has ','\'s ')

    def is_convert(self, line, c_type = 00):
        assert c_type == 0
        if c_type:
            return None
        else:
            return line.replace(' is ','\'s ')
    
    def ll_convert(self, line, c_type = 1):
        if c_type:
            return line.replace('\'ll',' will')
        else:
            return line.replace(' will','\'ll')  

    def d_convert(self, line, c_type = 1):
        if c_type:
            return line.replace('\'d',' would')
        else:
            return line.replace(' would','\'d')

    def accent_process(self, line):
        line = self.am_convert(line)
        line = self.nt_convert(line)
        line = self.are_convert(line)
        line = self.have_convert(line)
        line = self.ll_convert(line)
        line = self.d_convert(line)
        # line = self.has_convert(line)
        # line = self.is_convert(line)
        return line


class sub_word:
    def __init__(self,mode='hold'):
        self.word_list = [('gonna','going to'),('gotta','got to'),('wanna','want to'),('mph','mile per hour')]
        self.load_d('data/abbr.txt',mode)
        self.load_d('data/subs.txt',mode)
        pass
    
    def load_d(self, file, mode = 'hold'):
        with open(file,'r') as f:

            lines = f.readlines()
            for line in lines:
                item = line.split()
                if len(item) == 0:
                    pass
                else:
                    if mode == 'upper':
                        item[0] = item[0].upper()
                        item[1] = item[1].upper()
                    elif mode == 'lower':
                        item[0] = item[0].lower()
                        item[1] = item[1].lower()
                    self.word_list += [(item[0],item[1])]
        return 
    
    def sub_pro(self, line):
        for old_w,new_w in self.word_list:
            old_w = ' ' + old_w + ' '
            new_w = ' ' + new_w + ' '
            line = line.replace(old_w,new_w)
        return line 


# xxx.com
def net_process(line):
    line = line.replace('/',' slash ')
    line = line.replace('.',' dot ')
    line = line.replace('@',' at ')
    return line

def money_convert(line):
    for sign,word in money_list:
        r = re.compile('\$\d+\.*\d+')
        li = r.findall(line)
        for item in li:
            if float(item[1:])<=1:
                line = line.replace(item,item[1:]+' dollar')
            else:
                line = line.replace(item,item[1:]+' dollars')
    return line

def upper_combine(line):
    words = line.split()
    wb = ''
    wn = ''
    str1 = ''
    str2 = ''
    for word in words:
        if word.isupper():
            if len(str1) >= 1:
                str2 += ' '
            str1 += word
            str2 += word
        else:
            line = line.replace(str2,str1)
            str1 = ''
            str2 = ''    
    if len(str1)>=2:
        line = line.replace(str2,str1)
        str1 = ''
        str2 = ''
    return line


def normalize(line, mode=0):
    # test
    n = number_process()
    s = sign()
    a = accent()
    ss = sub_word('hold')
    line = ' ' + line + ' '
    if mode:
        line = line.lower()
    line = ss.sub_pro(line)
    line = a.accent_process(line)
    line = money_convert(line)
    line = s.sign_process(line)
    line = n.convert_line(line)
    line = net_process(line)
    # test
    if mode:
        line = line.upper()
    return line.strip() 



if __name__ == '__main__':
    d = data_process()
    print(normalize('60,500'))
    print(normalize('6:30'))
    print(normalize('70th'))
    print(normalize('Januarary 1 2014'))
    print(normalize('60,500'))
    print(normalize('twenty twenty two'))
    print(normalize('493431778@qq.com/s'))
    print(upper_combine('There is a U F O'))



