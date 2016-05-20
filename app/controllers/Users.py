"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
       
        self.load_model('User')
        self.load_model('Quote')
        self.db = self._app.db

        
   
    def index(self):
       return redirect('/main')

    def main(self):
        return self.load_view('index.html')
    def register(self):
        user_info = {
            "name" : request.form['name'],
            "alias" : request.form['alias'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "conpass" : request.form['conpass'],
            "birth_date": request.form['birth_date']
        }
        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['alias'] = create_status['user']['alias']
            flash("Successfully registered")
            
            return redirect('/quotes')
        else:
            
            for message in create_status['errors']:
                flash(message)
            return redirect('/main')

    def login(self):
        user_info ={
        "email" : request.form['email'],
        "password" : request.form['password']
            }
        login_status = self.models['User'].login_user(user_info)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['alias'] = login_status['user']['alias']
            
            flash("Successfully logged in")
            return redirect('/quotes')
        else:
            flash("invalid login")
            return redirect('/main')
    def quotes(self):
        quotes = self.models['Quote'].get_quotes()
        faves = self.models['Quote'].get_fav_by_id(session['id'])
        print faves
        return self.load_view('quotes.html', quotes = quotes, faves=faves)
    
    def add_quote(self, user_id):
        author =request.form['author']
        message = request.form['message']
        self.models['Quote'].add_quote(author, message, user_id)
        return redirect('/quotes')
        
    def show(self, user_id):
        user = self.models['User'].get_user(user_id)
        quotes =self.models['Quote'].get_quotes_by_id(user_id)
        count = len(quotes)
        return self.load_view('user.html', user=user[0], quotes=quotes, count=count)
    
    def logout(self):
        session.clear
        return redirect('/main')
    def add_fav(self,  quote_id):
        user_id = session['id']
        self.models['Quote'].add_fav(quote_id, user_id)
        return redirect('/quotes')
    
    def delete_fav(self, fav_id):
        self.models['Quote'].delete_fav(fav_id)
        return redirect('/quotes')
        
        
        
    