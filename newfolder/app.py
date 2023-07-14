

from flask import Flask
from Review.Review import review

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello, World! {review}'

if __name__ == '__main__':
    app.run(debug=True)
