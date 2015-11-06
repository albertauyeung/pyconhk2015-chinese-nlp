# -*- coding: utf-8 -*-
# ###########################################################################
import codecs
import sys
from gensim import corpora, models, similarities
from gensim.models import Word2Vec

infname = "docs.txt"
infile = codecs.open(infname, "r", "utf-8")

# Read word-segmented documents from file
lines = infile.readlines()
documents = []
for l in lines:
    words = l.strip().split(" ")
    documents.append(words)

# Build dictionary
dictionary = corpora.Dictionary(documents)
dictionary.filter_extremes(no_below=5)

# Build a corpus of bag-of-words using the dictionary
corpus = [ dictionary.doc2bow(d) for d in documents ]

# Generate the TF-IDF transformation
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# Train the LSI model using the TF-IDF transformed corpus
lsi = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=200)
corpus_lsi = lsi[corpus_tfidf]

# Create a similarity index
index = similarities.MatrixSimilarity(corpus_lsi)

# Query the index for similar documents for document ID 40
sims = index[lsi[tfidf[corpus[40]]]]
sims = sorted(enumerate(sims), key=lambda item: -item[1])

# Generate word vectors using the Word2vec algorithm
model = Word2Vec(documents, size=200, window=5, min_count=5, workers=4)
