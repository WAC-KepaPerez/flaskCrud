import base64
from flask import Flask, redirect, render_template, request, flash
from models import Workouts,db,User
import os
from flask_migrate import Migrate
import markdown
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from auth import auth_bp  # Import the auth blueprint
load_dotenv()
from flask_login import LoginManager,login_required,current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/workouts'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)
migrate=Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    print(User.query.get(int(user_id)))
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/readme')
def readme():
    with open('readme.md', 'r') as file:
        markdown_content = file.read()
    html_content = markdown.markdown(markdown_content)
    return render_template('readme.html', content=html_content)
@app.route('/workouts')
@login_required
def workouts():
    workouts = Workouts.query.filter_by(user_id=current_user.id).all()
    return render_template('workouts.html', workouts=workouts)

@app.route('/workouts/<int:workout_id>')
def view_workout(workout_id):
    # Find the workout by ID
    workout = Workouts.query.get(workout_id)
    return render_template('workout_details.html', workout=workout)

@app.route('/add_workout', methods=['POST'])
def add_workout():
    # Get the form data
    name = request.form['name']
    reps = int(request.form['reps'])  # Convert reps to integer
    description = request.form['description']
    
    # Create a new Workout object with the form data
    new_workout = Workouts(name=name, reps=reps, description=description,user_id=current_user.id)
    
    # Add the new workout to the database session
    db.session.add(new_workout)
    db.session.commit()
    # Redirect to the workouts page to display the updated list of workouts
    return redirect('/workouts')



# Define route to handle workout deletion
@app.route('/delete_workout', methods=['POST'])
def delete_workout():
    # Get the workout ID from the form data
    workout_id = request.form['workout_id']
    
    # Find the workout by ID
    workout = Workouts.query.get(workout_id)
    # Delete the workout from the database
    db.session.delete(workout)
    db.session.commit()
    
    # Redirect back to the workouts page
    return redirect('/workouts')

# Route to handle form submission for updating workout details
@app.route('/workouts/<int:workout_id>/update', methods=['POST'])
def update_workout(workout_id):
    # Get the workout by ID
    workout = Workouts.query.get(workout_id)
    
    # Update workout data based on the submitted form data
    workout.name = request.form['name']
    workout.reps = request.form['reps']
    workout.description = request.form['description']
    workout.completed = 'completed' in request.form  # Check if 'completed' checkbox is checked
    
    # Commit changes to the database
    db.session.commit()
    
    # Redirect back to the workout details page
    return redirect(f'/workouts')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),404


if __name__ == '__main__':
    app.run(debug=True)



