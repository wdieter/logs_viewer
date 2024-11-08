import flask
from flask import Flask, request, jsonify, render_template

import domain

app = Flask(__name__)


@app.route("/logs", methods=['GET'])
def handle_get_logs():
    filename = request.args.get('filename', '')
    n = request.args.get('n', '20')
    keyword = request.args.get('keyword', '')

    try:
        n = int(n)
        if n < 0:
            raise ValueError
    except ValueError:
        return flask.make_response(jsonify({'error': 'Parameter "n" must be a non-negative integer.'}), 400)

    try:
        res = domain.get_logs(filename, n, keyword)
    except FileNotFoundError as e:
        return flask.make_response(jsonify({'error': 'file not found'}), 404)

    new_res = [file.to_dict() for file in res]
    return flask.make_response(jsonify({'logs': new_res}), 200)


@app.route('/', methods=['GET'])
def index():
    """
    Renders the HTML UI.
    """
    return render_template('index.html')


# for local development purposes app can be run with `python service.py`
if __name__ == '__main__':
    # Run the app on port 8080
    app.run(host='0.0.0.0', port=8080)