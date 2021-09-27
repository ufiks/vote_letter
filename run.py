from typing import List

from flask import Flask, request, abort, jsonify
import json
import redis

app = Flask(__name__)
redis = redis.Redis(host='127.0.0.1')
hashset_name = 'votting'
init_values = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0
}


def initialize() -> None:
    init_values = {
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0
    }

    for key in init_values:
        value = 0
        redis.set(key, value)


def get_all_keys() -> List[str]:
    all_keys = list(redis.scan_iter("*"))

    return [key.decode() for key in all_keys]


def get_db() -> dict:
    db = {}

    for key in get_all_keys():
        value = redis.get(key)

        db[key] = value.decode()
    return db


@app.route('/letters', methods=['Get'])
def letters() -> json:
    query_letter = request.args.get('letter', None)

    if query_letter is None:
        return jsonify(get_db()), 200

    if query_letter not in get_all_keys():
        abort(400, 'Letter does not exist in database')
    decoded_query_letter = redis.get(query_letter)
    result = {
        query_letter: decoded_query_letter.decode()
    }

    return jsonify(result), 200


@app.route('/vote', methods=['Post'])
def vote() -> json:
    required_key = 'letter'
    body = json.loads(request.data)
    if required_key not in body:
        abort(400, 'did not send letter')

    target_letter = body[required_key]

    if target_letter not in get_all_keys():
        abort(400, 'your key is not in the database')

    db = get_db()
    current = int(db[target_letter])
    current += 1
    redis.set(target_letter, current)

    return jsonify(get_db())


@app.route('/maxvoted', methods=['Get'])
def maxvoted() -> json:
    votes = 'votes_number:'
    maxed_sum = sum(int(v) for v in get_db().values())

    return jsonify(votes + str(maxed_sum))


initialize()
if __name__ == '__main__':
    app.run(debug=True)
