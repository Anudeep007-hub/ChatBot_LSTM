import numpy as np


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


from CleanText import SentTokenize,Token_to_Sent 
from  RemoveStopWords import stopWords_removal
from PorterStemmer import porter_stemmer
from TFIDF import TFIDFVectorizer, CosineSimilarity 
import pickle
import json

loaded_model = load_model('Model_Results_test/my_model.keras')

max_len = 20

# 2. Load the saved tokenizer
with open('Model_Results_test/tokenizer.pkl', 'rb') as f:
    loaded_tokenizer = pickle.load(f)

# 3. Load the classes mapping
with open('Model_Results_test/classes_set.pkl', 'rb') as f:
    loaded_classes_set = pickle.load(f)

print("Model, Tokenizer, and Classes Mapping Loaded!")

# Function to optimize and predict new input
def optimize_phrase(sentence):
    sequences = loaded_tokenizer.texts_to_sequences([sentence])
    padded_sequences = pad_sequences(sequences, maxlen=max_len)
    return padded_sequences


def pipeline(input_phrase):
    obj = SentTokenize(phrase=input_phrase) 
    obj = obj.get_tokenized_sentence() 
    print(f"Tokenized sentence: {obj}")

    obj = stopWords_removal(tokenized_sentence=obj) 
    obj = obj.get_refined_tokeinzed_sentence()
    print(f"After stop words removal: {obj}")

    obj = porter_stemmer(tokenised_phrase=obj)
    obj = obj.get_stemmed_tokens() 
    print(f"After stemming with porters algorithm: {obj}") 
    return obj

def get_predicted_class(sentence):
    refined_sentence = pipeline(input_phrase=sentence)
    ts = Token_to_Sent() 
    optimized_input = optimize_phrase(ts.token_to_sent(tokenized_sentence=refined_sentence))
    prediction = loaded_model.predict(optimized_input)
    predicted_class = loaded_classes_set[np.argmax(prediction)]

    print(f"Predicted Class: {predicted_class}") 
    return predicted_class 

# Load the JSON data
with open('updated_corpus/updated_corpus.json', 'r') as f:
    data = json.load(f) 
    f.close()

# Define a function to find the response for a specific tag
def get_response_for_tag(tag, user_phrase):
    sim_values = []
    # Traverse through all intents to find the matching tag
    for intent in data['intents']:
        if intent['tag'] == tag:
            respone = intent["response"] 
            if type(respone) is list:
                
                for i in respone:
                    user_token = pipeline(input_phrase=user_phrase) 
                    response = pipeline(input_phrase=i)
                    l = TFIDFVectorizer(query_tokenized=user_token, tag_tokenized=response) 
                    l,m = l.vectorize()
                    sim = CosineSimilarity(query_vector=l, tag_vector=m)
                    sim = sim.cosine_similarity()
                    sim_values.append(sim)
                max_index = np.argmax(sim_values)
                    
                return respone[max_index]
            else:
                return intent['response']
    return None  # If tag not found









