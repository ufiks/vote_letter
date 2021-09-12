from flask import Flask
import json

app = Flask(__name__)
lettersall = json.dumps({'A': 1, 'B': 2, 'C': 3, 'D': 4})


@app.route('/letters', methods=['Get'])
def get_letter():
    return lettersall


@app.route('/letters', methods=['post'])
def letters():
    letters_1 = json.dumps('letter:A')
    return letters_1


@app.route('/topletters', methods=['Get'])
def top_letters():
    topletters = json.dumps('topletter: B')
    return topletters


if __name__ == '__main__':
    app.run(debug=True)
