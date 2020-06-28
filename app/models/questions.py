from app import *
from app.models.db import *
import json
import random
import os


class question:
	def __init__(self, id_= None, question = None, answer = None, options = None):
		self.id = id_
		self.question = question
		self.answer = answer
		self.options = options


# read the file containing the question set and convert it into the desired format
def build_question_set(file_name):
	question_set = {}
	f = open(file_name, "r")
	files = f.readlines()

	for vals in files:
		vals = vals.replace("\n", "")
		questions = vals.split("	")
		options = questions[-1].split(", ")
		random.shuffle(options)

		q = question(int(questions[0]), questions[1], questions[2], options)
		question_set[int(questions[0])] = q

	return question_set


# get the question set
@app.route('/questions', methods=['POST'])
def questions():
    """
    This is the question set API
    Call this api to get question set
    ---
    tags:
      - API to get question set
    parameters:
      - name: reply
        in: body
        type: string
        required: true
        description: The reply
        schema:
          properties:
            init:
                type: integer
            learning_id:
                type: integer
            question_id:
                type: integer
            question:
                type: string
            answer:
                type: string
            options:
                type: string
    responses:
      400:
        description: fail
      200:
        description: success
        schema:
          id: question_reply
          properties:
            learning_id:
                type: string
            question_id:
                type: string
            question:
                type: string
            answer:
                type: string
            options:
                type: array
                items:
                    type: string
            number_question:
                type: integer

    """

    if request.method == "POST":
        reply = json.loads((request.data).decode())

        if reply['init'] == 1:
            # load the first question from question set initially
            questions = build_question_set(os.path.join(app.config['UPLOAD_FOLDER'],f'question_set{reply["learning_id"]}.tsv')) #used learning id to get question set
            reply = {'learning_id' : reply['learning_id'], 'question_id' : questions[0].id, 'question' : questions[0].question,\
            'answer' : questions[0].answer, 'options' : questions[0].options, 'number_question' : len(questions)}

            return json.dumps(reply)
        else:
            # load the next question from question set (if it exists)
            questions = build_question_set(os.path.join(app.config['UPLOAD_FOLDER'],f'question_set{reply["learning_id"]}.tsv'))

            if reply['question_id'] + 1 in questions:
                reply = {'learning_id': reply['learning_id'], 'question_id' : questions[reply['question_id'] + 1].id, \
				'question' : questions[reply['question_id'] + 1].question,\
				'answer' : questions[reply['question_id'] + 1].answer, 'options' : questions[reply['question_id'] + 1].options}

                return json.dumps(reply)

            return json.dumps({'learning_id' : reply['learning_id'], 'question_id' : '', 'question' : '', 'answer' : '', 'options' : []})
