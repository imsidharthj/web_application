from flask import Flask, render_template, request, redirect, url_for,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from daignosis_database import Base, Patient_data

app = Flask(__name__)
app.secret_key = 'super_secert_key'

engine = create_engine('sqlite:///patientdata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/patients')
def PatientInformation():
    patients = session.query(Patient_data).all()
    return render_template('patients.html', patients=patients)

@app.route('/patient/new', methods=['GET', 'POST'])
def newPatient():
    if request.method == 'POST':
        new_patient = Patient_data(
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
            weight=request.form['weight'],
            allergy=request.form['allergy']
        )
        session.add(new_patient)
        session.commit()
        flash("New patient added successfully!")
        return redirect(url_for('PatientInformation'))
    else:
        return render_template('daignosis_from.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
