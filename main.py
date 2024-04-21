from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/add")
def add():
    nums = str(request.args.get('nums')).split(';')
    print(nums)
    return jsonify(int(nums[0]) + int(nums[1]))


@app.route("/testarr", methods=['POST'])
def returnarr():
    arr = request.get_json()
    for i in range(5):
        for j in range(5):
            arr[i][j] = '☺'
    return (arr), 600

@app.route("/")
def home():
    return "you made it home"


if __name__ == '__main__':
    app.run(debug=True)

    app.config['SECRET_key'] = 'a'

    app.run
