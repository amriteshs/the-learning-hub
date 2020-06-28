from app import *
from app.models.db import *
import json
import random
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField
from flask_bootstrap import Bootstrap
from datetime import datetime
import numpy as np
import base64
import uuid


class NameForm(Form):
    name = TextField('Name:')


# add a new comment into comments table
@app.route('/comments/<id>', methods = ["GET","POST"])
def comments(id):
    """
    This is the comments API
    Call this api to get or post comments
    ---
    tags:
      - API to get or post comments
    get:
      parameters:
        - name: data_id
          in: path
          type: string
          required: true
          description: The data ID
    post:
      parameters:
        - name: data_id
          in: path
          type: string
          required: true
          description: The data ID
        - name: name
          in: body
          type: string
          required: true
          description: The comment desc
          schema:
            properties:
              name:
                type: string
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: leader_boards_reply
          properties:
            first_name:
                type: string
            last_name:
                type: string
            comment_desc:
                type: string
            time_stamp:
                type: object
            rating:
                type: string


    """

    if request.method == 'POST':
        user_id = 37 # for anonymous user
        name = request.form['name']

        # insert a new comment into comments table
        query1 = f"INSERT INTO public.comments (data_id, user_id, rating, comment_desc,time_stamp) VALUES({id},'37','0','{name}','now');"
        reply1 = insert_query(query1)

    form = NameForm(request.form)

    # query to fetch data from comments table by comment_id
    query1 = f"SELECT u.first_name,u.last_name,c.comment_desc,c.time_stamp,c.rating FROM public.comments as c INNER JOIN public.user_ as u ON u.id=c.user_id WHERE c.data_id = '{id}'"
    data = execute_query(query1)

    for i in data:
        data[3] = datetime.fromtimestamp(data[3])

    return (form,data)


# get dataset details for the specified dataset
@app.route('/dataset_API/<id>', methods = ["GET"])
def get_dataset(id):
    """
    This is the get dataset API
    Call this api passing a dataset id and get back its content
    ---
    tags:
      - API to get dataset
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The dataset ID
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: dataset_reply
          properties:
            dataset_id:
                type: string
            catogery_id:
                type: string
            category:
                type: string
            name:
                type: string
            discription:
                type: string
            dataset_owner:
                type: string
            uploader:
                type: string
            last_update:
                type: string
            link_to_api:
                type: string
            search_tags:
                type: string
            learning_tags:
                type: string
            file_format:
                type: string
            file_patch:
                type: string
            visualisation_link:
                type: string
            status:
                type: string

    """

    # query to fetch dataset details from dataset table by dataset_id
    query = f"SELECT id, catogery_id, category, name, discription, dataset_owner, uploader, last_update, link_to_api, search_tags, learning_tags, file_format, file_patch, visualisation_link, status FROM public.dataset where id = '{id}';"
    data = execute_query(query)

    # store fetched data in dictionary
    reply = {}
    if data:
        reply['dataset_id'] = data[0][0]
        reply['catogery_id'] = data[0][1]
        reply['category'] = data[0][2]
        reply['name'] = data[0][3]
        reply['discription'] = data[0][4]
        reply['dataset_owner'] = data[0][5]
        reply['uploader'] = data[0][6]
        reply['last_update'] = data[0][7]
        reply['link_to_api'] = data[0][8]
        reply['search_tags'] = data[0][9]
        reply['learning_tags'] = data[0][10]
        reply['file_format'] = data[0][11]
        reply['file_patch'] = data[0][12]
        reply['visualisation_link'] = data[0][13]
        reply['status'] = data[0][14]

        # return data as json object
        return json.dumps(reply)

    return json.dumps({})





# add a new dataset into the dataset table
def insert_dataset(data):
    id = int(uuid.uuid4()) % 2147483647

    # query to insert dataset with its details into dataset table
    query = f"INSERT INTO public.dataset (catogery_id, category, name, \
	discription, dataset_owner, uploader, last_update,\
	 link_to_api, search_tags, learning_tags, file_format,\
	  file_patch, visualisation_link, status, upvote, downvote) VALUES('', '{data['category']}', '{data['name']}',\
	   '{data['discription']}', '{data['dataset_owner']}', '{data['uploader']}', '{data['last_update']}',\
	    '{data['link_to_api']}', '{data['search_tags']}', '{data['learning_tags']}',\
	     '{data['file_format']}', '{data['file_patch']}', '{data['visualisation_link']}', '0', 0, 0);"

    # return status response as success or failure
    reply = insert_query(query)
    if reply == 'success':
        return {"status" : 'success'}
    else:
        return {"status" : 'fail'}


