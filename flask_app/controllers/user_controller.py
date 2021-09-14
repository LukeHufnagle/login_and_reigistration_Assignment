from sys import meta_path
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Index Route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@app.route('/')
def index():
    return render_template('index.html')

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Register User Route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@app.route('/register', methods=['POST'])
def register():
    # validate user
    if not User.register_validation(request.form):
        return redirect('/')

    #create hash pasword
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #Add the user data to dictionary
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    #Call the class method on User
    user_id = User.register_user(data)
    #Store user id into session
    session['user_id'] = user_id
    return redirect('/dashboard')

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Login User Route
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route('/login', methods=['POST'])
def login_user():
    data = {
        'email' : request.form['email']
    }

    user_in_db = User.get_by_email(data)

    validation_data = {
        'user' : user_in_db,
        'password' : request.form['password']
    }
    if not User.login_validation(validation_data):
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    data = {
        'user_id' : session['user_id']
    }
    
    user = User.get_user_info(data)
    return render_template('show_user.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')