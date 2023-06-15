from flask import Flask, render_template, request
import pandas as pd
import pickle


app = Flask(__name__)

# Load the pickled model
model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

with open('Top_n.pkl','rb') as file:
    top_n = pickle.load(file)

# Load the data from CSV file and convert it to a DataFrame
data_path = 'final_data.csv'
final_data = pd.read_csv(data_path)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['GET','POST'])
def recommend():
    user_id = request.form.get('user_id')

    
    # Retrieve book information for the recommendations
    recommendations = []
    for book_id, est_rating in top_n[int(user_id)]:
        book_info = final_data.loc[final_data['ISBN'] == book_id, ['ISBN', 'Book-Title', 'Book-Rating', 'Image-URL-S']].iloc[0]
        recommendations.append({
            'ISBN': book_info['ISBN'],
            'Book-Title': book_info['Book-Title'],
            'Book-Rating': book_info['Book-Rating'],
            'Image-URL-S': book_info['Image-URL-S']
        })

    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

