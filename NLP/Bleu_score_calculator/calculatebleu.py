import sys
import codecs
import glob
import math

class bleu:
    def __init__(self):
        self.reference_files=[]
        self.candidate_file=codecs.open(sys.argv[1],"r", "utf-8")
        self.candidate=[]
        self.references=[]
        self.best_len=[]
        
    def open_ref_file(self):
        if ".txt" in sys.argv[2]:
            self.reference_files.append(codecs.open(sys.argv[2],"r","utf-8"))
        else:
            for file in glob.glob(sys.argv[2]+"/*.txt"):
                self.reference_files.append(codecs.open(file,"r","utf-8"))

    def read_content(self):
        self.candidate=self.candidate_file.read().split("\n")
        for files in self.reference_files:
            self.references.append(files.read().split("\n"))

    def generatengram(self,line,n):
        split_lines=line.split()
        word=[]
        i=0
        while (i+n-1)<len(split_lines):
            tempword=[]
            for j in range(0,n):
                tempword.append(split_lines[i+j])
            word.append(" ".join(tempword))
            i+=1
        return word

                                 
    def calculate_precision(self,n):
        clip_count=0
        total_count=0
        if n==1:
            self.best_len=[float("inf")]*len(self.candidate)
            candidate_sen_len=0
        no_of_ref=len(self.references)
        for i in range(0,len(self.candidate)):
            dict_of_candidate={}
            dict_of_reference={}
            candidate_word_arr=self.generatengram(self.candidate[i],n)
            total_count+=len(candidate_word_arr)
            if n==1:
                candidate_sen_len=len(candidate_word_arr)
            for word in candidate_word_arr:
                if word in dict_of_candidate.keys():
                    dict_of_candidate[word]+=1
                else:
                    dict_of_candidate[word]=1
            for j in range(0,no_of_ref):
                ref_word_arr=self.generatengram(self.references[j][i],n)
                if n==1 and  abs(len(ref_word_arr)-candidate_sen_len) < self.best_len[i]-candidate_sen_len:
                    self.best_len[i]=len(ref_word_arr)
                for word in ref_word_arr:
                    if word in dict_of_reference.keys():
                        dict_of_reference.get(word)[j]+=1
                    else:
                        newlist=[0]*(no_of_ref)
                        newlist[j]=1
                        dict_of_reference[word]=newlist
            for key in dict_of_candidate.keys():
                if key in dict_of_reference.keys():
                    clip_count+=min(dict_of_candidate[key],max(dict_of_reference[key]))  
        return (clip_count*1.0)/total_count

    
def main():
    wn=1.0/4
    log_sum=0
    bl=bleu()
    bl.open_ref_file()
    bl.read_content()
    BP=0
    pn=bl.calculate_precision(1)
    if pn != 0:
        log_sum+=wn*math.log(pn)
    else:
        log_sum+=0
    candidate_len=sum([len(j) for j in [i.split() for i in bl.candidate]])
    if candidate_len>sum(bl.best_len):
        BP=1.0
    else:
        BP=math.exp(1-((sum(bl.best_len)*1.0)/candidate_len))  
    pn=bl.calculate_precision(2)
    if pn != 0:
        log_sum+=wn*math.log(pn)
    else:
        log_sum+=0
    pn=bl.calculate_precision(3)
    if pn != 0:
        log_sum+=wn*math.log(pn)
    else:
        log_sum+=0
    pn=bl.calculate_precision(4)
    if pn != 0:
        log_sum+=wn*math.log(pn)
    else:
        log_sum+=0
    bleu_score=BP*math.exp(log_sum)
    output=open("bleu_out.txt", "w")
    output.write(str(bleu_score))
    
if __name__ == "__main__":main()