from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Replace this with your actual database path
DATABASE_PATH = 'database.db'

def get_personalized_recommendations(username):
    # Connect to the database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Retrieve user preferences and browsing habits
    query = "SELECT preferences, browsing_habits FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    
    if user_data:
        preferences = user_data[0]
        browsing_habits = user_data[1]
        
        # Use preferences and browsing habits to generate personalized recommendations
        # You can implement collaborative filtering algorithms here
        
        recommendations = []  # Placeholder, replace with actual recommendations
        
    else:
        recommendations = []

    conn.close()

    return recommendations

@app.route('/buy', methods=['POST'])
def buy_item():
    data = request.json
    item_name = data.get('item_name', '')
    keywords = data.get('keywords', '')
    username = data.get('username', '')

    # Store the bought item and its keywords in the database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    query = "INSERT INTO bought_items (item_name, keywords, username) VALUES (?, ?, ?)"
    cursor.execute(query, (item_name, keywords, username))
    
    # Update user preferences and browsing habits
    update_query = "UPDATE users SET preferences = ?, browsing_habits = ? WHERE username = ?"
    cursor.execute(update_query, (data.get('preferences', ''), data.get('browsing_habits', ''), username))
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Item bought successfully!'})

@app.route('/recommend', methods=['GET'])
def recommend_items():
    username = request.args.get('username', '')
    recommendations = get_personalized_recommendations(username)
    
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
