from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user import User

class Sighting:
    db = "sasquatch_schema"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.num_of = data['num_of']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO sightings(location,description,date,num_of, user_id)
            VALUES (%(location)s,%(description)s,%(date)s,%(num_of)s,%(user_id)s)
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def select_one(cls, data):
        query="""SELECT * FROM sightings 
            JOIN users ON users.id = sightings.user_id 
            WHERE sightings.id=%(id)s"""
        results=connectToMySQL(cls.db).query_db(query, data)
        result=results[0]
        print(result)
        temp={
            'id': result['users.id'],
            'first_name': result['first_name'], 
            'last_name': result['last_name'], 
            'email': result['email'], 
            'password': result['password'], 
            'created_at': result['users.created_at'], 
            'updated_at': result['users.updated_at']
        }
        result=cls(result)
        result.user=User(temp)
        return result
    
    @classmethod
    def update(cls,data):
        query="UPDATE sightings SET location=%(location)s, description=%(description)s, date=%(date)s, num_of=%(num_of)s, user_id=%(user_id)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
        
    @classmethod
    def delete(cls,data):
        query="DELETE FROM sightings WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db).query_db(query)
        print (results)
        sightings = []
        for row in results:
            sightings.append(cls(row))
        return sightings
    
    @staticmethod 
    def validate(data):
        is_valid = True
        if len(data['location']) < 2:
            flash("Location Please")
            is_valid = False
        if len(data['description']) < 2:
            flash("Tell Me!!")
            is_valid = False
        if len(data['date']) < 10:
            flash("When When When!!")
            is_valid = False
        # if "num_of" not in data:
        #     flash("Cmn How Many!!")
        #     is_valid = False
        return is_valid