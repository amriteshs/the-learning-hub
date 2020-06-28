from rasa.nlu.model import Interpreter
from app import *
from app.models.db import *
import json
import random
import wikipediaapi
import wikipedia


interpreter = None
entered_learning = 0
entered_search = 0
entered_info = 0


@app.before_first_request
def init_models():
	global interpreter
	print("Loading rasa nlu model")
	interpreter = Interpreter.load("./model/nlu")


@app.route('/livechat_back', methods = ['POST'])
def livechat_back():
    """
    This is the livechat API
    Call this api to get livechat response
    ---
    tags:
      - API to get livechat response
    parameters:
      - name: message
        in: body
        type: string
        required: true
        description: The message
        schema:
          properties:
            message:
                type: string
    responses:
      400:
        description: fail
      200:
        description: success
        schema:
          id: livechat_response
          properties:
            reply:
                type: string
            options:
                type: array
            is_link:
                type: integer
            name:
                type: string
            type:
                type: string

    """
    
    global entered_info
    global entered_learning
    global entered_search
    if request.method == "POST":
        reply = json.loads((request.data).decode())
        message = reply['message']
        intent = interpreter.parse(message)
        print(reply)
        intro_text = 'I am a bot, and i can help in recommending learning activities and searching datasets'
        if intent['intent']['name'] == 'greet' and intent['intent']['confidence'] > 0.4:
            entered_learning = 0
            entered_search = 0
            entered_info = 0
            greet_reply = ['hey', 'hello', 'hi', 'hey there']
            re = random.choice(greet_reply) + ', ' + intro_text
            reply = {'reply' : re, 'options' : [], 'is_link' : 0}
            return json.dumps(reply)
        if entered_info == 1:
            reply = message
            wiki = wikipediaapi.Wikipedia('en')
            wikipedia.set_lang('en')
            wikiterm = wikipedia.search(reply)
            if len(wikiterm) > 0:
                page = wiki.page(wikiterm[0])
                reply = page.summary
                entered_info = 0
            else:
                entered_info = 0
                reply = "can you enter the topic for which information is needed"
            return json.dumps({'reply' : reply, 'options' : [], 'is_link' : 0})
        if entered_search == 1:
            query = f"SELECT id, catogery_id, category, name, discription, dataset_owner, uploader, last_update, link_to_api, search_tags, learning_tags, file_format, file_patch, visualisation_link, status FROM public.dataset where search_tags ilike '%{message}%' or name ilike '%{message}%' or category ilike '%{message}%' or discription ilike '%{message}%';"
            data = execute_query(query)
            dataset = []
            name = []
            for vals in data:
                dataset.append("dataset/" + str(vals[0]))
                name.append(vals[3])
            reply = {'reply' : dataset, 'options' : [], 'is_link' : 1, 'name' : name, 'type' : 'searched datasets'}
            entered_search = 0
            return json.dumps(reply)
        if entered_learning == 1:
            if message == 'beginer':
                reply = [0, 3]
            elif message == 'intermediate':
                reply = [2, 5]
            elif message == 'pro':
                reply = [4, 6]
            query = f'Select id, name from public.learning_content where skill_level < {reply[1]} and skill_level > {reply[0]}'
            data = execute_query(query)
            learning = []
            name = []
            for vals in data:
                learning.append("learning/" + str(vals[0]))
                name.append(vals[1])
            reply = {'reply' : learning, 'options' : [], 'is_link' : 1, 'name' : name, 'type' : 'recommended learning activities'}
            entered_learning = 0
            return json.dumps(reply)
        if intent['intent']['name'] == 'get_information' and intent['intent']['confidence'] > 0.6:
            reply = {'reply' : 'what topic do you want to information on?', 'options' : [], 'is_link' : 0}
            entered_info = 1
            return json.dumps(reply)
        if intent['intent']['name'] == 'search_dataset' and intent['intent']['confidence'] > 0.6:
            reply = {'reply' : 'what topic do you want to search for?', 'options' : [], 'is_link' : 0}
            entered_search = 1
            return json.dumps(reply)
        if intent['intent']['name'] == 'recommend_learning' and intent['intent']['confidence'] > 0.6:
            print('entered')
            reply = {'reply' : 'Select difficulty level', 'options' : ['beginer', 'intermediate', 'pro'], 'is_link' : 0}
            entered_learning = 1
            return json.dumps(reply)
        reply = {'reply' : 'Sorry did not understand what you said', 'options' : [], 'is_link' : 0}
        return json.dumps(reply)
