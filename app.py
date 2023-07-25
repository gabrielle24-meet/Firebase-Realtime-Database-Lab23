from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



config = {
"apiKey": "AIzaSyAFSxExGBR4zkhGJRK_Xb-BFz3mE5T4nBM", 
  "authDomain": "example-9e0f4.firebaseapp.com",
  "projectId": "example-9e0f4",
  "storageBucket": "example-9e0f4.appspot.com",
  "messagingSenderId": "5891476454" ,
  "appId": "1:5891476454:web:920a5f8c52b0041e9be427",
 "measurementId": "G-LXM8YFZZ2B",
 "databaseURL": "xpEPDFGZfEehvHw2uU8MkRXLMtF2https://example-9e0f4-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()






app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'




@app.route('/', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       full_name = request.form['full_name']
       username = request.form['username']
       email = request.form['email']
       password = request.form['password']
       bio = request.form['bio']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": full_name, "email": email}
            db.child("Users").child(UID).set(user)
            users = {"full_name" : full_name, "username" : username, "email":email,  "bio" : bio}
            return redirect(url_for('signin'))
       
       except:
           error = "Authentication failed"
       return render_template("signup.html")

   


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == "Post":
        try:   
            title = request.com["title"]
            text = request.form["text"]
            tweet = {"title" : title,
            "text" : text}
            db.child("tweet").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "adasda"
    return render_template("add_tweet.html")




@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == "Post":
        password = request.form["password"]
        email = request.form["email"]
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
    except:
        return render_template("signin.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("all_tweets.html" , tweets = tweets)






    


if __name__ == '__main__':
    app.run(debug=True)


    