# get datasets pending approval from admin
@app.route('/unapproved_dataset', methods = ["GET"])
def unapproved_dataset():
    """
    This is the get unapproved dataset API
    Call this api to get unapproved dataset
    ---
    tags:
      - API to get unapproved dataset
    responses:
      400:
        description: Error
      200:
        description: Success
        schema:
          id: unapproved_dataset_reply
          properties:
            dataset_id:
                type: string
            catogery_id:
                type: string
            category:
                type: string
            name:
                type: string
            discription:
                type: string
            dataset_owner:
                type: string
            uploader:
                type: string
            last_update:
                type: string
            link_to_api:
                type: string
            search_tags:
                type: string
            learning_tags:
                type: string
            file_format:
                type: string
            file_patch:
                type: string
            visualisation_link:
                type: string
            status:
                type: string

    """

    if request.method == "GET":
        # query to fetch dataset details where status = 0 (unapproved)
        query = f"SELECT id, catogery_id, category, name, discription, dataset_owner, uploader, last_update, link_to_api, search_tags, learning_tags, file_format, file_patch, visualisation_link, status, upvote, downvote FROM public.dataset where status = '0';"
        data = execute_query(query)
        if data:
            # store fetched data in dictionary
            reply = {}
            i = 0
            for val in data:
                temp = {}
                temp['dataset_id'] = val[0]
                temp['catogery_id'] = val[1]
                temp['category'] = val[2]
                temp['name'] = val[3]
                temp['discription'] = val[4]
                temp['dataset_owner'] = val[5]
                temp['uploader'] = val[6]
                temp['last_update'] = val[7]
                temp['link_to_api'] = val[8]
                temp['search_tags'] = val[9]
                temp['learning_tags'] = val[10]
                temp['file_format'] = val[11]
                temp['file_patch'] = val[12]
                temp['visualisation_link'] = val[13]
                temp['status'] = val[14]
                temp['upvote'] = val[15]
                temp['downvote'] = val[16]
                reply[i] = temp
                i += 1

            # return data as json object
            return json.dumps(reply), 200

        return json.dumps({}), 400


# get datasets that have been approved by admin
@app.route('/approved_dataset', methods = ["GET"])
def approved_dataset():
    """
    This is the get approved dataset API
    Call this api to get approved dataset
    ---
    tags:
      - API to get approved dataset
    responses:
      400:
        description: Error
      200:
        description: Success
        schema:
          id: approved_dataset_reply
          properties:
            dataset_id:
                type: string
            name:
                type: string
            upvote:
                type: string
            downvote:
                type: string

    """

    if request.method == "GET":
        # query to fetch dataset details where status = 1 (approved)
        query = f"SELECT id, name, upvote, downvote FROM public.dataset where status = '1';"
        data = execute_query(query)

        if data:
            # store fetched data in dictionary
            reply = {}
            i = 0
            for val in data:
                temp = {}
                temp['dataset_id'] = val[0]
                temp['name'] = val[1]
                temp['upvote'] = val[2]
                temp['downvote'] = val[3]
                reply[i] = temp
                i += 1

            # return data as json object
            return json.dumps(reply), 200
        return json.dumps({}), 400


# allow admin to approve or delete an unapproved dataset
@app.route('/approve_dataset', methods = ["POST"])
def approve_dataset():
    """
    This is the approve dataset API
    Call this api to approve dataset
    ---
    tags:
      - API to approve dataset
    parameters:
      - name: data
        in: body
        type: string
        required: true
        description: The approve data
        schema:
          properties:
            id:
                type: integer
            action:
                type: string
                default: "approve"
    responses:
      400:
        description: fail
      200:
        description: success

    """

    if request.method == "POST":
        data = json.loads((request.data).decode())
        if data['action'] == 'approve':
            # update dataset's status to 1 (approved)
            query = f"UPDATE public.dataset SET status = '1' WHERE id = '{data['id']}'"
        else:
            # delete dataset from table
            query = f"DELETE FROM public.dataset WHERE id = '{data['id']}'"

        result = insert_query(query)
        if result == 'success':
            reply = {"status" : "success"}
        else:
            reply = {"status" : "fail"}

        # return status response as success or failure
        return json.dumps(reply)


