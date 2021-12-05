from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.email import Email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if not Email.validate_email(request.form):
        return redirect('/')
    session['email'] = request.form['email']
    data = {
        'email' : request.form['email']
        }
    Email.create(data)
    return redirect('/success')

@app.route('/success')
def success():
    emails = Email.get_all()
    return render_template('success.html', emails=emails)

@app.route('/delete/<id>')
def delete(id):
    data = {'id' : id}
    Email.delete(data)
    return redirect('/success')