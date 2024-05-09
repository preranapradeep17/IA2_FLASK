#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create database table
def create_table():
    with sqlite3.connect('travel_journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS travel_entries (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        location TEXT NOT NULL,
                        favorite_place TEXT NOT NULL,
                        from_date DATE NOT NULL,
                        to_date DATE NOT NULL,
                        description TEXT NOT NULL
                    )''')

@app.route('/')
def home():
    with sqlite3.connect('travel_journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM travel_entries")
        travel_entries = cursor.fetchall()

    # Convert the tuple of tuples to a list of dictionaries
    travel_entries = [{'id': entry[0], 'name': entry[1], 'age': entry[2], 'location': entry[3], 'favorite_place': entry[4], 'from_date': entry[5], 'to_date': entry[6], 'description': entry[7]} for entry in travel_entries]

    return render_template('final_app.html', travel_entries=travel_entries)

@app.route('/add', methods=['POST'])
def add_entry():
    # Retrieve the form data
    name = request.form['name']
    age = request.form['age']
    location = request.form['location']
    favorite_place = request.form['favorite_place']
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    description = request.form['description']

    # Store the data in the database
    with sqlite3.connect('travel_journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO travel_entries (name, age, location, favorite_place, from_date, to_date, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, age, location, favorite_place, from_date, to_date, description))

    return redirect(url_for('home'))

@app.route('/edit/<int:entry_id>', methods=['POST'])
def edit_entry(entry_id):
    # Retrieve the form data
    name = request.form['name']
    age = request.form['age']
    location = request.form['location']
    favorite_place = request.form['favorite_place']
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    description = request.form['description']

    # Update the entry in the database
    with sqlite3.connect('travel_journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE travel_entries SET name=?, age=?, location=?, favorite_place=?, from_date=?, to_date=?, description=? WHERE id=?", (name, age, location, favorite_place, from_date, to_date, description, entry_id))

    return redirect(url_for('home'))

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    # Delete the entry from the database
    with sqlite3.connect('travel_journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM travel_entries WHERE id=?", (entry_id,))

    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload_photo():
    # Retrieve the uploaded photo file
    photo = request.files['photo']

    # Process the photo file and store it in a directory or perform any other required actions

    return 'Photo uploaded successfully'

@app.route('/search', methods=['GET'])
def search_entries():
    # Retrieve the search parameters from the query string
    location = request.args.get('location')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    # Perform the search and filtering based on the parameters
    with sqlite3.connect('travel_journal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM travel_entries WHERE location=? OR from_date=? OR to_date=?", (location, from_date, to_date))
        search_results = cursor.fetchall()

    # Render the search results directly within the same route handler
    if search_results:
        result_str = "<h2>Search Results:</h2>"
        for entry in search_results:
            result_str += f"<p>Name: {entry[1]}, Location: {entry[3]}, From Date: {entry[5]}, To Date: {entry[6]}</p>"
        return result_str
    else:
        return "No results found."


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
