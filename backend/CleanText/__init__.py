import re


class SentTokenize:
    def __init__(self, phrase) -> None:
        self.phrase = phrase

    def _special_char_removal(self):
        algo = re.sub("[^A-Za-z ]", " ", string=self.phrase)
        return algo 
    
    def _text_normalization(self):
        temp = self._special_char_removal() 
        temp = temp.lower().split() 
        return temp
    def get_tokenized_sentence(self):
        temp = self._special_char_removal()
        temp = self._text_normalization()
        return temp 
    def token_to_sent(self):
        temp = self.get_tokenized_sentence()
        sen = ""
        sen = temp[0]
        for i in range(1, len(temp)):
            sen  += " " + temp[i] 
        return sen 
    
class Token_to_Sent:
    def token_to_sent(self, tokenized_sentence):
        temp = tokenized_sentence
        sen = ""
        sen = temp[0]
        for i in range(1, len(temp)):
            sen  += " " + temp[i] 
        return sen 

        
    



