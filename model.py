from os import name
# from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import torch
from spellchecker import SpellChecker
from onnx_transformers import pipeline
import time
class ourmodel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.spell = SpellChecker()
        # self.model = RobertaForQuestionAnswering.from_pretrained("models")
        # self.tokenizer = RobertaTokenizer.from_pretrained("models")
        self.qa = pipeline("question-answering", model="models",tokenizer = "deepset/roberta-base-squad2", onnx=True)

    def forward(self,nerd_question, user_reply):
        reply_to_user = self.qa(question = nerd_question, context = user_reply)['answer']
        try: 
            reply_to_user  = int(reply_to_user)
        except:
            reply_to_user = self.money_format(reply_to_user)
        return reply_to_user
    
    
    def check_spellings(self,user_reply):
        crct_reply = ""
        user_reply_list = user_reply.split()
        misspelled = self.spell.unknown(user_reply_list)

        for word in user_reply_list:
            if word in misspelled:

                crct_reply = crct_reply + self.spell.correction(word) + " "
            else:
                crct_reply = crct_reply + word + " "
        return crct_reply
    
    def money_format(self, money):
        money_list = money.lower().split()[0:2]
        ignore_list = ['rupees','dollars','bucks']
        needed_list = {'thousand':1000,'hundred':100,'lakh':100000,'lakhs':100000}
        try:
            if(money_list[0][0:-1].isdigit() and money_list[0][-1]=="k"):
                return int(money_list[0][0:-1])*1000
        
            if(money_list[0].isdigit() and (money_list[1] in needed_list.keys()) ):
                return int(money_list[0])*needed_list[money_list[1]]

            if(money_list[0].isdigit() and (money_list[1] in ignore_list) ):
                return int(money_list[0])

        except:
            return "invalid inputs"

        return "invalid inputs"

if __name__ == '__main__':
    model = ourmodel()
    res = model("how much spent?","I have spent 3000 rupees")
    print(res)