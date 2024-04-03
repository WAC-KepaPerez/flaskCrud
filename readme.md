# FlaskCrud App

This is a simple Flask application for tracking workouts.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/WAC-KepaPerez/flaskCrud.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd flaskCrud
    ```

3. **Set up a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    venv\Scripts\activate

e venv/bin/activate
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database:**

   - Create a MySQL database named `workouts`.
   - Update the database connection URI in `app.py` to match your MySQL database configuration.

6. **Run the Flask application:**

    ```bash
    python app.py
    ```
    The application will be accessible at `http://localhost:5000`.

## Usage

- Navigate to `http://localhost:5000/workouts` to view all workouts.
- Use the form on the page to add new workouts.
- Each workout can be marked as completed by checking the corresponding checkbox.


