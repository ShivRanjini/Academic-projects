import sys
import os
import math
from preprocessing import preprocessing 
class nbclassify:
    def __init__(self):
        fp=open("nbmodel.txt","r")
        model=fp.readlines()
        self.sum=list(map(int,model[0].strip("\n").split(" ")))
        self.dictionary=eval(model[1])

    def compute(self,wordlist):
        prob_pos_tru=prob_neg_tru=prob_pos_dec=prob_neg_dec=0
        for w in wordlist:
            if w in self.dictionary.keys():
                prob_pos_tru=prob_pos_tru+math.log(self.dictionary[w][0]/(self.sum[0]))
                prob_neg_tru=prob_neg_tru+math.log(self.dictionary[w][1]/(self.sum[1]))
                prob_pos_dec=prob_pos_dec+math.log(self.dictionary[w][2]/(self.sum[2]))
                prob_neg_dec=prob_neg_dec+math.log(self.dictionary[w][3]/(self.sum[3]))
        prob_pos_tru=prob_pos_tru+math.log(0.25)
        prob_neg_tru=prob_neg_tru+math.log(0.25)
        prob_pos_dec=prob_pos_dec+math.log(0.25)
        prob_neg_dec=prob_neg_dec+math.log(0.25)
        maximum=max(prob_pos_tru,prob_neg_tru,prob_pos_dec,prob_neg_dec)
        if maximum == prob_pos_tru:
          result="truthful positive "
        elif maximum == prob_neg_tru:
          result="truthful negative "
        elif maximum == prob_pos_dec:
          result="deceptive positive "
        else:
          result="deceptive negative "
        return result  


def main():  
    fpw=open("nboutput.txt","w")
    classify=nbclassify()
    for root,direc,filelist in os.walk(sys.argv[1]):
        for file in filelist:
          if file.endswith('.txt') and len(direc)==0:
            fp=open(os.path.join(root,file),"r")
            word_list=preprocessing(fp.read())
            result=classify.compute(word_list)
            result+=os.path.join(root,file)
            fpw.write(result+"\n")

if __name__ == "__main__":main()
