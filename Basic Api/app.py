from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello World</h1>"

@app.route('/checkeven/<int:No>')
def checkeven(No):
    if No%2 == 0:
        result = {
            'Number':No,
            "Even":True,
            'Ip' :'192.168.1.1'
        }
    else :
        result = {
            'Number':No,
            "Even":False,
            'Ip' :'192.168.1.1'
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run()