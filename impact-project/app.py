from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np

# Load preprocessed data from pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))  # Data for popular books
pt = pickle.load(open('pt.pkl', 'rb'))              # Pivot table (used for recommendations)
book = pickle.load(open('book.pkl', 'rb'))          # Book dataset with details
similar_score = pickle.load(open('similar_score.pkl', 'rb'))  # Similarity scores for recommendations

# Extract and sort book titles for binary search
book_titles = sorted(book['Book-Title'].unique())  # Get unique book titles and sort them alphabetically

# Initialize the Flask app
app = Flask(__name__, static_folder='static')

# Define a binary search function to find a book title
def binary_search(arr, x):
    """
    Performs binary search on a sorted list to find the target value (x).
    Returns the index of the target if found, otherwise -1.
    """
    low, high = 0, len(arr) - 1  # Set the initial search range
    while low <= high:  # Continue as long as the range is valid
        mid = (low + high) // 2  # Calculate the middle index
        if arr[mid] == x:  # If the target is found
            return mid
        elif arr[mid] < x:  # If the target is greater, search the right half
            low = mid + 1
        else:  # If the target is smaller, search the left half
            high = mid - 1
    return -1  # Return -1 if the target is not found

# Home route: Renders the homepage
@app.route('/')
def home():
    return render_template('Home.html')

# Route to display the top 50 popular books
@app.route('/top-50')
def index():
    """
    Fetches the top 50 books and passes their details to the index.html template.
    Each book's details are sent as a dictionary in a list.
    """
    books = [
        {
            'title': title, 'author': author, 'image': image, 'vote': vote, 'rating': rating
        }
        for title, author, image, vote, rating in zip(
            popular_df['Book-Title'].values, popular_df['Book-Author'].values,
            popular_df['Image-URL-M'].values, popular_df['num_rating'].values, popular_df['avg_rating'].values
        )
    ]
    return render_template('index.html', books=books)

# Search route: Finds a book based on user input
@app.route('/search', methods=['POST'])
def search():
    """
    Handles the search functionality. 
    Receives the book title as input, performs binary search, 
    and returns book details if found, else returns a 'not found' response.
    """
    data = request.get_json()  # Get JSON data from the client
    print("Received data:", data)  # Debugging line to check the received data
    user_input = data.get('user_input')  # Extract the user's search input

    # Perform binary search to find the book
    index = binary_search(book_titles, user_input)
    if index != -1:  # If the book is found
        matched_book = book[book['Book-Title'] == book_titles[index]].iloc[0]
        return jsonify({
            'found': True,
            'title': matched_book['Book-Title'],
            'author': matched_book['Book-Author'],
            'image': matched_book['Image-URL-M']
        })
    else:  # If the book is not found
        return jsonify({'found': False})

# Recommendation route: Suggests similar books based on user input
@app.route('/recommand_book', methods=['GET', 'POST'])
def recommand_book():
    """
    Recommends books similar to the user's input.
    Uses similarity scores and book details to generate the recommendations.
    """
    data = []  # List to hold recommendation data
    error = None  # To store any error messages

    if request.method == 'POST':  # If the request method is POST
        user_input = request.form.get('user_input')  # Get user input from the form

        # Check if the book exists in the pivot table index
        if user_input not in pt.index:
            error = "Book not found."
        else:
            # Find the index of the book and sort similar books by their similarity score
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similar_score[index])), key=lambda x: x[1], reverse=True)[1:6]

            # Gather details for the top 5 similar books
            for i in similar_items:
                item = []
                temp_df = book[book['Book-Title'] == pt.index[i[0]]]  # Get details of the similar book
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)

    print(data)  # Debugging line to check the recommendations
    return render_template('book.html', data=data, error=error)

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the "About Us" page
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

# Routes for various book categories
@app.route('/fiction')
def fiction_page():
    return render_template('fiction.html')

@app.route('/non-fiction')
def non_fiction_page():
    return render_template('non_fiction.html')

@app.route('/mystery')
def mystery_page():
    return render_template('mystery.html')

@app.route('/romance')
def romance_page():
    return render_template('romance.html')

@app.route('/fantasy')
def fantasy_page():
    return render_template('fantasy.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
