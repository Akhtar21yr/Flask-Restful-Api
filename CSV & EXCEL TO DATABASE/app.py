from flask import Flask,jsonify,request
import io
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import csv
import openpyxl

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/FlaskApi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    rollno = db.Column(db.Integer,unique=True)
    std =  db.Column(db.String(10))
    course = db.Column(db.String(20))

    def __init__(self,name,rollno,std,course) :
        self.name = name
        self.rollno = rollno
        self.std = std
        self.course = course

class StudentSchema(ma.Schema):
    class Meta :
        fields = ('name','rollno','std','course')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


@app.route('/database')
def create_database():
    with app.app_context():
        db.create_all()
    return jsonify({'msg':'database created'})

@app.route('/csv',methods=['POST'])
def excel_upload():
    if request.method == 'POST':
        existing = [roll[1] for roll in db.session.query(Student.rollno).all()]
        if request.files:
            uploaded_file = request.files['Student']
            data = uploaded_file.stream.read()
            stream = io.BytesIO(data)
            reader = csv.reader(io.TextIOWrapper(stream, encoding='utf-8'))
            i = 0
            for row in reader :
                if i ==0:
                    i += 1
                else:
                    if int(row[1]) in existing:
                        name = row[0]
                        rollno = row[1]
                        std = row[2]
                        course = row[3]
                        col = Student.query.filter_by(rollno=rollno).first()
                        if col.name != name or col.std != std or col.course != course :
                            col.name = name
                            col.std = std
                            col.course = course

                    else :
                        student = Student(*row)
                        db.session.add(student)
                    db.session.commit()

            return jsonify({'msg':'csv file upload successfully'})
    return jsonify({'msg':'some error occured'})

@app.route('/excel',methods=["POST"])
def csv_upload():
    existing = [roll[1] for roll in db.session.query(Student.rollno).all()]
    if request.files:
        uploaded_file = request.files['student']
        wb = openpyxl.load_workbook(uploaded_file)
        sheet = wb.active
        i = 0
        for row in sheet.iter_rows(values_only=True):
            if i == 0:
                i += 1
            else :
                if row[1] in existing:
                    name = row[0]
                    rollno = row[1]
                    std = row[2]
                    course = row[3]
                    col = Student.query.filter_by(rollno=rollno).first()

                    if col.name != name or col.std != std or col.course != course :
                            col.name = name
                            col.std = std
                            col.course = course

                    else :
                        student = Student(*row)
                        db.session.add(student)
                    db.session.commit()

                return jsonify({'msg':'csv file upload successfully'})
    return jsonify({'msg':'some error occured'})


        

if __name__=="__main__":
    app.run(debug=True)


