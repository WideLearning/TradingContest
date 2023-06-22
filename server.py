from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_json()
    print(data)
    return jsonify({'message': 'Received'}), 200

if __name__ == '__main__':
    app.run(debug=True)
