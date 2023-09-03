from random import shuffle
import mysql.connector
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch, string, random
import os
from config import *
import re


db_conn = mysql.connector.connect(database=database['database'], user="root", password=database['password'], host="localhost", port="3306")
code_directory = os.path.dirname(os.path.abspath(__file__))
model_directory = os.path.join(code_directory, "model")


def user(user_id):
    chosen_pref = db_conn.cursor()
    query = 'SELECT Content FROM content WHERE UserID = %s'
    chosen_pref.execute(query, (user_id,))
    # category.close()
    category = list(chosen_pref)
    chosen_pref.close()
    pref = category[0][0]
    cursor = db_conn.cursor()
    query = "SELECT QuestionID FROM question WHERE Answered = 0 AND Category = %s"
    cursor.execute(query, (pref,))
    matched_requests = [row[0] for row in cursor]
    cursor.close()
    return matched_requests


def check_text(tokenizer, device, list_ABC, model, text, list_label, shuffle=False): 
    list_label = [x+'.' if x[-1] != '.' else x for x in list_label]
    list_label_new = list_label + [tokenizer.pad_token]* (20 - len(list_label))
    if shuffle: 
        random.shuffle(list_label_new)
    s_option = ' '.join(['('+list_ABC[i]+') '+list_label_new[i] for i in range(len(list_label_new))])
    text = f'{s_option} {tokenizer.sep_token} {text}'

    model.to(device).eval()
    encoding = tokenizer([text],truncation=True, max_length=512,return_tensors='pt')
    item = {key: val.to(device) for key, val in encoding.items()}
    logits = model(**item).logits
    
    logits = logits if shuffle else logits[:,0:len(list_label)]
    probs = torch.nn.functional.softmax(logits, dim = -1).tolist()
    predictions = torch.argmax(logits, dim=-1).item() 
    probabilities = [round(x,5) for x in probs[0]]

    return f'prediction:    {predictions} => ({list_ABC[predictions]}) {list_label_new[predictions]} \n probability:   {round(probabilities[predictions]*100,2)}%'

def assistance(text):
    tokenizer = AutoTokenizer.from_pretrained(model_directory)
    model = AutoModelForSequenceClassification.from_pretrained(model_directory)

    list_label = 'health_and_fitness, technology_and_gadgets, science_and_research, business_and_finance, travel_and_adventure, food_and_cooking, sports_and_recreation, arts_and_culture, education_and_learning, environment_and_sustainability, politics_and_government, history_and_archaeology, fashion_and_style, music_and_entertainment, books_and_literature, movies_and_tv_shows, home_and_interior_design, parenting_and_childcare, relationships_and_dating, self_improvement_and_personal_development'.split(',')
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    list_ABC = [x for x in string.ascii_uppercase]
    return check_text(tokenizer, device, list_ABC, model, text, list_label)

# def extract_prediction_values(prediction_string):
#     match = re.search(r'prediction: (\d+) => \(C\) (.+)\.\n probability: (\d+\.\d+)%', prediction_string)
#     category_index = match.group(1)
#     category_name = match.group(2)
#     probability = match.group(3)

#     value = (category_name.strip(), probability)
#     return value
