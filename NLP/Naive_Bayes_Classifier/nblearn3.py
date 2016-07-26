import glob
import sys
from preprocessing import preprocessing

    
    
class classifier:
    def __init__(self):
        self.dictionary={}
    
    def readAndTokenize(self,file_list,listindex):
        for file in file_list:
            fp=open(file,"r")
            word_list=preprocessing(fp.read())
            for w in word_list:
                if w in self.dictionary.keys():
                    self.dictionary[w][listindex] += 1
                else:
                    newlist=[1]*4
                    self.dictionary[w]=newlist
                    self.dictionary[w][listindex] += 1
                    
               
    def filewrite(self):
        fp=open("nbmodel.txt","w")
        pos_tru_sum=neg_tru_sum=pos_dec_sum=neg_dec_sum=0
        for v in self.dictionary.values():
            pos_tru_sum+=v[0]
            neg_tru_sum+=v[1]
            pos_dec_sum+=v[2]
            neg_dec_sum+=v[3]
        fp.write(str(pos_tru_sum)+" "+str(neg_tru_sum)+" "+str(pos_dec_sum)+" "+str(neg_dec_sum)+"\n")
        fp.write(str(self.dictionary))
   
def main(): 
    dir=sys.argv[1]
    filelist_positive_tru = glob.glob(dir+"/positive_polarity/truthful*/fold?/*.txt")
    filelist_negative_tru = glob.glob(dir+"/negative_polarity/truthful*/fold?/*.txt")
    filelist_pos_dec = glob.glob(dir+"/positive_polarity/deceptive*/fold?/*.txt")
    filelist_neg_dec = glob.glob(dir+"/negative_polarity/deceptive*/fold?/*.txt")
    nbclass=classifier()
    nbclass.readAndTokenize(filelist_positive_tru,0)
    nbclass.readAndTokenize(filelist_negative_tru,1)
    nbclass.readAndTokenize(filelist_pos_dec,2)
    nbclass.readAndTokenize(filelist_neg_dec,3)
    nbclass.filewrite()


    

if __name__ == "__main__":main()
    
   
       
    
    