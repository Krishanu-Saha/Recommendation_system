from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the pickled model and necessary data
model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

data_path = 'data.pkl'
with open(data_path, 'rb') as file:
    final_data = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form['user_id']

    # Get top 10 recommendations for the user
    top_n = {}
    for uid, iid, _, est, _ in model.test(model.build_anti_testset()):
        if uid in top_n:
            top_n[uid].append((iid, est))
        else:
            top_n[uid] = [(iid, est)]

    user_recommendations = top_n[user_id][:10]

    # Retrieve book information for the recommendations
    recommendations = []
    for book_id, est_rating in user_recommendations:
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
