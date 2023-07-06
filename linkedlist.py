'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, data=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.data = data  # Assign data
        self.next = None  # Initialize next as null
        self.skip = None  # Initialize skip as null
        self.tfidf = 0 #Initialize tfidf score as 0
        self.tf = 0 #Initialize tf to 0
        self.freq = 0 #Initialize the frequency of the term to 0


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = 0

    def traverse_list(self):
        traversal = []
        if self.head is None:
            return
        else:
            start = self.head
            while start:
                traversal.append(start.data)
                start=start.next
            return traversal

    def traverse_skips(self):
        if self.length<=2:
            return []
        traversal = []
        if self.head is None:
            return
        else:
            start = self.head
            while start:
                traversal.append(start.data)
                if start.skip:
                    start=start.skip
                else:
                    break   
            return traversal

    def add_skip_connections(self):
        temp = self.head
        prev = temp
        count, skipcount =0,0
        while temp and skipcount<self.n_skips:
            while temp and count<self.skip_length:
                count+=1
                temp=temp.next
            prev.skip = temp
            prev = temp
            count =0
            skipcount+=1

    def sortList(self,head):
        if head and head.next:
            firstend = self.middle(head)
            list2 = firstend.next
            firstend.next = None
            return self.merge(self.sortList(head), self.sortList(list2)) 
        return head
    def middle(self,A):
        slow,fast=A,A
        while(fast and fast.next):
            prev=slow
            slow=slow.next
            fast=fast.next.next
        return prev
    def merge(self,A,B):
        dummy = Node(-1)
        prev = dummy
        while A and B:
            if A.data<=B.data:
                prev.next=A
                prev = A
                A=A.next
            else:
                prev.next=B
                prev=B
                B=B.next
        if A:
            prev.next = A
        if B:
            prev.next = B
        return dummy.next
    
    def calculate_tf_idf(self):
        temp = self.head
        idf = self.idf
        while temp:
            temp.tfidf = temp.tf*idf
            temp = temp.next

        

    # def insert_at_end(self, value):
    #     """ Write logic to add new elements to the linked list.
    #         Insert the element at an appropriate position, such that elements to the left are lower than the inserted
    #         element, and elements to the right are greater than the inserted element.
    #         To be implemented. """
    #     raise NotImplementedError

