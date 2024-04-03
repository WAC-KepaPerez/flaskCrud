from flask import Blueprint, render_template, request, redirect, flash
from models import User, db
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager,login_required,login_user,logout_user


auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                flash('Login succesfully!!!', 'success')
                print(user)
                return redirect('/')
            else:
                flash('Wrong Password', 'error')
        else:
            flash('There is no user with that name', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect('/register')  # Redirect back to the registration page if username exists
        # Create a new user
         # Try to create a new user
        try:
            # Create a new user
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User successfully registered!', 'success')
            return redirect('/workouts')  # Redirect to a success page or any other route after registration
        
        except IntegrityError:
            db.session.rollback()  # Rollback the session to avoid partially committed changes
            flash('Error: Failed to register user.', 'error')
            return redirect('/register')
    
    return render_template('auth/register.html')



@auth_bp.route('/user', methods=['POST','GET'])
def user():
    return render_template('auth/user.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('LogOut Succesfully !!', 'success')
    return render_template('index.html')
