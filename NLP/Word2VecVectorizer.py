from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
import math
import re


class Word2VecSimple:
	def __init__(self, min_count=1, size=50, window=4, vectorization_function="maxmin"):

		self.min_count = min_count
		self.size = size
		self.window = window
		self.vectorization_function = vectorization_function
		self.normalize = True

	def fit(self, corpus):
		a = self.get_doc2vec_all_corpus(corpus)

		# For fast lookup create a dictionary of words
		self.vocabs = dict()
		for i in self.model.wv.vocab:
			self.vocabs[i.lower()] = i

		# Normalize prior any query:
		self.normalized_model = []
		self.word_index_dict = dict()
		indeces = 0
		for word in self.model.wv.vocab:
			self.word_index_dict[word] = indeces
			indeces = indeces + 1
			self.normalized_model.append(self.model[word])

		# Scaling:
		self.normalized_model = np.array(self.normalized_model)
		self.normalized_model = np.apply_along_axis(scaling, axis=0, arr=self.normalized_model)
		self.normalized_model = self.normalized_model.tolist()
		# Normalizing:
		#   w = csr_matrix(np.asarray(self.normalized_model))
		#   self.normalized_model = normalize(w, norm='l1', axis=0)
		#   self.normalized_model = self.normalized_model.todense().tolist()
		#   print(self.normalized_model[:,26:])
		print("Finish model")

	def transform(self, corpus):
		if self.model is None:
			print("model was not created. Please call fit method before transform. Exiting!")
			exit()

		vectorization = []
		for document in corpus:
			# Process the document
			alphanumeric_document = re.sub('[^0-9a-zA-Z ]+', ' ', document)
			doc_dictionary = dict()
			data = ' '.join(alphanumeric_document.split(' ')).split(' ')
			for word in data:
				doc_dictionary[word.lower()] = True
			# Finish process the document

			words_factors_list_of_lists = []

			# for word in doc_dictionary:
			#  if word.lower() in self.vocabs:
			#    words_factors_list_of_lists.append(self.model[self.vocabs[word.lower()]])

			for word in doc_dictionary:
				if word.lower() in self.vocabs:
					original_case_word = self.vocabs[word.lower()]
					index_in_normalized_model = self.word_index_dict[original_case_word]
					model_to_append = self.normalized_model[index_in_normalized_model]
					words_factors_list_of_lists.append(model_to_append)

			# for word in self.model.wv.vocab:
			#  if word.lower() in doc_dictionary:
			#    index = self.word_index_dict[word]
			#    words_factors_list_of_lists.append(self.normalized_model[index])

			vectorization_item = self.vectorize_document(words_factors_list_of_lists)
			if vectorization_item is not None:
				vectorization.append(vectorization_item)

		w = csr_matrix(np.asarray(vectorization))
		# return normalize(w, norm='l1', axis=0)
		return w

	# This method creates the model and extract the vectorization in one go. It creates one distinct model per each document.
	# Is different with "fit()" and "transform()" in that in "fit()" and "transform()" the model is created from the beginning based on *all* documents and reused for the transform.
	def fit_and_transform(self, corpus):
		vectorization = []
		for raw_content in corpus:
			words_factors_list_of_lists = self.get_doc2vec(raw_content)
			vectorization_item = self.vectorize_document(words_factors_list_of_lists)
			vectorization.append(vectorization_item)

		w = csr_matrix(np.asarray(vectorization))
		return normalize(w, norm='l1', axis=0)

	def vectorize_document(self, document_words):
		if (self.vectorization_function == 'maxmin'):
			vectorization_item = self.get_doc2vec_maxmin(document_words)
			if vectorization_item is not None:
				return vectorization_item
		elif (self.vectorization_function == 'avg'):
			vectorization_item = self.get_doc2vec_avg(document_words)
			if vectorization_item is not None:
				return vectorization_item
		else:
			vectorization_item = self.get_doc2vec_max(document_words)
			if vectorization_item is not None:
				return vectorization_item
		return None

	def get_doc2vec_avg(self, document_words):
		if document_words is None:
			return None
		# axis = 0 means apply operations across the rows. If arr is n rows x m cols, at end we get 1 row and m columns.
		doc_vec = np.apply_along_axis(get_mean, axis=0, arr=document_words)
		return doc_vec

	def get_doc2vec_maxmin(self, document_words):
		if document_words is None:
			return None
		document_words_array = np.array(document_words)
		if len(document_words_array.shape) == 1 and len(document_words_array) == self.size:
			# In case the document has only one word vector (each vector is size self.size).
			doc_vec = np.append(document_words, document_words)
		elif len(document_words_array.shape) == 1 and len(document_words_array) == 0:
			# In this case, the documents_words is empty
			return None
		else:
			magnitudes = np.apply_along_axis(get_magnitude, axis=1, arr=document_words)
			index_of_max = np.argmax(magnitudes)
			index_of_min = np.argmin(magnitudes)
			doc_vec = np.append(document_words[index_of_max], document_words[index_of_min])

		return doc_vec

	def get_doc2vec_max(self, document_words):
		if document_words is None:
			return None
		document_words_array = np.array(document_words)
		if len(document_words_array.shape) == 1 and len(document_words_array) == self.size:
			# In case the document has only one word vector (each vector is size self.size).
			doc_vec = np.append(document_words, document_words)
		elif len(document_words_array.shape) == 1 and len(document_words_array) == 0:
			# In this case, the documents_words is empty
			return None
		else:
			magnitudes = np.apply_along_axis(get_magnitude, axis=1, arr=document_words)
			index_of_max = np.argmax(magnitudes)
			index_of_min = np.argmin(magnitudes)
			doc_vec = document_words[index_of_max]

		return doc_vec

	def get_doc2vec(self, raw_content):
		alphanumeric_content = re.sub('[^0-9a-zA-Z ]+', ' ', raw_content)

		# maybe add here some stop-word removal if needed ?
		text_file = open("Output.txt", "w")
		text_file.write(alphanumeric_content)
		text_file.close()

		sentences = LineSentence("Output.txt", max_sentence_length=10)
		# print(sentences)

		# Ref: https://radimrehurek.com/gensim/models/word2vec.html
		# min_count = 2
		# size = 50
		# window = 4
		# print(self.min_count)
		# print(self.size)
		# print(self.window)
		try:
			model = Word2Vec(sentences, min_count=self.min_count, size=self.size, window=self.window)
			size_vocab = 0

			words_factors_list_of_lists = []
			for i in model.wv.vocab:
				words_factors_list_of_lists.append(model[i])
			return words_factors_list_of_lists
		except Exception as exception:
			print(exception.args)
			print(alphanumeric_content)
			print(raw_content)
			return None
		# print(model.wv.vocab)

	# This method will create a model considering all sentences of all documents.
	# This is used when classifying the real news with fake news.
	def get_doc2vec_all_corpus(self, corpus):
		print("joining all corpus")
		one_string_corpus = ' '.join(corpus);

		alphanumeric_corpus = re.sub('[^0-9a-zA-Z ]+', ' ', one_string_corpus)

		# maybe add here some stop-word removal if needed ?
		text_file = open("Output.txt", "w")
		text_file.write(alphanumeric_corpus)
		text_file.close()

		sentences = LineSentence("Output.txt", max_sentence_length=10)
		# print(sentences)
		# exit()
		# Ref: https://radimrehurek.com/gensim/models/word2vec.html
		# min_count = 2
		# size = 50
		# window = 4
		# print(self.min_count)
		# print(self.size)
		# print(self.window)
		self.model = None
		try:
			print("building word2vec model");
			self.model = Word2Vec(sentences, min_count=self.min_count, size=self.size, window=self.window, sg=1)

		except Exception as exception:
			print(exception.args)
			print(alphanumeric_content)
			print(raw_content)

		return self.model

	# print(model.wv.vocab)


def get_mean(x):
	return np.mean(x)


def get_magnitude(x):
	return math.sqrt(np.inner(x, x))


def scaling(x):
	maxim = max(x)
	minim = min(x)

	if maxim == minim:
		size = len(x)
		return np.ones(size) * 0.5
	return (x - minim) / (maxim - minim)
