'''Funções para manipulação de corpus, repositórios e indices.
'''

import json
import re
import nltk
from collections import defaultdict
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize


def load_corpus(filename):
    '''Carrega o corpus.

    O corpus deve estar armazenado em formato JSON. Deve ser um dicionário
    mapeando uma string representando o docid de um documento para outra string
    contendo o texto do documento.

    Args:
        filename: nome do arquivo do corpus.

    Returns:
        Um dicionário que mapeia docid (str) para um documento (str).
    '''
    with open(filename, 'r') as file_corpus:
        return json.load(file_corpus)


def create_repo(corpus):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    repo = {}
    stop_words = set(stopwords.words('english')) 

    for fileid in corpus.keys():
        filtered_text = corpus[fileid].lower()
        filtered_text = filtered_text.replace("\n"," ")
        filtered_text = re.sub(re.compile("\\\S+;", re.M), "", filtered_text)
        filtered_text = re.sub(re.compile("&\S+;", re.M), "", filtered_text)
        filtered_text = re.sub(re.compile("[A-Z.]+>", re.M), "", filtered_text)
        filtered_text = re.sub(re.compile("[ ]{2,}", re.M), " ", filtered_text)
        filtered_text = re.sub(re.compile("'\S+", re.M), "", filtered_text)
        filtered_text = re.sub(re.compile('\\"', re.M), '', filtered_text)
        filtered_text = re.sub(re.compile('\. ', re.M), ' ', filtered_text)
        filtered_text = re.sub(re.compile('\, ', re.M), ' ', filtered_text)
        filtered_text = re.sub(re.compile('\(', re.M), '', filtered_text)
        filtered_text = re.sub(re.compile('\)', re.M), '', filtered_text)
        filtered_text = re.sub(re.compile('\>', re.M), '', filtered_text)
        filtered_text = re.sub(re.compile('-/', re.M), '', filtered_text)
        filtered_text = re.sub(re.compile('\d+[\.|,]*', re.M), '', filtered_text)
        tokens = nltk.word_tokenize(filtered_text)
        tokens = [w for w in tokens if not w in stop_words]
        repo[fileid] = tokens

    return repo


def create_index(repo):
    '''Indexa os documentos de um corpus.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.

    Returns:
        O índice reverso do repositorio: um dicionario que mapeia token para
        lista de docids.
    '''
    index = defaultdict(lambda: defaultdict(list))

    for fileid in repo.keys():
        for i in range(len(repo[fileid])):
            index[repo[fileid][i]][fileid].append(i)

    return index


def save_repo(filename, repo):
    '''Grava um repositório.

    O repositório será gravado como um arquivo JSON.

    Args:
        filename: nome do arquivo.
        repo: dicionario que mapeia docid para uma lista de tokens.
    '''
    with open(filename, 'w') as file_repo:
        json.dump(repo, file_repo, indent=4)


def save_index(filename, index):
    '''Grava um indice reverso.

    O indice será gravado como um arquivo JSON.

    Args:
        filename: nome do arquivo.
        index: dicionario que mapeia palavra para uma lista de docids.
    '''
    with open(filename, 'w') as file_index:
        json.dump(index, file_index, indent=4)
