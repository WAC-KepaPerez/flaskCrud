import base64
from flask import Flask, redirect, render_template, request
from models import Workouts,db
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/workouts'
db.init_app(app)
migrate=Migrate(app,db)


@app.route('/form')
def form():
    return render_template('form.html')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/workouts')
def index():
    workouts = Workouts.query.all()
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
    new_workout = Workouts(name=name, reps=reps, description=description)
    
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
@app.route('/save_images', methods=['POST'])
def download_and_save():
     # Obtener las imágenes codificadas en base64 desde la solicitud POST
    images_base64 = [request.form[key] for key in request.form]
    if not os.path.exists('uploads_'):
        os.makedirs('uploads')
    # Guardar cada imagen en un archivo
    for index, image_base64 in enumerate(images_base64):
        image_data = base64.b64decode(image_base64.split(',')[1])  # Decodificar la imagen desde su representación base64
        with open(os.path.join('uploads', f'image_{index}.png'), 'wb') as file:
            file.write(image_data)

    return 'Imágenes guardadas correctamente'

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),404


if __name__ == '__main__':
    app.run(debug=True)



