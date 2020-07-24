#Author: Nutan Nimkar
#Date:   23rd July 2020
#Assignment 5
#All the imports required to run the app and its functions
from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import random

#Initiating the SQLALCHEMY DataBase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db'
db = SQLAlchemy(app)

#Initiates the migration function
#Migration helps makes changes to the database, like adding rows or columns

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

#This class defines the model for the Database
# It creates all the columns to store data in 

class Data(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    proteins = db.Column(db.Integer,default = 0)
    carbs = db.Column(db.Integer,default = 0)
    fats = db.Column(db.Integer,default = 0)

    total=db.Column(db.Integer,default = 0)
    totalexceed=db.Column(db.Integer,default = 0)
    displaylimit = db.Column(db.String,default = 0)

#Representation of the Output
    def __repr__(self):
        return '<Task %r>' % self.id      

#This function helps the data to get collected from the form which is situated on the HTML page
#Data is collected to specific variables and then added to the database using db.session.add()
# The data is stored in terms latest to oldest

@app.route("/", methods = ['POST','GET'])
def add():
    if request.method =='POST':
        add_content = request.form.get('add_food')
        add_carbs = int(request.form.get('add_carbs'))
        add_pro = int(request.form.get('add_pro'))
        add_fat = int(request.form.get('add_fats'))

        add_total = (0.50*add_carbs)+(0.25*add_pro)+(0.25*add_fat)

        add_limit =  int(request.form.get('add_limit'))
        add_dislimit = add_limit - add_total

        if(add_dislimit == 0):
            add_dislimit = 'Exceeded'
        else:
             add_dislimit = str(int(add_dislimit))

        new_content = Data(content = add_content,carbs = add_carbs,proteins = add_pro,fats = add_fat,total = add_total,totalexceed = add_limit,displaylimit = add_dislimit)
        try:
            db.session.add(new_content)
            db.session.commit()
            return redirect('/')
        except:
            return " Issue with the entry/text"   
    else:
        check = Data.query.order_by(Data.date_created).all()
        return render_template('home.html',check = check)

#This function helps delete information from the html
# It also removes the data from the database, by using database functions
#         
@app.route('/delete/<int:id>')
def delete(id):
    content_deletion = Data.query.get_or_404(id)
        
    try:
        db.session.delete(content_deletion)
        db.session.commit()

        return redirect('/')
    except:
        return 'Issue occured with the function'
#This function helps update the information from the html page
#It redirects to another html page where the data can be manipulated and inserted again

@app.route('/update/<int:id>', methods =['GET','POST'])
def update(id):
    update_content =  Data.query.get_or_404(id)
    if request.method == 'POST':
        update_content.content = request.form.get('add_food')

        update_content.carbs = int(request.form.get('quantity2'))
        update_content.fats = int(request.form.get('quantity1'))
        update_content.proteins = int(request.form.get('quantity'))

        update_content.totalexceed = request.form.get('quantity3')

        update_content.total = (0.25*update_content.carbs) + (0.25*update_content.fats) + (0.25*update_content.proteins)

        update_content.displaylimit = int(update_content.totalexceed) - update_content.total

        if(update_content.displaylimit < 0):
            update_content.displaylimit= 'Exceeded'
        else:
             update_content.displaylimit = str(int(update_content.displaylimit))

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Issue with the update"    
    else:
        return render_template('update.html',update_content = update_content)

if __name__ == "__main__":
    app.run(debug=True)
    #manager.run()