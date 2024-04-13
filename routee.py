from flask import Flask, url_for, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import os
from forms import StudentForm, DeleteForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SECRET_KEY'] = '48a89ef0b9a63e63dc8a5ca21fc1871d'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}', '{self.last_name}', '{self.email}','{self.gender}', '{self.state}',)"



@app.route('/create', methods=['POST', 'GET'])
def create_list():
    stud_Form = StudentForm()
    if stud_Form.validate_on_submit():
        try:
            student = Students(first_name=stud_Form.first_name.data, last_name=stud_Form.last_name.data,
                            email=stud_Form.email.data, gender=stud_Form.gender.data, state=stud_Form.state.data)
            db.session.add(student)
            db.session.commit()
            flash('Student has been added to the list!')
            return redirect(url_for('student_list'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exixts, use another')
            return redirect(url_for('create_list'))
    return render_template('create.html', form=stud_Form, title='Create')


@app.route('/edit/<int:student_id>', methods=['POST', 'GET'])
def edit(student_id):
    student_by_id = Students.query.get_or_404(student_id)
    stud_form = StudentForm()

    if request.method == 'GET':
        stud_form.first_name.data = student_by_id.first_name
        stud_form.last_name.data = student_by_id.last_name
        stud_form.email.data = student_by_id.email
        stud_form.gender.data = student_by_id.gender
        stud_form.state.data = student_by_id.state

    elif stud_form.validate_on_submit():
        try:
            student_by_id.first_name = stud_form.first_name.data
            student_by_id.last_name = stud_form.last_name.data
            student_by_id.email = stud_form.email.data
            student_by_id.gender = stud_form.gender.data
            student_by_id.state = stud_form.state.data
            db.session.commit()
            flash('Student data has been updated!', 'sucess')
            return redirect(url_for('student_list'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists, use another')


    return render_template ('create.html', form=stud_form, title='Edit')


@app.route('/', methods=['POST', 'GET'])
def student_list():
    studentsss = Students.query.all()
    return render_template('student_list.html', list_of_students=studentsss)


@app.route('/delete/<int:student_id>', methods=['POST', 'GET'])
def delete(student_id):
    student_by_id = Students.query.get_or_404(student_id)
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        db.session.delete(student_by_id)
        db.session.commit()
        flash('Student data has been deleted')
        return redirect(url_for('student_list'))
    return render_template('delete.html', students=student_by_id, form=delete_form)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)