from flask import Flask

app = Flask(__name__)


@app.route('/letters', methods=['Get'])
def post_letter():
    return '<h1>{A: 1,B: 2, C:3, D:4}</h1>'


@app.route('/letters', methods=['post'])
def letters():
    return '<h1>letter:A</h1>'


@app.route('/topletters', methods=['Get'])
def top_letters():
    return '<h1>topletter: B</h1>'


if __name__ == '__main__':
    app.run(debug=True)
