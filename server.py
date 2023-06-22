from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_json()  # get the JSON data from the request
    print(data)
    # TODO: Process the data
    return jsonify({'message': 'Received'}), 200

if __name__ == '__main__':
    app.run(debug=True)
