from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database connection
def connect_to_db():
    return sqlite3.connect('database.db')

# Creating the user table
def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL);
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

# Create the database table when the app starts
create_db_table()

# CRUD operations

# GET all users
@app.route('/api/users', methods=['GET'])
def api_get_users():
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = [{k: row[k] for k in row.keys()} for row in rows]
    return jsonify(users)

# GET a user by ID
@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row:
        user = {k: row[k] for k in row.keys()}
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Add a new user
@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()  # Get the JSON object from the request body
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Insert the new user into the database
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()  # Commit the transaction
        user['user_id'] = cur.lastrowid  # Get the last inserted user_id
    except Exception as e:
        conn.rollback()  # Rollback in case of any errors
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()  # Close the connection
    return jsonify(user), 201  # Return the newly added user

# Update an existing user
@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()  # Get the JSON object from the request body
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Update the user record in the database based on the provided user_id
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
                    (user['name'], user['email'], user['phone'], user['address'], user['country'], user['user_id']))
        conn.commit()  # Commit the transaction
    except Exception as e:
        conn.rollback()  # Rollback in case of any errors
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()  # Close the connection
    return jsonify(user), 200  # Return the updated user

# Delete a user
@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # Delete the user from the database
        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()  # Commit the transaction
        if cur.rowcount == 0:  # Check if a user was deleted
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        conn.rollback()  # Rollback in case of any errors
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()  # Close the connection
    return jsonify({'message': 'User deleted successfully'}), 200  # Return success message

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
