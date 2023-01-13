from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Person:
	db_name = "Budget"
	
	def __init__(self, data):
		self.id = data["id"]
		self.first_name = data["first_name"]
		self.last_name = data["last_name"]
		self.email = data["email"]
		self.password = data["password"]
		self.created_at = data["created_at"]
		self.updated_at = data["updated_at"]

	@classmethod
	def save_new(cls, data):
		query = """INSERT INTO User(first_name, last_name, email, password) 
		VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
		return connectToMySQL(cls.db_name).query_db(query, data)

	@classmethod
	def get_by_id(cls, user_id):
		data = {
			'id': user_id
		}
		query = "SELECT * FROM User WHERE id = %(id)s;"
		results = connectToMySQL(cls.db_name).query_db(query, data)
		return cls(results[0])

	@classmethod
	def get_email(cls, data):
		query = "SELECT * FROM User WHERE email = %(email)s;"
		results = connectToMySQL(cls.db_name).query_db(query, data)
		if len(results) < 1:
			return False
		return cls(results[0])


	@staticmethod
	def validate(Person):
		is_valid = True
		query = "SELECT * FROM User Where email = %(email)s;"
		results = connectToMySQL(Person.db_name).query_db(query, Person)
		if len(results >= 1):
			flash("Email Taken", "Register")
			is_valid = False
		if not EMAIL_REGEX.match(Person['email']):
			flash("Invalid Email", 'Register')
			is_valid = False
		if len(Person['password']) < 8:
			flash("Password is not long enough", "Register")
			is_valid = False
		if Person['password'] != Person['confirm']:
			flash("Passwords Do Not Match", "Register")
			is_valid = False
		return is_valid