from flask import Flask, render_template, request
import mysql.connector

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

# Replace with your MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="belt_test"
)

# Function to fetch names and belt information from database
def fetch_names_and_belts():
    cursor = db.cursor()
    cursor.execute("SELECT name, belt FROM entries")
    names_and_belts = cursor.fetchall()
    cursor.close()
    return names_and_belts

# Function to calculate result from numbers
def calculate_result(numbers):
    if len(numbers) != 5:
        return None
    
    # Sort numbers
    numbers.sort()
    
    # Calculate sum of middle three values
    result = sum(numbers[1:4])
    
    return result

# Route to render the HTML template
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission
        selected_name = request.form['selected_name']
        belt_info = request.form['belt_info']
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        num3 = float(request.form['num3'])
        num4 = float(request.form['num4'])
        num5 = float(request.form['num5'])
        
        # Calculate result
        numbers = [num1, num2, num3, num4, num5]
        result = calculate_result(numbers)

        # Insert data into another table (results_table)
        cursor = db.cursor()
        insert_sql = "INSERT INTO kata_score (name, belt, jug1, jug2, jug3, jug4, jug5, total_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        insert_values = (selected_name, belt_info, num1, num2, num3, num4, num5, result)
        cursor.execute(insert_sql, insert_values)
        db.commit()
        cursor.close()

        names_and_belts = fetch_names_and_belts()

        # Render the template with updated data and result
        return render_template('kata_score.html', names_and_belts=names_and_belts, result=result)

    # If GET request, just fetch names and belts
    names_and_belts = fetch_names_and_belts()
    print("\n data is \n ",names_and_belts)
    # Render the HTML template with names and belts
    return render_template('kata_score.html', names_and_belts=names_and_belts)
if __name__ == '__main__':
    app.run(debug=True)
