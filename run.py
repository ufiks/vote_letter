from flask import Flask, request, abort
import json
import redis

app = Flask(__name__)
redis = redis.Redis(host='127.0.0.1')
all_letters = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0
}


def get_all_letters(*args):
    value = redis.get(*args)
    letters_decode = value.decode("utf-8")
    new_letters = json.loads(letters_decode.replace("'", '"'))
    return new_letters


@app.route('/letters', methods=['Get'])
def letters():
    if request.args.get('letter'):
        name_letter = get_all_letters('all_letters')
        dels = name_letter[request.args.get('letter')]
        return {'numberOfVotes': dels }, 200
    else:
        del_letters = get_all_letters('all_letters')
        return del_letters, 200


@app.route('/vote', methods=['Post'])
def vote():
    body = json.loads(request.data)
    letters_in_redis = get_all_letters('all_letters')
    if 'letter' not in letters_in_redis:
        abort(400, 'letter not detected')
    if body.get('letter') in letters_in_redis:
        current = letters_in_redis[request.args.get('letter')]
        current += 1
        redis.set(request.args.get('letter'), current)
        return json.dumps(letters_in_redis)


@app.route('/topletters', methods=['Get'])
def top_letters():
    topletter = get_all_letters('all_letters')
    return json.dumps(topletter), 200


redis.set('all_letters', str(all_letters))

if __name__ == '__main__':
    app.run(debug=True)
