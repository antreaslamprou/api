from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

#Create connection with database
conn = sqlite3.connect('skylinedb.sqlite', check_same_thread=False)
cursor = conn.cursor()

def add_column_names(cursor, rows):
    
    # Get column names from the cursor (chat-gpt assisted)
    column_names = [description[0] for description in cursor.description]
                
    # Combine column names with row data (chat-gpt assisted)
    result = [dict(zip(column_names, row)) for row in rows]
                                  
    # Convert the list of dictionaries to JSON
    return result


@app.route("/")
def index():
    return "Asou Elenaaa!"

#View, Add, Edit and Delete Users
@app.route("/users", defaults={"user_id" : None}, methods=['GET', 'POST']) 
@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def users_functionality(user_id):
    match request.method:

 
        #----> VIEW USERS <----#

        case 'GET':

            # If a user id is provided
            if user_id is None:

                # Gets the database data
                rows = cursor.execute('SELECT * FROM users').fetchall()
            
            # If no user id is provided
            else:
                 
                # Gets the database data for single user
                 rows = cursor.execute('SELECT * FROM users WHERE id= ?', (str(user_id,))).fetchall()

            # Find the user with user_id or shows exception/error (chat-gpt assisted)
            try: 
                      
                # If user is not in database 
                if not rows:

                    return jsonify({'error': 'User not found!'}), 400

                return jsonify(add_column_names(cursor, rows))
            
            except Exception as e:

                return jsonify({'error': str(e)}), 400
                
                
        #----> ADD USER <----#

        case 'POST': 

            #Save the new user details json as array
            content = request.get_json()

            #Save user's details (chat-gpt assisted)
            first_name = content['first_name']
            last_name = content['last_name']
            email = content['email']
            password = content['password']
            telephone = content['telephone']
            role = content['role']
            
            #Adds the user to the database or shows exception/error
            try:

                cursor.execute('INSERT INTO users(first_name, last_name, email, password, telephone, role, created_at) VALUES (?, ?, ?, ?, ?, ?, datetime(CURRENT_TIMESTAMP, "+1 hour"))', (first_name, last_name, email, password, telephone, role))
                conn.commit()

                return jsonify({'OK': "User added"}), 201 
            
            except Exception as e:

                return jsonify({'error': str(e)}), 400
            
            
        #----> UPDATE USER <----#

        case 'PUT':   

            #Save the new user details json as array
            content = request.get_json()

            #Save user's details(chat-gpt assisted)
            first_name = content['first_name']
            last_name = content['last_name']
            email = content['email']
            password = content['password']
            telephone = content['telephone']
            role = content['role']

            #Updates the user or shows exception/error
            try: 

                result = cursor.execute('UPDATE users SET first_name = ?, last_name = ?, email = ?, password = ?, telephone = ?, role = ? WHERE id = ?', (first_name, last_name, email, password, telephone, role, user_id)).fetchall() 
                return jsonify({'OK': 'User updated!'}), 202

            except Exception as e:

                return jsonify({'error': str(e)}), 400
            

        #----> DELETE USER <----#

        case 'DELETE': 

            #Deletes the user or shows exception/error
            try:

                cursor.execute('DELETE FROM users WHERE id=?', (str(user_id)))
                return jsonify({"OK" : "User deleted!"}), 202
            
            except Exception as e:

                return jsonify({"error" : str(e)}), 400                


#View, Add, Edit and Delete Services
@app.route("/services", defaults={"service_id" : None}, methods=['GET', 'POST']) 
@app.route('/services/<int:service_id>', methods=['PUT', 'DELETE'])
def services_functionality(service_id):
    match request.method:
        
        
        #----> VIEW SERVICES <----#

        case 'GET':
            rows = cursor.execute('SELECT * FROM services').fetchall()

            try:
            
                return jsonify(add_column_names(cursor, rows))

            except Exception as e:

                return jsonify({'error': str(e)}), 400
            
        
        #----> ADD SERVICE <----#

        case 'POST': 

            #Save the new service details json as array
            content = request.get_json()

            #Save service's details (chat-gpt assisted)
            name = content['name']
            descreption = content['descreption']
            price = content['price']
            
            #Adds the service to the database or shows exception/error
            try:

                cursor.execute('INSERT INTO services(name, descreption, price) VALUES (?, ?, ?)', (name, descreption, price))
                conn.commit()

                return jsonify({'OK': "Service added"}), 201 
            
            except Exception as e:

                return jsonify({'error': str(e)}), 400
            
            
        #----> UPDATE SERVICE <----#

        case 'PUT':   

            #Save the new service details json as array
            content = request.get_json()

            #Save service's details (chat-gpt assisted)
            name = content['name']
            descreption = content['descreption']
            price = content['price']

            #Updates the service or shows exception/error
            try: 

                result = cursor.execute('UPDATE services SET name = ?, descreption = ?, price = ? WHERE id = ?', (name, descreption, price, service_id)).fetchall() 
                return jsonify({'OK': 'Service updated!'}), 202

            except Exception as e:

                return jsonify({'error': str(e)}), 400
            

         #----> DELETE SERVICES <----#

        case 'DELETE': 

            #Deletes the service or shows exception/error
            try:

                cursor.execute('DELETE FROM services WHERE id=?', (str(service_id)))
                return jsonify({"OK" : "Service deleted!"}), 202
            
            except Exception as e:

                return jsonify({"error" : str(e)}), 400               




if __name__ == "__main__":
    app.run(debug=True)
