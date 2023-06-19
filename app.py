import mysql.connector
from flask import jsonify

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="vignesh",
    password="123@Viki",
    database="ticketbooking"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

@app.route('/')
def index():
    # Fetch all movies from the database
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    return render_template('movie-manager.html', movies=movies)


@app.route('/add_movie', methods=['POST'])
def add_movie():
    movie_title = request.form['movieTitle']
    show_timing = request.form['showTiming']
    theater_name = request.form['theaterName']
    city = request.form['city']

    if movie_title and show_timing and theater_name and city:
        # Insert the movie into the database
        sql = "INSERT INTO movies (title, show_timing, theater_name, city) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (movie_title, show_timing, theater_name, city))
        db.commit()

    return redirect('/')




@app.route('/search_movie', methods=['POST'])
def search_movie():
    search_term = request.form['searchTerm']

    # Search movies in the database
    query = "SELECT * FROM movies WHERE title LIKE %s OR show_timing LIKE %s OR theater_name LIKE %s OR city LIKE %s"
    search_value = f"%{search_term}%"
    cursor.execute(query, (search_value, search_value, search_value, search_value))

    movies = cursor.fetchall()

    return render_template('movie-manager.html', movies=movies)

@app.route('/booking_form', methods=['GET'])
def show_booking_form():
    movie_id = request.args.get('movieId')
    return render_template('booking_form.html', movie_id=movie_id)

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    # Process the form submission and book the ticket
    movie_id = request.form.get('movieId')
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    tickets = int(request.form.get('tickets'))

    # Calculate the total amount based on the number of tickets
    ticket_price = 10  # Adjust the ticket price as needed
    amount = tickets * ticket_price

    # Add your booking logic here

    return render_template('booking_form.html', movie_id=movie_id, amount=amount)

@app.route('/delete_movie', methods=['POST'])
def delete_movie():
    movie_id = request.json['movieId']

    # Delete the movie from the database
    sql = "DELETE FROM movies WHERE id = %s"
    cursor.execute(sql, (movie_id,))
    db.commit()

    # Check if the movie was successfully deleted
    if cursor.rowcount > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete movie.'})


@app.route('/update_movie', methods=['POST'])
def update_movie():
    movie_id = request.json['movieId']
    new_movie_title = request.json['newMovieTitle']
    new_show_timing = request.json['newShowTiming']
    new_theater_name = request.json['newTheaterName']
    new_city = request.json['newCity']

    # Update the movie title, show timing, theater name, and city in the database
    sql = "UPDATE movies SET title = %s, show_timing = %s, theater_name = %s, city = %s WHERE id = %s"
    cursor.execute(sql, (new_movie_title, new_show_timing, new_theater_name, new_city, movie_id))
    db.commit()

    # Check if the movie was successfully updated
    if cursor.rowcount > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to update movie.'})

@app.route('/movies')
def show_movie_list():
    # Fetch all movies from the database
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    return render_template('movie-manager.html', movies=movies)

if __name__ == '__main__':
    app.run(port=5003)
