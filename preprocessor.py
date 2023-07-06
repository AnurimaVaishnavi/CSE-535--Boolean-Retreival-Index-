'''
@author: Sougata Saha
Institute: University at Buffalo
'''
import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]
    

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        text = text.lower() # to lowercase
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text) # special character removal
        text = re.sub(' +', ' ', text) # removing extra whitespace
        text.strip()
        text = text.split(' ')
        text=[i for i in text if i]
        text = self.removeStopWords(text)
        text = self.porterStemming(text)
        return text

    def removeStopWords(self, data):
        filtered_data = []
        for w in data:
            if w not in self.stop_words:
                filtered_data.append(w)
        return filtered_data
   
    def porterStemming(self, data):
        stem_data = []
        for w in data:
            stem_data.append(self.ps.stem(w))
        return stem_data
    
    def convert(self,data):
        d={}
        for i in data:
            if i in d:
                d[i]+=1
            else:
                d[i]=1
        return d

