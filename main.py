from flask import Flask, request, jsonify
# from llama import analyze_question
import utils


app = Flask(__name__)

@app.route('/<endpoint>', methods=['POST'])
def handle_endpoint(endpoint):
    data = request.get_json()
    question = data.get('question')

    if endpoint == 'question':
        result = utils.assistance(question)
    elif endpoint == 'user':
        user_id = data.get('user_id')
        result = utils.user(user_id)
    else:
        return jsonify({'error': 'Unknown endpoint'}), 404
    response = {
        'status': 'success',
        'content': result
    }

    return jsonify(response), 200



if __name__ == '__main__':
    app.run(debug=True)