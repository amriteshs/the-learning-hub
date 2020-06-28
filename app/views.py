from app import *
from flask import *
import psycopg2
from app.models.user import *
from app.models.dataset import *
from app.models.learning import *
from app.models.questions import *
import requests
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField
from flask_bootstrap import Bootstrap
from datetime import datetime


class NameForm(Form):
    name = TextField('Name:')


# render login page's contents
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return view_profile()

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        check_user = User_.query.filter_by(email=email).first()

        if check_user:
            if check_user.password == password:
                login_user(check_user)

                if 'next' in request.args:
                    qs = request.args['next']

                    return redirect(qs[1:len(qs)-1])

                return view_profile()

            if 'next' in request.args:
                qs = request.args['next']

                return redirect(qs[1:len(qs)-1])

            return render_template('login.html', error="Username or password not found")
        else:
            # if 'next' in request.args:
            #     qs = request.args['next']

            #     return redirect(qs[1:len(qs)-1])

            return render_template('login.html', error="Username or password not found")

    if 'next' in request.args:
            qs = request.args['next']

            return redirect(qs[1:len(qs)-1])

    return render_template('login.html')


# render signup page's contents
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return view_profile()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            New_user = User_(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(New_user)
            db.session.commit()
        except IntegrityError as e:
            db.session().rollback()

            return render_template('signup.html', error="Email already exsist")

        return redirect(url_for("login"))

    return render_template('signup.html')


# render add_dataset page's contents
@app.route('/add_dataset', methods = ['GET', "POST"])
def add_dataset():
    status = ''
    category_list = execute_query(f"SELECT DISTINCT category FROM dataset ORDER BY category;")
    # if request.method == "GET":
    #     return render_template('add_dataset.html', category_list=category_list)

    data = json.loads(get_user())
    if data and request.method == "POST":
        message = []
        message.append(data['first_name'])
        message.append(data['last_name'])
        message.append(data['email'])
        owner_name = data['first_name'] + ' ' + data['last_name']
        dataset_category = request.form.get('category')
        dataset_name = request.form.get('name')
        dataset_discription = request.form.get('discription')
        dataset_owner = request.form.get('owner')
        dataset_lastupdate = request.form.get('update')
        dataset_api = request.form.get('api')
        dataset_stags = request.form.get('search_tags')
        dataset_ltags = request.form.get('learning_tags')
        dataset_format = request.form.get('format')
        dataset_vl = request.form.get('link')

        reply = {
            "category" : dataset_category,
            "name" : dataset_name,
            "discription" : dataset_discription,
            "dataset_owner" : dataset_owner,
            "uploader" : owner_name,
            "last_update" : dataset_lastupdate,
            "link_to_api" : dataset_api,
            "search_tags" : dataset_stags,
            "learning_tags" : dataset_ltags,
            "file_patch" : "",
            "file_format" : dataset_format,
            "visualisation_link" : dataset_vl
        }

        # reply = json.dumps(reply)
        r = insert_dataset(reply)

        if r['status'] == 'success':
            status = "dataset successfully added"
        else:
            status = "error in adding dataset"

        return render_template('add_dataset.html', message = message, status = status, error = '', category_list=category_list)

    if data:
        message = []
        message.append(data['first_name'])
        message.append(data['last_name'])
        message.append(data['email'])

        return render_template('add_dataset.html', message = message, status = status, error = '', category_list = category_list)

    return render_template('add_dataset.html', message = [], status = status, error = 'Please login to add dataset', category_list = category_list)


# render the specified dataset page's contents
@app.route('/dataset/<dataset_id>', methods = ["GET","POST"])
def view_dataset(dataset_id):
    data = json.loads(get_user())

    if request.method == 'POST':
        # get user_id details
        if data:
            user_id = data['user_id']
        else:
            user_id = 37
        name = request.form['name']
        now = str(datetime.now().strftime('%b %d,%Y %H:%M'))
        query2 = f"INSERT INTO public.comments (data_id, user_id, rating, comment_desc,time_stamp) VALUES({dataset_id},'{user_id}','0','{name}','{now}');"
        reply2 = insert_query(query2)

    if data:
        message = []
        message.append(data['first_name'])
        message.append(data['last_name'])
        message.append(data['email'])
        dataset_details = []
        data = json.loads(get_dataset(dataset_id))

        if data:
            for vals in data:
                dataset_details.append(data[vals])
        # get comments
        form = NameForm(request.form)
        query1 = f"SELECT u.first_name,u.last_name,c.comment_desc,c.time_stamp,c.rating FROM public.comments as c INNER JOIN public.user_ as u ON u.id=c.user_id WHERE c.data_id = '{dataset_id}'"
        query1_data = execute_query(query1)

        return render_template('dataset.html', message = message, dataset_details = dataset_details,form=form,comments=query1_data)
    dataset_details = []
    data = json.loads(get_dataset(dataset_id))

    if data:
        for vals in data:
            dataset_details.append(data[vals])

    # get comments
    form = NameForm(request.form)
    query1 = f"SELECT u.first_name,u.last_name,c.comment_desc,c.time_stamp,c.rating FROM public.comments as c INNER JOIN public.user_ as u ON u.id=c.user_id WHERE c.data_id = '{dataset_id}'"
    query1_data = execute_query(query1)

    return render_template('dataset.html', message = [], dataset_details = dataset_details,form=form,comments=query1_data)


# render the livechat bot's contents
@app.route('/livechat')
def livechat():
    return render_template('bot.html')


# render the learning page's contents
@app.route('/learning/<learning_id>', methods = ["GET","POST"])
def view_learning(learning_id):
    data = json.loads(get_user())

    if request.method == 'POST':
        # get user_id details
        if data:
            user_id = data['user_id']
        else:
            user_id = 37

        name = request.form['name']
        now = str(datetime.now().strftime('%b %d,%Y %H:%M'))

        query2 = f"INSERT INTO public.comments (learn_id, user_id, rating, comment_desc,time_stamp) VALUES({learning_id},'{user_id}','0','{name}','{now}');"
        reply2 = insert_query(query2)

    if data:
        message = [data['first_name'], data['last_name'], data['email']]
    else:
        message = []

    # get learning content details
    content_details = []
    activity_details = []
    content_data = json.loads(get_content(learning_id))

    if content_data:
        for vals in content_data:
            content_details.append(content_data[vals])

    # get comments
    form = NameForm(request.form)
    query1 = f"SELECT u.first_name,u.last_name,c.comment_desc,c.time_stamp,c.rating FROM public.comments as c INNER JOIN public.user_ as u ON u.id=c.user_id WHERE c.learn_id = '{learning_id}'"
    query1_data = execute_query(query1)

    # get related datasets for the learning content
    tags = [i.lower() for i in content_details[5].split(', ')]
    query2 = f"SELECT id, name, discription FROM dataset WHERE "

    for i in range(len(tags)):
        query2 += f"learning_tags ILIKE \'%{tags[i]}%\'"
        if i == len(tags) - 1:
            query2 += ";"
        else:
            query2 += " OR "
    query2_data = execute_query(query2)

    return render_template('learning.html', message=message, content_details=content_details, form=form, comments=query1_data, related_datasets=query2_data)


# render the admin page's contents
@app.route('/admin', methods = ["GET", "POST"])
def admin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        query = f"select * from public.admin where email = '{email}' and password = '{password}'"
        data = execute_query(query)

        if data:
            return render_template("admin_console.html", message = [])

        return render_template('admin_login.html', error="Username or password not found")

    return render_template('admin_login.html', error="")


# render home page's contents post-search
@app.route('/', methods = ["GET", "POST"])
@app.route('/search', methods = ["GET", "POST"])
def search():
    data = json.loads(get_user())

    query = f'select * from public.learning_content'
    data_learning = execute_query(query)
    level0 = []
    level1 =[]
    level2 = []
    for vals in data_learning:
        if 0 < vals[2] < 3:
            level0.append([vals[0], vals[1]])
        elif 2 < vals[2] < 5:
            level1.append([vals[0], vals[1]])
        elif 4 < vals[2] < 6:
            level2.append([vals[0], vals[1]])

    learning = [level0 ,level1, level2]

    if data:
        message = []
        message.append(data['first_name'])
        message.append(data['last_name'])
        message.append(data['email'])

        return render_template('search.html', message = message, learning = learning)

    return render_template('search.html', message = [], learning = learning)


# logout user
@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for("login"))


# render user's profile page
@app.route('/profile', methods=['GET'])
def view_profile():
    if current_user.is_authenticated:
        data = json.loads(get_user())

        if data:
            message = [data['first_name'], data['last_name'], data['email']]
        else:
            message = []

        return render_template('profile.html', message=message)

    return render_template('login.html', error="You should be logged in to view your profile")
