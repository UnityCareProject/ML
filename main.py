from flask import Flask, request, render_template, jsonify
import utils

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        endpoint = request.json.get('endpoint')
        input_value = request.json.get('input_value')
        user = request.json.get('user_value')

        if endpoint == 'question':
            result = utils.assistance(input_value)
        elif endpoint == 'user':
            try:
                user_id = int(input_value)
                result = utils.user(user_id)
            except ValueError:
                result = 'Invalid ID'
        else:
            return jsonify({'error': 'Unknown endpoint'}), 404

        response = {
            'status': 'success',
            'content': result
        }

        return jsonify(response), 200

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 