# search for datasets according to user's search term
@app.route('/search_dataset/<search_term>', methods = ["GET"])
def search_dataset(search_term):
    """
    This is the search dataset API
    Call this api to search dataset
    ---
    tags:
      - API to search dataset
    parameters:
      - name: search_term
        in: path
        type: string
        required: true
        description: The search term
    responses:
      500:
        description:
      400:
        description: fail
      200:
        description: success
        schema:
          id: search_dataset_reply
          properties:
            dataset_id:
                type: string
            catogery_id:
                type: string
            category:
                type: string
            name:
                type: string
            discription:
                type: string
            dataset_owner:
                type: string
            uploader:
                type: string
            last_update:
                type: string
            link_to_api:
                type: string
            search_tags:
                type: string
            learning_tags:
                type: string
            file_format:
                type: string
            file_patch:
                type: string
            visualisation_link:
                type: string
            status:
                type: string

    """

    if request.method == "GET":

        # query to fetch dataset details where search term is present in a dataset table row
        query = f"SELECT id, catogery_id, category, name, discription, dataset_owner, uploader, last_update, link_to_api, search_tags, learning_tags, file_format, file_patch, visualisation_link, status FROM public.dataset where search_tags ilike '%{search_term}%' or name ilike '%{search_term}%' or category ilike '%{search_term}%' or discription ilike '%{search_term}%';"
        db_data = execute_query(query)

        if db_data:
            # query to store fetched data in dictionary
            reply = {}
            i = 0
            for val in db_data:
                temp = {}
                temp['dataset_id'] = val[0]
                temp['catogery_id'] = val[1]
                temp['category'] = val[2]
                temp['name'] = val[3]
                temp['discription'] = val[4]
                temp['dataset_owner'] = val[5]
                temp['uploader'] = val[6]
                temp['last_update'] = val[7]
                temp['link_to_api'] = val[8]
                temp['search_tags'] = val[9]
                temp['learning_tags'] = val[10]
                temp['file_format'] = val[11]
                temp['file_patch'] = val[12]
                temp['visualisation_link'] = val[13]
                temp['status'] = val[14]
                reply[i] = temp
                i += 1

            # return data as json object
            return json.dumps(reply), 200

        return json.dumps({}), 200

    return '', 500


# get upvote, downvote count for the specified dataset
@app.route('/get_votes/<id>', methods = ["GET"])
def get_votes(id):
    """
    This is the get votes API
    Call this api to get votes
    ---
    tags:
      - API to get votes
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The dataset ID
    responses:
      400:
        description: fail
      200:
        description: success
        schema:
          id: get_votes_reply
          properties:
            upvote:
                type: integer
            downvote:
                type: integer

    """

    if request.method == 'GET':

        # query to fetch upvote, downvote count from the dataset table by dataset_id
        query = f"select upvote, downvote from public.dataset where id = '{id}'"
        data = execute_query(query)

        # store fetched data in dicionary and return it as json object
        return json.dumps({'upvote' : int(data[0][0]), 'downvote' : int(data[0][1])})


# allow user to upvote or downvote a dataset
@app.route('/add_votes', methods = ["POST"])
def add_votes():
    """
    This is the get votes API
    Call this api to get votes
    ---
    tags:
      - API to get votes
    parameters:
      - name: id
        in: body
        type: string
        required: true
        description: The dataset ID
        schema:
          properties:
            id:
                type: integer
            upvote:
                type: string
            downvote:
                type: string
    responses:
      400:
        description: fail
      200:
        description: success

    """

    if request.method == 'POST':
        data = json.loads((request.data).decode())

        # query to update upvote, downvote count for the specified dataset
        id_ = data['id']
        upvote = int(data['upvote'])
        downvote = int(data['downvote'])
        query = f"UPDATE public.dataset SET upvote={upvote}, downvote={downvote} where id = '{id_}';"
        result = insert_query(query)

        # return status response as success or failure
        if result == 'success':
            return json.dumps({'status' : 'success'}), 200

        return json.dumps({'status' : 'fail'}), 400
