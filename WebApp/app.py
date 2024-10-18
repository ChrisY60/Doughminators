from flask import *

app = Flask(__name__)
app.secret_key = 'DoughminatorsKey'

@app.route("/")
def index():
    return "aa"

if __name__ == '__main__':
    app.run(port=8080)