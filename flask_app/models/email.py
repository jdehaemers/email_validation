from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Email:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(self, data):
        query = 'INSERT INTO emails (email) VALUES ( %(email)s );'
        return connectToMySQL('validated_emails').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM emails;'
        results = connectToMySQL('validated_emails').query_db(query)
        return results
    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM emails WHERE id = %(id)s;'
        return connectToMySQL('validated_emails').query_db(query, data)
    
    @staticmethod
    def validate_email( email ):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address!")
            is_valid = False
        entries = Email.get_all()
        for entry in entries:
            if entry['email'] == email['email']:
                flash("Non-unique address!")
                is_valid = False
        return is_valid