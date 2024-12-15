import numpy as np

class TFIDFVectorizer:
    def __init__(self, query_tokenized, tag_tokenized):

        self.vocabulary = list(set(query_tokenized + tag_tokenized))
        self.tf_vector1 = self.__calculate_tf(query_tokenized, self.vocabulary)
        self.tf_vector2 = self.__calculate_tf(tag_tokenized, self.vocabulary)

        self.idf_vector = self.__calculate_idf(query_tokenized, tag_tokenized, self.vocabulary)
        self.tfidf_vector1 = self.__calculate_tfidf(self.tf_vector1, self.idf_vector)
        self.tfidf_vector2 = self.__calculate_tfidf(self.tf_vector2, self.idf_vector)
    
    def __calculate_tf(self, phrase_token, vocabulary):
        """Calculate the Term Frequency (TF) vector for a phrase."""
        tf_vector = np.zeros(len(vocabulary))
        for i, word in enumerate(vocabulary):
            tf_vector[i] = phrase_token.count(word)
        return tf_vector

    def __calculate_idf(self, phrase1_tokens, phrase2_tokens, vocabulary):
        """Calculate the Inverse Document Frequency (IDF) vector for the vocabulary."""
        num_documents = 2
        idf_vector = np.zeros(len(vocabulary))
        for i, word in enumerate(vocabulary):
            # Count the number of documents containing the word
            doc_count = 0
            if word in phrase1_tokens:
                doc_count += 1
            if word in phrase2_tokens:
                doc_count += 1
            # Compute IDF using log formula
            idf_vector[i] = np.log((num_documents + 1) / (doc_count + 1)) + 1
        return idf_vector

    def __calculate_tfidf(self, tf_vector, idf_vector):
        """Calculate the TF-IDF vector by multiplying TF and IDF vectors."""
        return tf_vector * idf_vector
    
    def vectorize(self):
        return self.tfidf_vector1, self.tfidf_vector2


    



class CosineSimilarity:
    def __init__(self, query_vector, tag_vector) -> None:
        self.query_vector = query_vector 
        self.tag_vector = tag_vector 

    def cosine_similarity(self):
        dot_product = np.dot(self.query_vector, self.tag_vector)
        norm_vec1 = np.linalg.norm(self.query_vector)
        norm_vec2 = np.linalg.norm(self.tag_vector)
        __value = dot_product / (norm_vec1 * norm_vec2) if (norm_vec1 != 0 and norm_vec2 != 0) else 0.0

        return __value



