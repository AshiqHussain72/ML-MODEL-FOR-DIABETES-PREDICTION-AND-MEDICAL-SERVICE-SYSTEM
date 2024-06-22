from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
import random 
from django.db.models import Sum, Count
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import datetime
from django.conf import settings
from django.http import JsonResponse
from .utils import public_key 
from django.db.models import Q
from datetime import datetime
import os
import pickle
base_directory = settings.BASE_DIR
# Get the path to your app directory relative to the base directory
relative_app_path = 'app' 
app_dir = os.path.join(base_directory, relative_app_path)
model_path = app_dir+'/random_forest_model.pkl'
if os.path.exists(model_path):
    try:
        # Load the pickle file
        with open(model_path, 'rb') as f:
            # Attempt to load data from the file
            loaded_data = pickle.load(f)
    except EOFError:
        print("Error: EOFError - Ran out of input. The file may be empty or corrupted.")
    except Exception as e:
        print("Error:", e)
else:
    print("Error: The specified file does not exist.")

def home(request):
	return render(request,'index.html',{})
def register(request):
	if request.method == 'POST':
		name = request.POST.get('username')
		address = request.POST.get('address')
		mobile= request.POST.get('mobile')
		email = request.POST.get('email')
		password = request.POST.get('password')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		country = request.POST.get('country')
		city = request.POST.get('city')
		gender = request.POST.get('gender')
		age = request.POST.get('age')
		zip = request.POST.get('zip')
		crt = Register_Detail.objects.create(name=name,
		address=address,mobile=mobile,password=password,email=email,fname=fname,lname=lname,
		city=city,country=country,zip=zip,gender=gender,age=age)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})
def dashboard(request):
	return render(request,'dashboard.html',{})
