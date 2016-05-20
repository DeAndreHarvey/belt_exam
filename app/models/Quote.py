""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()
    
    def get_quotes(self):
        query = "select quotes.id,quotes.author,quotes.message,quotes.user_id,users.alias from quotes left join users on quotes.user_id= users.id"
        return self.db.query_db(query)
    
    def add_quote(self, author, message, user_id):
        sql = "INSERT INTO quotes (author, message, user_id, created_at) Values(:author, :message, :user_id, NOW())"
        data ={
            'author':author,
            'message':message,
            'user_id': user_id
            }
        self.db.query_db(sql, data)
        return True
    
    def get_quotes_by_id(self, user_id):
        query = "select * from quotes left join users on quotes.user_id= users.id where user_id = :user_id"
        data ={
            'user_id': user_id
        }
        return self.db.query_db(query,data)
    
    def add_fav(self,quote_id, user_id):
        sql = "INSERT INTO favorites (quote_id, user_id) Values(:quote_id, :user_id)"
        data ={
            'quote_id':quote_id,
            'user_id': user_id
            }
        self.db.query_db(sql, data)
        return True
    def get_fav_by_id(self, user_id):
        query = "select favorites.id, favorites.user_id,favorites.quote_id,quotes.author,quotes.message,quotes.user_id as quser_id,users2.alias  from favorites left join users on favorites.user_id= users.id left join quotes on  favorites.quote_id = quotes.id left join users as users2 on quotes.user_id = users2.id where favorites.user_id = :user_id"
        data ={
            'user_id': user_id
        }
        return self.db.query_db(query,data)
    
    def delete_fav(self, fav_id):
        query = "DELETE FROM favorites WHERE id = :fav_id"
        data = { "fav_id": fav_id }
        self.db.query_db(query, data)
        return True
        
    