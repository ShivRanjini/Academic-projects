import re


class stemmer:
    cop=r'(?:[bcdfghjklmnpqrstvwxz]|(?<=[aeiou])y|^y)*'
    c=r'(?:[bcdfghjklmnpqrstvwxz]|(?<=[aeiou])y|^y)+'
    v=r'(?:[aeiou]|(?<![aeiou])y)+'
    vop=r'(?:[aeiou]|(?<![aeiou])y)*'  
     
    def m(self,strs):
        combo=""
        m=-1
        list1=[]
        while((strs not in list1)):
            p=re.compile(self.cop+combo+self.vop);
            list1=re.findall(p,strs)
            combo+=self.v+self.c
            m+=1
        return m  
      
    def stem(self,string):
        self.string=string
        if(len(self.string)<= 2):
            return self.string
        else:
            self.step1ab()
            self.step1c()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
        return self.string
    
    def cvc(self,i):
        if(len(self.string[:i])>=2 and (re.match(self.c, self.string[i],0) and self.string[i] not in 'wxy') and (re.match(self.v, self.string[i-1],0)) and (re.match(self.c, self.string[i-2],0))):
            return True
        else:
            return False
        
    def replaceend(self,last,new_word,minlen):
        if  self.m(self.string[:-len(last)])> minlen and self.string.endswith(last):
            self.string = self.string=re.sub(last+'$',new_word, self.string)
            return True 
        else:
            return False 
             
    def step1ab(self):
        if (self.string[-1] == 's'):
            if self.string.endswith("sses"):
                self.string=re.sub(r'sses$', 'ss', self.string)  
            elif  self.string.endswith("ies"):
                self.string=re.sub(r'ies$', 'i', self.string) 
            elif self.string.endswith("ss"):
                self.string=re.sub(r'ss$', 'ss', self.string)
            else:
                self.string=re.sub(r's$', '', self.string)
         
        if(self.string.endswith("eed")):
            if self.m(self.string[:-3]) > 0:
                self.string=re.sub(r'eed$', 'ee', self.string)
        elif ((self.string.endswith("ed") and re.match('[a-z]*'+self.v+'[a-z]*', self.string[:-2],0)) or (self.string.endswith("ing")) and re.match('[a-z]*'+self.v+'[a-z]*', self.string[:-3],0)):
            self.string=re.sub(r'ed$|ing$','', self.string)
            if self.string.endswith("at"):
                self.string=re.sub(r'at$', 'ate', self.string)
            elif self.string.endswith("bl"):
                self.string=re.sub(r'bl$', 'ble', self.string)
            elif self.string.endswith("iz"):
                self.string=re.sub(r'iz$', 'ize', self.string) 
            elif re.match(self.c,self.string[-1],0) and len(self.string)>=2 and self.string[-1] == self.string[-2] and self.string[-1] not in 'lsz':
                self.string=self.string[:-1]
            elif self.m(self.string) == 1 and self.cvc(len(self.string)-1):
                self.string+="e"
        
                
                
                
            
    def step1c(self):
        if(self.string.endswith("y") and re.match('[a-z]*'+self.v+'[a-z]*', self.string[:-1],0)):
            self.string=re.sub(r'y$', 'i', self.string)   
            
    
    def step2(self):
        if self.string[-2] == 'a':
            self.replaceend("ational", 'ate', 0) or (not self.string.endswith("ational") and self.replaceend("tional",'tion', 0))
        elif self.string[-2] == 'c':
            self.replaceend("enci", 'ence', 0) or self.replaceend("anci", 'ance',0)
        elif self.string[-2] == 'e':
            self.replaceend("izer",'ize',0)
        elif self.string[-2] == 'l':
            self.replaceend("bli", 'ble', 0) or self.replaceend("alli", 'al', 0)  or self.replaceend("entli", 'ent', 0)   or self.replaceend("eli", 'e', 0)  or self.replaceend("ousli", 'ous', 0)  
        elif self.string[-2] == 'o':
            self.replaceend("ization", 'ize', 0)  or   (not self.string.endswith("ization") and self.replaceend("ation",'ate', 0)) or self.replaceend("ator", 'ate', 0)
        elif self.string[-2] == 's':
            self.replaceend("alism", 'al',0)  or  self.replaceend("iveness", 'ive', 0) or self.replaceend("fulness", 'ful', 0) or  self.replaceend("ousness", 'ous', 0)
        elif self.string[-2] == 't':
            self.replaceend("aliti", 'al', 0)  or self.replaceend("iviti",'ive', 0) or  self.replaceend("biliti", 'ble', 0) 
        elif self.string[-2] == 'g': 
            self.replaceend("logi", 'log', 0) 
            
            

    def step3(self):
        if self.string[-1] == 'e':
            self.replaceend("icate","ic",0) or self.replaceend("ative","",0) or self.replaceend("alize","al",0)
        elif  self.string[-1]  == 'i':
            self.replaceend("iciti","ic",0)
        elif  self.string[-1]  == 'l':
            self.replaceend("ical","ic",0) or self.replaceend("ful","",0)  
        elif  self.string[-1]  == 's':
            self.replaceend("ness","",0)   
    
    def step4(self):
        if len(self.string)<2:
            return
        if self.string[-2] == 'a':
            self.replaceend("al","",1)
        elif self.string[-2] == 'c':
            self.replaceend("ance","",1) or self.replaceend("ence","",1)
        elif self.string[-2] == 'e':
            self.replaceend("er","",1)
        elif self.string[-2] == 'i':
            self.replaceend("ic","",1)
        elif self.string[-2] == 'l':
            self.replaceend("able","",1) or  self.replaceend("ible","",1)
        elif self.string[-2] == 'n':
            self.replaceend("ant","",1) or self.replaceend("ement","",1) or (not self.string.endswith("ement") and self.replaceend("ment","",1)) or (not self.string.endswith("ment" ) and self.replaceend("ent","",1))
        elif self.string[-2] == 'o':
            if (len(self.string)>=4 and (self.string[-4] == 't' or self.string[-4] == 's') and self.replaceend("ion","",1)): pass
            else:
                self.replaceend("ou","",1)
        elif self.string[-2] == 's':
            self.replaceend("ism","",1)
        elif self.string[-2] == 't':
            self.replaceend("ate","",1) or self.replaceend("iti","",1)  
        elif self.string[-2] == 'u':
            self.replaceend("ous","",1)
        elif self.string[-2] == 'v':
            self.replaceend("ive","",1)
        elif self.string[-2] == 'z':
            self.replaceend("ize","",1)
    
    def step5(self):
        if self.string[-1] == 'e':
            a = self.m(self.string[:-1])
            if a > 1 or (a == 1 and not self.cvc(-2)):
                self.string = self.string[:-1]
        if self.string[-1] == 'l' and len(self.string)>= 2 and self.string[-1] == self.string[-2] and self.m(self.string) > 1:
            self.string = self.string[:-1]

               
def stem(list):
    try:                                   
        s=stemmer()
        returnlist=[]
        for word in list:
            if all(letter.isalpha() for letter in word):
                returnlist.append(s.stem(word))
            else:
                returnlist.append(word)
        return returnlist
    except:
        return list
    
