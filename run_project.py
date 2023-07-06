'''
@author: Sougata Saha
Institute: University at Buffalo
'''

# from selectors import EpollSelector
from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
from linkedlist import Node
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib
import heapq

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def intersect(self,A,B):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-
            value of a document.
            To be implemented."""
        mergedList=LinkedList()
        count,length=0,0
        while A and B:
            count+=1
            if A.data<B.data:
                A=A.next
            elif A.data>B.data:
                B=B.next
            else:
                mergedList.length+=1
                if mergedList.head==None:
                    if A.tfidf>B.tfidf:
                        mergedList.head=Node(A.data)
                        prev = mergedList.head
                        prev.tfidf= A.tfidf
                    else:
                        mergedList.head=Node(B.data)
                        prev = mergedList.head
                        prev.tfidf = B.tfidf
                else:
                    if A.tfidf>B.tfidf:
                        prev.next=Node(A.data)
                        prev=prev.next
                        prev.tfidf=A.tfidf
                    else:
                        prev.next=Node(B.data)
                        prev=prev.next
                        prev.tfidf=B.tfidf
                A=A.next
                B=B.next
        return mergedList, count

    # def _daat_and(self):
    #     """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
    #         Use appropriate parameters & return types.
    #         To be implemented."""
        
    #     raise NotImplementedError

    # def _get_postings(self):
    #     """ Function to get the postings list of a term from the index.
    #         Use appropriate parameters & return types.
    #         To be implemented."""
    #     raise NotImplementedError

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt
    
    def mergeskip(self,A,B):
        count=0
        while A and B:
            count+=1
            if A.data<B.data:
                if A.skip and A.skip.data<=B.data:
                    A=A.skip
                else:
                    A=A.next
            elif A.data>B.data:
                if B.skip and B.skip.data<=A.data:
                    B=B.skip
                else:
                    B=B.next
            else:
                A=A.next
                B=B.next
        return count


    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        a,tokens=[],[]
        with open(corpus, 'r', encoding="utf8") as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                dictionary_document = self.preprocessor.convert(tokenized_document)
                a.append([doc_id,tokenized_document,dictionary_document])
                tokens.extend(tokenized_document)
        tokens=set(tokens)
        self.indexer.generate_inverted_index(a,tokens)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
    

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].head),
                "node_type": str(type(index[kw].head)),
                "node_value": str(index[kw].head.data),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}
        index = self.indexer.get_index()

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            
            input_term_arr = list(set(self.preprocessor.tokenizer(query)))  # Tokenized query. To be implemented.
            lists = []
            for term in input_term_arr:
                postings, skip_postings = None, None
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""
                if term in index and term!="":
                    postings = index[term].traverse_list()
                    skip_postings = index[term].traverse_skips()
                    lists.append([index[term].head,index[term].length])
                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
            and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = 0, 0, 0, 0
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            if lists:
                if len(lists)>1:
                    lists.sort(key = lambda x: x[1])
                    and_comparisons_no_skip=0
                    and_comparisons_skip = 0
                    A,B = lists[0][0],lists[1][0]
                    l, count1= self.intersect(A,B)
                    A,B = lists[0][0],lists[1][0]
                    count2 = self.mergeskip(A,B)
                    and_comparisons_no_skip+=count1
                    and_comparisons_skip+=count2
                    l.add_skip_connections()
                    for i in range(2,len(lists)):
                        A,B=l.head,lists[i][0]
                        l, count1 = self.intersect(A,B)
                        l.add_skip_connections()
                        count2 = self.mergeskip(A,B)
                        and_comparisons_no_skip+=count1
                        and_comparisons_skip+=count2
                    and_comparisons_no_skip_sorted = and_comparisons_no_skip
                    and_comparisons_skip_sorted = and_comparisons_skip
                    p=l.head
                else:
                    l= lists[0][0]
                    p=l
                and_op_no_skip=[]
                a=[]
                while p:
                    and_op_no_skip.append(p.data)
                    a.append([p.data,p.tfidf])
                    p=p.next
                and_op_skip = and_op_no_skip
                a.sort(key = lambda x: (-x[1],x[0]))
                and_op_no_skip_sorted=[]
                for i in a:
                    and_op_no_skip_sorted.append(i[0])
                and_op_skip_sorted = and_op_no_skip_sorted

            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted
        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="C:/Users/anuri/IRProject2/CSE_4535_Fall_2022/project2/data/input_corpus.txt",default="C:/Users/anuri/IRProject2/CSE_4535_Fall_2022/project2/data/input_corpus.txt")
    parser.add_argument("--output_location", type=str, help="C:/Users/anuri/IRProject2/CSE_4535_Fall_2022/project2/data/sample_output.json", default=output_location)
    parser.add_argument("--username", type=str,
                        help="anurimav",default="anurimav")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)

