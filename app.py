from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from database import connect_to_db, create_db_table

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


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
@app.route('/api/users/patch/<int:user_id>', methods=['PATCH'])
def api_patch_user(user_id):
    user_updates = request.get_json()  # Get the JSON object with updated fields

    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Build the SQL query dynamically based on the provided fields
        fields_to_update = []
        values = []
        
        if "name" in user_updates:
            fields_to_update.append("name = ?")
            values.append(user_updates["name"])
        if "email" in user_updates:
            fields_to_update.append("email = ?")
            values.append(user_updates["email"])
        if "phone" in user_updates:
            fields_to_update.append("phone = ?")
            values.append(user_updates["phone"])
        if "address" in user_updates:
            fields_to_update.append("address = ?")
            values.append(user_updates["address"])
        if "country" in user_updates:
            fields_to_update.append("country = ?")
            values.append(user_updates["country"])

        if not fields_to_update:
            return jsonify({'error': 'No valid fields to update'}), 400

        values.append(user_id)  # Append the user_id to the end for the WHERE clause

        query = f"UPDATE users SET {', '.join(fields_to_update)} WHERE user_id = ?"
        cur.execute(query, values)
        conn.commit()

        # Fetch the updated user
        updated_user = get_user_by_id(user_id)
        if not updated_user:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

    return jsonify(updated_user), 200

def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        if row:
            user["user_id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["phone"] = row["phone"]
            user["address"] = row["address"]
            user["country"] = row["country"]
        else:
            user = None  # If user_id not found, return None

    except Exception as e:
        print(f"Error fetching user by id: {e}")
        user = {}

    finally:
        conn.close()

    return user

# Run the app
if __name__ == "__main__":
    create_db_table()
    app.run(debug=True)
