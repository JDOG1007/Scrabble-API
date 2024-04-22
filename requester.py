import requests
from flask import jsonify

board = []
for i in range(5):
    board.append([0, 0, 0, 0, 0])





boardgot = requests.post("http://127.0.0.1:5000/testarr?name",json=board)

boardgot = boardgot.json()
print(boardgot)





