import sys
import codecs
class learn:
	def __init__(self):
		self.emissiondict={}
		self.transdict={}
		self.MAXTAGS=0
		
	def readandpopulate(self,input):
		line_input=input.split("\n")
		del line_input[-1]
		tagtrack=[]
		for line in line_input:
			previoustag="q0"
			for word in line.split(" "):
				tagandword=word.split("/")
				stringword=""
				tagandword_len=len(tagandword)
				tag=tagandword[tagandword_len-1]
				if tag not in tagtrack:
					tagtrack.append(tag)
				for i in range(0,tagandword_len-1):
					stringword += tagandword[i]
				self.add_dict(self.emissiondict,tag,stringword)
				self.add_dict(self.transdict,previoustag,tag)
				previoustag=tag
		self.MAXTAGS=len(tagtrack)
		
	def add_dict(self,dictonary,firstkey,secondkey):
		if firstkey in dictonary.keys():
			innerdict=dictonary.get(firstkey)
			if secondkey in innerdict.keys():
				innerdict[secondkey]+=1
			else:
				innerdict[secondkey]=1
		else:
			innerdict={}
			innerdict[secondkey]=1
			dictonary[firstkey]=innerdict
		
	def write(self):
		out_file=codecs.open("hmmmodel.txt","w","UTF-8")
		out_file.write(str(self.MAXTAGS)+"\n")
		out_file.write(str(self.emissiondict)+"\n")
		out_file.write(str(self.transdict))
		out_file.close()
	
def main():
	hmmlearn=learn()
	input_file=codecs.open(sys.argv[1],"r","UTF-8")
	input=input_file.read()
	hmmlearn.readandpopulate(input)
	hmmlearn.write()
	
if __name__ == "__main__":main()			
			
			
				