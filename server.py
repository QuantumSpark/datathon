from flask import Flask, request
from predictor import predict


app = Flask(__name__)

PORT = int(os.getenv('PORT', 8000))
@app.route('/classifyrequest', methods=['POST'])
def example():
    json_dict = request.get_json()
    return predict(json_dict['body'])


if __name__ == '__main__':
    app.run(port = :PORT)
