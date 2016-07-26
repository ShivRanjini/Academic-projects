import sys
import codecs
import math
import re 

class decode():
	def __init__(self):
		self.emission={}
		self.trans={}
		self.emissionsumm={}
		self.transum={}
		self.MAXTAGS=0
		self.str=""
		 
	def readmodel(self):
		model_file=codecs.open("hmmmodel.txt","r","UTF-8")
		input=model_file.read()
		split_input=input.split("\n")
		self.MAXTAGS=int(split_input[0])
		self.emission=eval(split_input[1])
		self.trans=eval(split_input[2])
		for tag in self.emission.keys():
			self.emissionsumm[tag]=sum(self.emission[tag].values())
		for tag in self.trans.keys():
			self.transum[tag]=sum(self.trans[tag].values())
		
	def decode(self,input,fpw):
		f=re.compile('\d')
		prevprob={}
		prevprob["q0"]=math.log(1)
		wordarr=input.split(" ")
		backpointer = [dict() for x in range(len(wordarr))]
		index=0
		for word in wordarr:
			nextprob={}
			flag = 0
			for tag in self.emission.keys():
				tagdict=self.emission[tag]
				if word in tagdict.keys():
					flag=1
					break
			emissiondict=self.emission
			if flag == 0:
				if f.search(word) != None:
					innerdict={}
					emissiondict={}
					innerdict[word]=1
					emissiondict["ZZ"]=innerdict
				elif  word[0].isupper() == True:
					emissiondict={}
					innerdict={}
					innerdict[word]=1
					emissiondict["NP"]=innerdict
					
			for tag in emissiondict.keys():
				if flag == 1 and word not in self.emission[tag].keys():
					continue
				maxprob=float("-inf")
				for prevtag in prevprob.keys():
					previousprob=prevprob[prevtag]
					if prevtag in self.trans.keys():
						if len(self.trans[prevtag]) < self.MAXTAGS:					
							prevtagdict=self.trans[prevtag]
							totalprevsum=self.transum[prevtag]
							if tag in prevtagdict.keys():
								transprob=math.log(prevtagdict[tag]+1)- math.log(totalprevsum+self.MAXTAGS)
							else:
								transprob=math.log(1)-math.log(totalprevsum+self.MAXTAGS)
						else:
							prevtagdict=self.trans[prevtag]
							transprob=math.log(prevtagdict[tag])-math.log(totalprevsum)
					else:
						transprob=math.log(1)-math.log(self.MAXTAGS)
					nowprob=transprob+previousprob
					if(nowprob > maxprob):
						maxprob = nowprob
						backpointer[index][tag]=prevtag
				if flag == 1:
					tagdict=self.emission[tag]
					emissionprob=math.log(tagdict[word])-math.log(self.emissionsumm[tag])
					nextprob[tag]=emissionprob+maxprob
				else:
					nextprob[tag]=maxprob
			prevprob=nextprob
			index=index+1	
		maxprob=float("-inf")
		finalarr=[]
		temptag=""
		for tag in prevprob.keys():
			if prevprob[tag]> maxprob:
				temptag=tag		
		finalarr.append(wordarr[len(wordarr)-1]+"/"+temptag)
		index=index-1
		while(index > 0):
			temptag=backpointer[index][temptag]
			finalarr.append(wordarr[index-1]+"/"+temptag)
			index=index-1
		finalarr.reverse()
		self.str+=" ".join(finalarr)
		self.str+="\n"
		

		
def main():
	hmmdecode=decode()
	hmmdecode.readmodel()
	fpi=codecs.open(sys.argv[1],"r","UTF-8")
	fpw=codecs.open("hmmoutput.txt","w","UTF-8")
	input=fpi.read()
	inputlines=input.split("\n")
	for line_no in range(0,len(inputlines)-1):
		hmmdecode.decode(inputlines[line_no],fpw)
	fpw.write(hmmdecode.str)
	fpw.close()

if __name__ == "__main__":main()