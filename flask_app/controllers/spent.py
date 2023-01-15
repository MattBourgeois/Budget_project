from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_save import Person
from flask_app.models.money_spent import Spending

@app.route('/create', methods = ['POSt'])
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