from app import *
from app.models.db import *
import json
import random
from app.models.user import *


# get learning content for the specified learning_id
@app.route('/learning_API/<learning_id>', methods = ["GET"])
def get_content(learning_id):
    """
    This is the get learning content API
    Call this api passing a learning id and get back its content
    ---
    tags:
      - API to get learning content
    parameters:
      - name: learning_id
        in: path
        type: integer
        required: true
        description: The learning ID
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: learning_content_reply
          properties:
            learning_id:
                type: string
            name:
                type: string
            skill_level:
                type: string
            topic_id:
                type: string
            topic:
                type: string
            tags:
                type: string
            link_to_video:
                type: string
            description:
                type: string

    """

    result = {}

    # query to fetch data from learning_content table by id
    query = f"SELECT * FROM learning_content WHERE id = {learning_id};"
    data = execute_query(query)

    # store fetched data in dictionary
    if data:
        result['learning_id'] = data[0][0]
        result['name'] = data[0][1]
        result['skill_level'] = data[0][2]
        result['topic_id'] = data[0][3]
        result['topic'] = data[0][4]
        result['tags'] = data[0][5]
        result['link_to_video'] = '/'.join(data[0][6].split(';')[0].split('/')[:-1]) + '/preview'
        result['description'] = data[0][7]

    # return data as a json object
    return json.dumps(result)


# search for learning content according to the entered search term
@app.route('/search_learning_activity/<search_term>', methods = ["GET"])
def search_learning_activity(search_term):
    """
    This is the search learning activity content API
    Call this api passing a search term and get back its result
    ---
    tags:
      - API to search learning activity
    parameters:
      - name: search_term
        in: path
        type: string
        required: true
        description: The search term
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: learning_search_reply
          properties:
            id:
                type: string
            name:
                type: string
            description:
                type: string

    """
    
    if request.method == "GET":

        # query to fetch data from learning_content table by tags that match the entered search term
        query = f"select id, name, description from public.learning_content\
        where tags ilike '%{search_term}%'"
        data = execute_query(query)

        if data:
            reply = {}
            i = 0

            # store fetched data in dictionary
            for vals in data:
                temp = {'id' : vals[0], 'name' : vals[1], 'description' : vals[2]}
                reply[i] = temp
                i += 1

            # return data as a json object
            return json.dumps(reply)

        return json.dumps({})


# get learning activity for the specified learning_id
@app.route('/activity_API/<learning_content_id>', methods = ["GET"])
def get_activity(learning_content_id):
    # query to fetch data from learning_activity table by learning_content_id
    query = f"SELECT id, activity_name, QNA FROM learning_activity \
    WHERE learning_content_id = {learning_content_id};"
    data = execute_query(query)

    # store fetched data in dictionary
    result = {}
    if data:
        result['activity_id'] = data[0][0]
        result['activity_name'] = data[0][1]
        result['QNA'] = data[0][2]

        # return data as a json object
        return json.dumps(result)

    return json.dumps({})


# store user score for the specified learning activity
@app.route('/upload_score', methods = ["POST"])
def upload_score():
    """
    This is the upload score API
    Call this api to upload score
    ---
    tags:
      - API to upload score
    parameters:
      - name: activity_id
        in: body
        type: integer
        required: true
        description: The activity ID
        schema:
          properties:
            activity_id:
              type: integer
            score:
              type: integer
    responses:
      400:
        description: fail
      200:
        description: success
        schema:
          id: upload_score_reply
          properties:
            status:
                type: string
                default: ["success", "fail"]

    """

    if request.method == "POST":
        data = json.loads((request.data).decode())
        user = json.loads(get_user())
        id = random.randint(0,10) + random.randint(10,100)

        # delete the previous score in the score table for the specified activity_id
        activity_id = data['activity_id']
        insert_query(f"DELETE FROM public.score WHERE activity_id = {activity_id} and user_id = {user}")

        # insert the new score in the score table for the same activity_id
        score = data['score']
        query = f"INSERT INTO score (id, score, activity_id, user_id) \
        VALUES ({id}, {score}, {activity_id}, {user['user_id']});"
        reply = insert_query(query)

        # return success or failure status according to the reply
        if reply == 'success':
            return json.dumps({"status" : 'success'}), 200
        else:
            return json.dumps({"status" : 'fail'}), 400



# get user's scores for the activities in different learning contents
@app.route('/get_score', methods = ["GET"])
def get_score():
    """
    This is the get score API
    Call this api to get a score
    ---
    tags:
      - API to get score
    parameters:
      - name: activity_id
        in: path
        type: integer
        required: true
        description: The activity ID
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: get_score_reply
          properties:
            learning_name:
                type: integer

    """
    
    if request.method == "GET":
        # query to fetch data from score table by user_id
        user = json.loads(get_user())
        user_id = user['user_id']
        query = f"select * from public.score where user_id = '{user_id}'"
        data = execute_query(query)

        if data:
            # query to fetch content name from learning_content table by learning_id
            reply = {}
            for vals in data:
                query = f'select name from public.learning_content where id = {vals[2]}'
                temp = execute_query(query)
                if temp:
                    reply[f'{temp[0][0]}'] = vals[1]

            # return data as json object
            return json.dumps(reply), 200

        return json.dumps([]), 200


# display user leaderboard in descending order of cumulative scores
@app.route('/leader_boards', methods = ["GET"])
def leader_boards():
    """
    This is the leader boards API
    Call this api to get leader boards
    ---
    tags:
      - API to get leader boards
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: leader_boards_reply
          properties:
            reply_id:
                type: array
                items:
                    oneOf:
                      - type: integer
                      - type: string
                      - type: string

    """
    
    if request.method == "GET":
        # query to fetch all data from score table
        query = 'select * from public.score'
        data = execute_query(query)

        # calculate cumulative scores for each user
        scores = {}
        for vals in data:
            if vals[3] in scores:
                scores[vals[3]] += vals[1]
            else:
                scores[vals[3]] = vals[1]

        # get user details from user table for each user
        final_scores = []
        for v, k in scores.items():
            query = f"select first_name, last_name from public.user_ where id = '{v}'"
            users = execute_query(query)
            final_scores.append([k, users[0][0], users[0][1]])

        # sort users in descending order of their final scores
        final_scores = sorted(final_scores, key=lambda x: x[0], reverse = True)
        final_scores = final_scores[:11]

        i = 1
        reply = {}
        for vals in final_scores:
            reply[i] = vals
            i += 1

        # return data as json object
        return json.dumps(reply), 200
