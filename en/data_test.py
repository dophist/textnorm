from nemo_text_processing.text_normalization.normalize import Normalizer
class data_tester:
    def __init__(self,lang = 'en'):
        print('tester initializing.....')
        self.normalizer = Normalizer('cased',lang = lang)
        self.count = 0
        self.sum = 0
        pass
    
    def test_file(self,file,if_print=True,if_pf=True,pre_process ='none'):
        with open(file,'r') as f:
            lines = f.readlines()
            outputfile = open('output.tsv','w+')
            self.sum = len(lines)
            for line in lines:
                if pre_process == 'lower':
                    line = line.lower()
                elif pre_process == 'upper':
                    line = line.upper()
                if len(line.split('	'))<2:
                    continue
                line0 = line.split('\t')[0].strip()
                line1 = line.split('\t')[1].strip()
                norm_line0 = self.normalizer.normalize(line0)
                norm_line1 = self.normalizer.normalize(line1)
                if norm_line0 == norm_line1:
                    self.count += 1
                else:
                    if if_print:
                        print(norm_line0)
                        print(norm_line1)
                    if if_pf:

                        print(norm_line0+'	'+norm_line1,file=outputfile)
            return self.sum,self.count
    
    def get_accuracy(self):
        return self.count/self.sum
        
    def test_sentence(self,line):
        return self.normalizer.normalize(line,verbose=1)
                    
                    
            
            
if __name__ == "__main__":
    d = data_tester()
    sumnum,count=d.test_file('pairs.tsv',1,1,'lower')
    print(sumnum,count)
    print(d.get_accuracy())
