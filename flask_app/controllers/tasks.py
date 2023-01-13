from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_save import Person
from flask_app.models.money_spent import Spending

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
	# flash("hello")
	# flash("Goodbye")
	return render_template('login.html')

@app.route('/Reg')
def Reg():
	return render_template('register.html')

@app.route('/Register', methods = ['POST']) #register method, FLASH IS NOT WORKING(because it isnt in there)
def register():
	data = {
		"first_name": request.form['first_name'],
		"last_name": request.form['last_name'],
		"email": request.form['email'],
		"password": bcrypt.generate_password_hash(request.form['password'])
	}
	id = Person.save_new(data)
	session['user_id'] = id
	return redirect('/dash')


@app.route('/login', methods = ['POST']) #login method, FLASH IS NOT WORKING
def login():    
    user = Person.get_email(request.form)
    print(user)
    if not user:
        flash("Wrong Email")
        return redirect('/')
        # return render_template('login.html')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrect")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dash')

@app.route('/logout') #loges the user out
def logout():
	session.clear()
	return redirect('/')

@app.route('/dash') # shows dashboard
def dashboard():
	# print(User_id)
	print(session['user_id'])
	if 'user_id' not in session:
		return redirect('/log')
	# print(session['user_id'])
	main = Person.get_by_id(session['user_id'])
	spent = Spending.get_all()
	return render_template('index.html', user = main, spent = spent) 

@app.route('/add') # brings person to the add expense page
def add_exp():
	user = Person.get_by_id(session['user_id'])
	return render_template('spent.html', user = user)

@app.route('/acc') # shows a singular account
def show_account():
	user = Person.get_by_id(session['user_id'])
	return render_template('account.html', user = user)