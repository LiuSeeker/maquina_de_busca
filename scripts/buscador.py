import json
from argparse import ArgumentParser
from nltk.tokenize import sexpr_tokenize
from math import log2
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
import re
import numpy as np

import search_engine.repository as se

def busca_and(index, query):
    query_terms = query.strip().split()
    if len(query_terms) == 0:
        return {}

    initial_term = query_terms[0]
    docids = set(index[initial_term]) if initial_term in index else set()
    for word in query_terms[1:]:
        result = set(index[word]) if word in index else set()
        docids &= result

    return docids

def busca_docids(index, query):
    result = [q.strip().strip('()') for q in sexpr_tokenize(query)]

    docids = set()
    for subquery in result:
        res = busca_and(index, subquery)
        docids |= res

    return docids

def busca(corpus, repo, index, query):
    # Parsing da query.
    # Recuperar os ids de documento que contem todos os termos da query.
    docids = busca_docids(index, query)

    # Retornar os textos destes documentos.
    return docids

def ranking(corpus, repo, index, docids, query):
    query = re.sub('\(', '', query)
    query = re.sub('\)', '', query)
    query = query.split()

    if len(docids) == 0:
        return list(docids)

    n = len(corpus)
    ranks = defaultdict(str)

    for doc in docids:
        tf_idf = 0
        fd = nltk.FreqDist(word.lower() for word in repo[doc])

        for e in query:
            if e in index.keys():
                ni = len(index[e])
        
            fij = fd[e]

            tf_idf += (1 + log2(fij)) * log2(n/ni)
        
        ranks[doc] = tf_idf


    '''
    for e in query:
        tf_idf = 0
        if e in index.keys():
            ni = len(index[e])
        for doc in docids:
            fd = nltk.FreqDist(word.lower() for word in repo[doc])
            fij = fd[e]

            #for word in corpus[doc].split():
            #    print(fd[word], word)
            #print(n, ni, fij, doc)

            tf_idf += (1 + log2(fij)) * log2(n/ni)
        ranks[e] = tf_idf
    '''

    #print(ranks)
    
    ret = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}

    return list(ret)  # dummy por enquanto.

def dist_leven(str1, str2):
    mat = np.zeros((len(str1)+1, len(str2)+1))

    for i in range(len(str1)+1):
        mat[i][0] = i
    for j in range(len(str2)+1):
        mat[0][j] = j

    i = 1
    while i < len(str1)+1:
        j = 1
        while j < len(str2)+1:
            if str1[i-1] == str2[j-1]:
                cost = 0
            else:
                cost = 1
            mat[i][j] = min(mat[i-1][j]+1, mat[i][j-1] + 1, mat[i-1][j-1] + cost)
            j += 1
        i += 1

    return mat[len(str1)][len(str2)]

def busca_palavra_parecida(index, query):
    for i in range(len(query)):
        if query[i] == "(" or query[i] == ")" or query[i] in index:
            continue
        else:
            novo_termo = query[i]
            min_dist = 100
            for key in index.keys():
                dist = dist_leven(query[i], key)
                if dist < min_dist:
                    min_dist = dist
                    novo_termo = key
            while True:
                resp = input("Vc quis dizer '{}' em lugar de '{}'? (s/n) > ".format(novo_termo, query[i]))
                if resp == "s":
                    query[i] = novo_termo
                    break
                elif resp == "n":
                    break
                else:
                    print("Resposta invalida")

    return query

def edit(term):
    letras = "qwertyuiopasdfghjklzxcvbnm"
    splits = [(term[:i], term[i:]) for i in range(len(term))]
    deletes = [L + R[1:] for L, R in splits]
    inserts = [L + c + R for L, R in splits for c in letras]
    replaces = [L + c + R[1:] for L, R in splits for c in letras]
    edits = deletes + inserts + replaces

    return edits

def busca_palavra_parecida2(index, query):
    for i in range(len(query)):
        if query[i] == "(" or query[i] == ")" or query[i] in index:
            continue
        else:
            ed1 = edit(query[i])
            ed1 = list(set(ed1))

            break_flag = False
            for w in ed1:
                if w in index:
                    while True:
                        resp = input("Vc quis dizer '{}' em lugar de '{}'? (s/n) > ".format(w, query[i]))
                        if resp == "s":
                            query[i] = w
                            break_flag = True
                            break
                        elif resp == "n":
                            break
                        else:
                            print("Resposta invalida")
                    if break_flag:
                        break
            
            if not break_flag:
                ed2 = []
                for w in ed1:
                    ed2 += edit(w)
                
                ed2 = list(set(ed2) - set(ed1))

                break_flag2 = False
                for w in ed2:
                    if w in index:
                        while True:
                            resp = input("Vc quis dizer '{}' em lugar de '{}'? (s/n) > ".format(w, query[i]))
                            if resp == "s":
                                query[i] = w
                                break_flag2 = True
                                break
                            elif resp == "n":
                                break
                            else:
                                print("Resposta invalida")
                        if break_flag2:
                            break

    return query

def main():
    parser = ArgumentParser()
    parser.add_argument('corpus', help='Arquivo do corpus')
    parser.add_argument('repo', help='Arquivo do repo.')
    parser.add_argument('index', help='Arquivo do index.')
    parser.add_argument('num_docs',
                        help='Numero maximo de documentos a retornar',
                        type=int)
    parser.add_argument('query', help='A query (entre aspas)')
    parser.add_argument('corretor', help='Opacao do corretor (1 : corretor por distancia; ou 2 : corretor norvig)',
                        type=int)
    args = parser.parse_args()

    corpus = se.load_corpus(args.corpus)

    with open(args.repo, 'r') as file:
        repo = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)

    query = re.sub('\(', '( ', args.query)
    query = re.sub('\)', ' )', query)
    query = query.split()
    query = [w for w in query if not w in set(stopwords.words('english')) ]
    
    if args.corretor == 1:
        query = busca_palavra_parecida(index, query)
    elif args.corretor == 2:
        query = busca_palavra_parecida2(index, query)
    else:
        print("Corretor '{}' invalido, sem correcao da query".format(args.corretor))

    
    query = " ".join(query)

    query = re.sub('\( ', '(', query)
    query = re.sub(' \)', ')', query)

    docids = busca(corpus, repo, index, query)
    docids_ranqueados = ranking(corpus, repo, index, docids, query)

    docs = [corpus[docid] for docid in docids_ranqueados[:args.num_docs]]

    for d in docs:
        print(d)
        print("")
    #print(docs)
    
if __name__ == '__main__':
    main()
