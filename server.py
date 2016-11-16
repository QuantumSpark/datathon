from flask import Flask,request
from predictor import predict


app = Flask(__name__)


@app.route('/classifyrequest',  methods=['POST'])
def example():
    json_dict = request.get_json()
    thing = json_dict['body']
    print thing
    return predict(thing)


if __name__ == '__main__':
    app.run()
