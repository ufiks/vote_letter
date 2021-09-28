import json
from typing import Tuple

import redis
from flask import request, abort, jsonify, Response
from instances import redis, app
from services import initialize, get_all_keys, get_db


@app.route('/letters', methods=['Get'])
def letters() -> Tuple[Response, int]:
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
def vote() -> Tuple[Response, int]:
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

    return jsonify(get_db()), 201


@app.route('/maxvoted', methods=['Get'])
def maxvoted() -> Tuple[Response, int]:
    sum_votes = sum(int(v) for v in get_db().values())

    return jsonify({'votes_number': sum_votes}), 200


initialize()
if __name__ == '__main__':
    app.run(debug=True)
