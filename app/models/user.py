from app import *
from app.models.db import *
import json


# get a user's details
@app.route('/user', methods = ["POST"])
def get_user():
    """
    This is the get user API
    Call this api to get user information
    ---
    tags:
      - API to get user information
    responses:
      500:
        description: Error
      200:
        description: Success
        schema:
          id: user_reply
          properties:
            first_name:
              type: string
            last_name:
              type: string
            email:
              type: string
            user_id:
              type: integer

    """
    
    # get current user's id
    id = current_user.get_id()
    if id:
        reply = {}
        
        # query to fetch user details for the specified user_id
        query = f"select first_name, last_name, email,id from user_ where id = '{id}'"
        data = execute_query(query)
        
        # store fetched data in dictionary
        if data:
            reply['first_name'] = data[0][0]
            reply['last_name'] = data[0][1]
            reply['email'] = data[0][2]
            reply['user_id'] = data[0][3]
            
        # return data as json object
        return json.dumps(reply)
        
    return json.dumps({})
