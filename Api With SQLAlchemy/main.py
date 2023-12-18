from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/FlaskApi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    des = db.Column(db.String(200))
    r_date = db.Column(db.DateTime,default = datetime.utcnow)

    def __init__(self,name,des) -> None:
        self.name = name
        self.des = des

class BookSchema(ma.Schema):
    class Meta :
        fields = ('name','des','r_date')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/database')
def create_db():
    with app.app_context():
        db.create_all()
    return jsonify('database create')

@app.route("/add_book",methods=['POST'])
def add_book():
    name = request.json['name']
    des = request.json['des']
    book = Book(name=name, des=des)
    db.session.add(book)
    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/get_book',methods=['GET'])
def get_book():
    all_book = Book.query.all()
    result = books_schema.dump(all_book)
    return jsonify(result)

@app.route('/book_detail/<int:id>',methods=['GET'])
def book_detail(id):
    book = Book.query.get(id)
    result = book_schema.dump(book)
    return jsonify(result)

@app.route('/update_book/<int:id>',methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    name = request.json['name']
    des = request.json['des']

    book.name = name
    book.des = des

    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/delete_book/<int:id>',methods = ['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)


if __name__=='__main__':
    app.run(debug=True)