def user_login(request):
	if request.session.has_key('username'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Register_Detail.objects.filter(email=username,password=password)
			if post:
				username = request.POST.get('username')
				request.session['username'] = username
				a = request.session['username']
				sess = Register_Detail.objects.only('id').get(email=a).id
				user_detail = Register_Detail.objects.get(id=int(sess))
				request.session['age'] = user_detail.age
				request.session['gender'] = user_detail.gender
				request.session['user_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'login.html',{})
def logout(request):
	try:
		del request.session['username']
		del request.session['user_id']
		del request.session['gender']
		del request.session['age']
	except:
		pass
	return render(request, 'login.html', {})
from .utils import generate_fernet_key  # Import the public_key function

def add_post(request):
	user_id=request.session['user_id']
	if request.method == 'POST':
		title=request.POST.get('title')
		description=request.POST.get('description')
		age=request.POST.get('age')
		gender=request.POST.get('gender')
		uid=Register_Detail.objects.get(id=int(user_id))
		key_value = public_key(20)
		prt = Post.objects.create(title=title,description=description,
		user_id=uid,description_key=generate_fernet_key(),gender=gender,age=age)
		if prt:
			messages.success(request,'Post Added Successfully')
	return render(request,'add_post.html',{})
def post(request):
	user_id=request.session['user_id']
	if request.session.has_key('username'):
		detail=Post.objects.filter(user_id=int(user_id))
		return render(request,'post.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def generate_key_post(request,pk):
	if request.session.has_key('username'):
		ids =Post.objects.filter(id=pk)
		email=request.session['username']
		post_id = Post.objects.get(id=pk)
		key_value = post_id.description_key
		recipient_list = [email]
		email_from = settings.EMAIL_HOST_USER
		b = EmailMessage('Your Secret Key To View Post',
		'Secret Key:  ' + key_value  ,email_from,recipient_list).send()
		if request.method == 'POST':
			skey = request.POST.get('skey')
			detail=Post.objects.filter(description_key=skey,id=pk)
			if detail:
				return render(request,'generate_key_post.html',{'detail':detail,'ids':ids})
			else:
				messages.success(request,'You Have Entered Wrong Key')
		return render(request,'generate_key_post.html',{'ids':ids})
	else:
		return render(request,'login.html',{})
def delete(request,pk):
	a=Post.objects.filter(id=pk).delete()
	return redirect('post')
def all_post(request):
	if request.session.has_key('username'):
		detail=Post.objects.all().order_by('-id')
		cursor = connection.cursor()
		post = ''' SELECT Count(app_feedback.comment) from app_feedback 
		GROUP BY app_feedback.post_id_id '''
		sub = cursor.execute(post)
		row = cursor.fetchall()
		post1 = ''' SELECT Count(app_post_feedback.like_post) from app_post_feedback 
		where app_post_feedback.like_post='Yes' GROUP BY app_post_feedback.post_id_id '''
		sub1 = cursor.execute(post1)
		row1 = cursor.fetchall()
		post2 = ''' SELECT Count(app_post_feedback.report_post) from app_post_feedback 
		where app_post_feedback.report_post='Yes' GROUP BY app_post_feedback.post_id_id '''
		sub2 = cursor.execute(post2)
		row2 = cursor.fetchall()
		return render(request,'all_post.html',{'row2':row2,'detail':detail,'row':row,'row1':row1})
	else:
		return render(request,'login.html',{})
def post_comment(request,pk):
	if request.session.has_key('user_id'):
		user_id = request.session['user_id']
		if request.method == 'POST':
			food_id = Post.objects.get(id=pk)
			uid = Register_Detail.objects.get(id=int(user_id))
			comment = request.POST.get('comment')
			already_exist = Feedback.objects.filter(post_id=pk,user_id=int(user_id))
			if already_exist:
				messages.success(request,'You Already Comment.')
			else:
				crt = Feedback.objects.create(post_id=food_id,user_id=uid,comment=comment)
		comment_detail = Feedback.objects.filter(post_id=pk)
		tot = Feedback.objects.filter(post_id=pk).aggregate(Count('comment'))
		
		return render(request,'comment.html',{'comment_detail':comment_detail,'tot':tot})
	else:
		return render(request,'login.html',{})	
def like_post(request,pk):
	user_id=request.session['user_id']
	post_id=Post.objects.get(id=pk)
	uid=Register_Detail.objects.get(id=int(user_id))
	prt = Post_Feedback.objects.create(post_id=post_id,like_post='Yes',
	user_id=uid)
	return redirect('all_post')
def report_post(request,pk):
	user_id=request.session['user_id']
	post_id=Post.objects.get(id=pk)
	uid=Register_Detail.objects.get(id=int(user_id))
	prt = Post_Feedback.objects.create(post_id=post_id,report_post='Yes',
	user_id=uid)
	return redirect('all_post')

def post_detail(request):
	cursor = connection.cursor()
	sql= '''SELECT p.date from app_post as p GROUP BY p.date'''
	res = cursor.execute(sql)
	row = cursor.fetchall()
	if request.method == 'POST':
		a = request.POST.get('date')
		b = request.POST.get('title')
		if a:
			posts = Post.objects.filter(title__startswith=b,date=a).order_by('-id')
			return render(request,'post_detail.html',{'grouped_posts':row,'posts':posts,'a':a})
		else:
			posts = Post.objects.filter(title__startswith=b).order_by('-id')
			return render(request,'post_detail.html',{'grouped_posts':row,'posts':posts})
	return render(request,'post_detail.html',{'grouped_posts':row})
def women_rights(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		detail=Women_Right.objects.all()
		return render(request,'women_right.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def ngo(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		detail=NGO.objects.all()
		return render(request,'ngo.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def all_users(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		cursor = connection.cursor()
		post = ''' SELECT r.name,f.status,f.user_id_id,r.id,f.id from app_register_detail as r LEFT JOIN app_followuser as f
		ON r.id=f.follow_id  where r.id!='%d' ''' %(int(user_id)) 
		sub = cursor.execute(post)
		row = cursor.fetchall()
		return render(request,'all_users.html',{'row':row})
	else:
		return render(request,'login.html',{})
def follow(request,pk):
	user_id=request.session['user_id']
	uid = Register_Detail.objects.get(id=int(user_id))
	FollowUser.objects.create(user_id=uid,follow_id=pk,status='Follow')
	return redirect('all_users')
def unfollow(request,pk):
	user_id=request.session['user_id']
	exist = FollowUser.objects.filter(follow_id=pk,user_id=int(user_id),status='Follow')
	if exist:
		FollowUser.objects.filter(follow_id=pk,user_id=int(user_id),status='Follow').delete()
	
	return redirect('all_users')
def profile(request,pk):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		detail = Post.objects.filter(user_id=pk)
		user = Register_Detail.objects.filter(id=pk)
		return render(request,'profile.html',{'detail':detail,'user':user})
	else:
		return render(request,'login.html',{})
def friends_list(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		cursor = connection.cursor()
		post = ''' SELECT r.name,f.status,f.follow_id,r.id,f.id from app_register_detail as r INNER JOIN app_followuser as f
		ON r.id=f.follow_id  where f.status='Follow' ''' 
		sub = cursor.execute(post)
		row = cursor.fetchall()
		return render(request,'friends_list.html',{'row':row})
	else:
		return render(request,'login.html',{})
def edit_profile(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		user = Register_Detail.objects.filter(id=int(user_id))
		if request.method == 'POST':
			address = request.POST.get('address')
			mobile= request.POST.get('mobile')
			email = request.POST.get('email')
			fname = request.POST.get('fname')
			lname = request.POST.get('lname')
			country = request.POST.get('country')
			age = request.POST.get('age')
			gender = request.POST.get('gender')
			city = request.POST.get('city')
			zip = request.POST.get('zip')
			crt = Register_Detail.objects.filter(id=int(user_id)).update(
			address=address,mobile=mobile,email=email,fname=fname,lname=lname,
			city=city,country=country,zip=zip,age=age,gender=gender)
			if crt:
				messages.success(request,'Profile Updated Successfully')
		return render(request,'edit_profile.html',{'user':user})
	else:
		return render(request,'login.html',{})

import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def preprocess_title(title):
	X_train, X_test, y_train, y_test = train_test_split(X_titles, y_target, test_size=0.2, random_state=42)

	# Vectorize titles using TF-IDF
	tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed
	X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
	X_test_tfidf = tfidf_vectorizer.transform(X_test)

	# Train a random forest classifier
	rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
	rf_classifier.fit(X_train_tfidf, y_train)

	# Make predictions
	y_pred = rf_classifier.predict(X_test_tfidf)


	# Save the trained model to a file
	joblib.dump(rf_classifier, 'random_forest_model.pkl')
	joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
	title_vectorized = tfidf_vectorizer.transform([title])
	return title_vectorized

# Function to recommend posts based on their titles
def recommend_posts(new_post_title, all_post_titles):
    # Preprocess the title of the new post
    new_post_vectorized = preprocess_title(new_post_title)

    # Make predictions for all posts
    post_scores = rf_classifier.predict_proba(new_post_vectorized)[:, 1]

    # Sort posts by predicted scores
    sorted_indices = np.argsort(post_scores)[::-1]  # Sort in descending order

    # Recommend top posts
    top_post_indices = sorted_indices[:5]  # Adjust the number of recommended posts as needed
    recommended_posts = [all_post_titles[i] for i in top_post_indices]

    return recommended_posts

def recommend_posts_age(age, gender, posts):
    input_data = preprocess_title(age, gender)
    predictions = classifier.predict(input_data)
    # Assuming predictions contain recommendation scores for each post
    # You can rank posts based on these scores and return the top recommended ones
    recommended_posts = rank_and_select_top_posts(posts, predictions)
    return recommended_posts

def recommend_posts_view(request):
    age = request.user.age  # Assuming you have user age available
    gender = request.user.gender  # Assuming you have user gender available
    posts = Post.objects.all()  # Get all posts
    recommended_posts = recommend_posts_age(age, gender, posts)
    return recommended_posts