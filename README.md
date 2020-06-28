## The Learning Hub

## To install the dependencies

Before running the actual code, navigate to the project directory and install all libraries used in the module using the following command:

``` pip3 install -r requirements.txt ```

## To run the code

Type the following command to run the code:

``` python3 run.py ```

and open http://127.0.0.1:5000/ in the browser of your preference.

## Admin login details

Email: admin@gmail.com  
Password: admin


## Database access (Postgres Database is hosted on Microsoft Azure)
1. Hostname: comp9323.postgres.database.azure.com
2. User: comp9323_admin@comp9323
3. Database: postgres
4. Password: password_123

Type the following command in terminal to connect to the database:  
```psql -h comp9323.postgres.database.azure.com -d postgres -U comp9323_admin@comp9323```

## Swagger endpoint access

After running the app, open http://127.0.0.1:5000/apidocs/index.html

## Hosted app access

The app is hosted on Heroku and can be accessed using the following link:  
https://the-learning-hub.herokuapp.com

## Instructions to use main features
A. Sign up
	
	1. From homepage, click log-in sign up
	2. Click Login/Signup in navigation bar
	3. Click "To Create an account click here"
	4. Fill up required details and click sign up
	
B. User Login
	
	Note: Log in required to upload dataset and answer learning activities
	1. From homepage, click log-in sign up
	2. Click Login/Signup in navigation bar
	3. Enter username and password and click log in
	
C. Admin Login
	
	Note: Admin Log in required to approve and delete datasets.
	1. From homepage, click admin
	3. Enter username: "admin@gmail.com" and password: "admin" and click log in
	
D. Access Learning Content
	
	1.1 From homepage, Search learning content using searchbox and click "Search Learning" Button. 
		Choose learning content you want to choose from search results
		
	 	Alternatively you can select learning content by skill level in the Learning Activities section of the homepage
	
	2. From the selected Learning Content page you can:
		- View basic description about the learning content
		- Watch Learning Content
		- Answer Learning Activities
			Note: Log in required
				  Scores of each learning activity is visible in user's profile. 
				  Top scores are posted in the leaderboard section of the hompege.
		- Provide comments in the comment section
		    Note: Log in required
			
C. Access Datasets
	
	1.1 From homepage, Search dataset using searchbox and click "Search Datasets" Button. 
		Choose dataset you want to choose from search results
		
		Alternatively you can select dataset by category in the Dataset section of the homepage
		
	2. From the selected Dataset page you can:
		- View metadata of the dataset 
		- Rate Dataset
		- See basic visualisation preview of the chart
		- Create visualisations and download data by clicking on the "Edit Chart" under the sample visualisation
		- Answer Learning Activities
		- Provide comments in the comment section
		     Note: Log in required

D. Upload Dataset
	
	Note: Have to be logged in to use this feature
	1. Select Add dataset in the navigation bar
	2. Complete details of form
		Note:
			- A shareable plotly share studio link is required to show the visualisation and allow users to download data
			-Datasets are marked "Unapproved" until admin does sanity check and approves

E. View Profile
	
	Note: Have to be logged in to use this feature
	1. Click Profile name in nav bar and select view profile
	2. To view score for each learning activty, select the dropdown box

F. Approve/Delete Dataset

	Note: Have to be logged in as admin to use this feature
	1. Log in as admin
	2. To preview the dataset, select one of the datasets in the approve/unapprove table to see more details of the dataset
	3. From the dataset preview, you can select "approve" to approve an unapproved dataset or "delete" to delete the dataset in the system.
	
G. Chatbot
	
	1. Chatbot is available by clicking the blue message icon hovered at the bottom right corner of the homepage
	2. Chatbot is built to create a natural dialogue with the user and detects the below intent
		a. Greeting (Eg., Hi)
		b. Search Datasets (Eg., Search for datasets)
		c. Recommend learning (Eg., Recommend learning)
		d. Provide Data Science information (Eg., What is classification?)


## Notes

1. Rasa will throw Tensorflow deprecation warnings while loading the model for chatbot. These can be ignored.
2. The response time for app may be slow as the database is hosted. In case of any difficulties, please check the hosted app.
3. The dump of the database is provided in the file mydb.dump
4. The main REST API operations are inside ./app/models and ./app/views.py
5. The front end files are inside ./app/templates and static files are inside ./app/extra
6. If the bot gets stuck, you can say 'hi' to reset the state of the bot.
