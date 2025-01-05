from flask import Flask, render_template, request, flash
import pickle
import numpy as np

# Load data files
popular_df = pickle.load(open('Pickle_Files/popular.pkl', 'rb'))
pt = pickle.load(open('Pickle_Files/pt.pkl', 'rb'))
books = pickle.load(open('Pickle_Files/books.pkl', 'rb'))
similarity_scores = pickle.load(open('Pickle_Files/similarity_scores.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = "YourSecretKey"  # Replace with a secure key

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Num-Ratings'].values),
                           rating=list(popular_df['avg-Ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if the input is blank
    if not user_input or user_input.strip() == "":
        flash("Enter a book name.", "error")
        return render_template('recommend.html', data=None)

    # Check if the book exists in the dataset
    matching_books = np.where(pt.index == user_input)[0]
    if len(matching_books) == 0:
        flash("Book not found.", "error")
        return render_template('recommend.html', data=None)

    # If the book is found, continue with the recommendation process
    index = matching_books[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
   