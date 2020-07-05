from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PayRoll.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    pay = db.Column(db.Float, nullable=False)
    hours = db.Column(db.Float)
    allowance = db.Column(db.Float)
    deduction = db.Column(db.Float)

    def __init__(self, first_name, last_name, pay, hours, allowance, deduction):
        self.first_name = first_name
        self.last_name = last_name
        self.pay = pay
        self.hours = hours
        self.allowance = allowance
        self.deduction = deduction

@app.route('/emp', methods=['GET'])
def get_emp():
    emp_list = Employee.query.all()
    emp = []
    for employee in emp_list:
        emp.append(
            {'id': employee.id,
            'first_name': employee.first_name, 
            'last_name': employee.last_name, 
            'pay': employee.pay,
            'hours': employee.hours,
            'allowance': employee.allowance,
            'deduction': employee.deduction})
    return jsonify({'employees': emp})



@app.route('/addemp', methods=['POST'])
def add_emp():
    data = request.get_json()
    new_emp = Employee(data['first_name'], data['last_name'], data['pay'], data['hours'], data['allowance'], data['deduction'])
    db.session.add(new_emp)
    db.session.commit()
    return 'Done', 201

@app.route('/net', methods=['POST'])
def get_net():
   emp_id = request.get_json()
   emp = Employee.query.filter_by(id=emp_id['id']).first()
   net = (emp.pay*emp.hours)+emp.allowance-emp.deduction
   return jsonify({'Monthly_Pay': net})


@app.route('/remove', methods=['POST'])
def remove():
   emp_id = request.get_json()
   emp = Employee.query.filter_by(id=emp_id['id']).first()
   db.session.delete(emp)
   db.session.commit()
   return 'Done', 201

@app.route('/edit', methods=['POST'])
def edit_field():
   data = request.get_json()
   emp = Employee.query.filter_by(id=data['id']).update({data['field']: data['value']})
   db.session.commit()
   return 'Done'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
