from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db'
db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)
class Data(db.Model):
    # for i in range(0,3): 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    proteins = db.Column(db.Integer,default = 0)
    carbs = db.Column(db.Integer,default = 0)
    fats = db.Column(db.Integer,default = 0)
    total=db.Column(db.Integer,default = 0)

    def __repr__(self):
        return '<Task %r>' % self.id
def totalcal():
    tot = proteins+ carbs+fats        

@app.route("/", methods = ['POST','GET'])
def add():
    if request.method =='POST':
        add_content = request.form.get('add_food')
        add_carbs = int(request.form.get('add_carbs'))
        add_pro = int(request.form['add_pro'])
        add_fat = int(request.form['add_fats'])
        tot = add_carbs+add_pro+add_fat
        new_content = Data(content = add_content,carbs = add_carbs,proteins = add_pro,fats = add_fat,total = tot)
        try:
            db.session.add(new_content)
            db.session.commit()
            return redirect('/')
        except:
            return " Issue with the text"   
    else:
        check = Data.query.order_by(Data.date_created).all()
        return render_template('home.html',check = check)
        
@app.route('/delete/<int:id>')
def delete(id):
    content_deletion = Data.query.get_or_404(id)
        
    try:
        db.session.delete(content_deletion)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue occured with the function'

@app.route('/update/<int:id>', methods =['GET','POST'])
def update(id):
    update_content =  Data.query.get_or_404(id)
    if request.method == 'POST':
        update_content.content = request.form['add_food']
        update_content.carbs = request.form['quantity1']
        update_content.fats = request.form['quantity2']
        update_content.proteins = request.form['quantity']
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