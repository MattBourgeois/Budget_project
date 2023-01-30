from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_save import Person
from flask_app.models.money_spent import Spending


@app.route('/create', methods = ['POST'])
def add_payment():
	pass
	if 'user_id' not in session:
		return redirect('/logout')
	if not Spending.validate_exp(request.form):
		return redirect('/add')
	data = {
		"expense": request.form['expense'],
		"description": request.form['description'],
		"price": request.form['price'],
		"user_id": session["user_id"]
	}
	Spending.save_expense(data)
	return redirect('/dash')


# @app.route("/pie") This works, but i am going to do a scatter plot to show what days money was spent
# def show_chat():
# 	data = {'Task' : 'Hours per Day', 'Work' : 11, 'Eat' : 2, 'Commute' : 2, 'Watching TV' : 2, 'Sleeping' : 7}
# 	#print(data)
# 	return render_template('pie-chat.html', data=data)

@app.route('/pie') #this will need to be saved in a mysql so it can be taken.
def addprice():	
	lows = Spending.chat_expense() #list of dict
	print('A')
	print(lows)
	total = 0
	for x in lows: #iterates throught the list
		print((str(x['created_at'].strftime('%x')))) #need to figure out how to print indexes of dictoary
		#  variable.strftime{'%Y-%m-%d'}
		# print(w)
		print('B')
		print(x['price'])
		total += x['price']
	print('**********')
	print(total)
	return redirect('/acc' )


