'''
@author: Sougata Saha
Institute: University at Buffalo
'''
import math
from linkedlist import LinkedList
from linkedlist import Node
from collections import OrderedDict



class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, documents,tokens):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        for word in tokens:
            self.inverted_index[word]=LinkedList()
            for document in documents:
                doc_id,tokenized_document,dictionary_document=document[0],document[1],document[2]
                if word in dictionary_document:
                    if self.inverted_index[word].head == None:
                        self.inverted_index[word].head = Node(doc_id)
                        curr = self.inverted_index[word].head
                    else:
                        prev = curr
                        prev.next = Node(doc_id)
                        curr = prev.next
                    self.inverted_index[word].length+=1
                    curr.tf = dictionary_document[word]/len(tokenized_document)
                    curr.freq = dictionary_document[word]
            self.inverted_index[word].tail=curr
            self.inverted_index[word].idf = len(documents)/self.inverted_index[word].length
            self.inverted_index[word].head=self.inverted_index[word].sortList(self.inverted_index[word].head)
            self.inverted_index[word].calculate_tf_idf()
    

    # def add_to_index(self, term_, doc_id_):
    #     """ This function adds each term & document id to the index.
    #         If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
    #         If a term is present, then add the document to the appropriate position in the posstings list of the term.
    #         To be implemented."""
    #     raise NotImplementedError


    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for term in self.inverted_index:
            len = self.inverted_index[term].length
            self.inverted_index[term].n_skips = math.floor(math.sqrt(len))
            if  self.inverted_index[term].n_skips *  self.inverted_index[term].n_skips == len:
                 self.inverted_index[term].n_skips =  self.inverted_index[term].n_skips - 1
            self.inverted_index[term].skip_length = int(round(math.sqrt(len),0))
            self.inverted_index[term].add_skip_connections()
        # print(self.inverted_index['problem'].length)
        # print(self.inverted_index['problem'].skip_length)
        # print(self.inverted_index['problem'].traverse_list())
        # print(self.inverted_index['problem'].traverse_skips())
    



    