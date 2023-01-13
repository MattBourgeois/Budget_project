from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_save import Person

class Spending:
	db_name = 'Budget'
	def __init__(self, db_data):
		self.id = db_data['id']
		self.expense = db_data['expense']
		self.description = db_data['description']
		self.price = db_data['price']
		self.user_id = db_data['user_id']
		self.created_at = db_data['created_at']
		self.updated_at = db_data['updated_at']
		self.user = None

	@classmethod		
	def save_expense(cls, data):
		query = "INSERT INTO Money (expense, description, price, user_id) VALUES (%(expense)s, %(description)s, %(price)s, %(user_id)s);"
		return connectToMySQL(cls.db_name).query_db(query, data) 

	@classmethod
	def get_all(cls):   #get all info for the user so it can display on dashboard
		query = "SELECT * FROM Money LEFT JOIN User ON Money.user_id = User_id;"
		results = connectToMySQL(cls.db_name).query_db(query)
		list = []
		for row in results:
			Exps = cls(row)
			user_data = {
				'id': row['user_id'],
				'first_name': row['first_name'],
				'last_name': row['last_name'],
				'email': row['email'],
				'password': row['password'],
				'created_at': row['User.created_at'],
				'updated_at': row['User.updated_at']
			}
			# list.users = Person(user_data)
			list.append(cls(row))
			# print(list[0])
		return list
