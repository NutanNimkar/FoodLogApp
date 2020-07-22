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
    rand = random.randint(20,400)
    rand1 = random.randint(20,200)
    rand2 = random.randint(15,100) 
    tot = rand+rand1+rand2
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    proteins = db.Column(db.Integer,default = rand1)
    carbs = db.Column(db.Integer,default = rand)
    fats = db.Column(db.Integer,default = rand2)
    total=db.Column(db.Integer,default = tot)

    def __repr__(self):
        return '<Task %r>' % self.id
def totalcal():
    tot = proteins+ carbs+fats        

@app.route("/", methods = ['POST','GET'])
def add():
    if request.method =='POST':
        add_content = request.form['add_notes']
        #add_carbs = int(request.form['add_carbs'])
        # add_pro = int(request.form['add_pro'])
        # add_fat = int(request.form['add_fats'])
        new_content = Data(content = add_content)
        #new_carbs = Data(carbs = add_carbs)
        # new_pro = Data(proteins = add_pro)
        # new_fat = Data(fats = add_fat)
        try:
            db.session.add(new_content)
            #db.session.commit()
            # db.session.add(new_carbs)
            # db.session.add(new_pro)
            # db.session.add(new_fat)
            db.session.commit()
            return redirect('/')
        except:
            return " Issue with the text"
        try:
            db.session.add(new_carbs)
            db.session.commit()
        except:
            return "Issue with the text2"    
    else:
        check = Data.query.order_by(Data.date_created).all()
        return render_template('home.html',check = check)

@app.route("/", methods = ['GET','POST'])
def carbs():
    rand = random.randint(0,100)
    if request.method =='POST':
        carb_add = request.form1['add_carbs']
        carb_data = Data(carbs = carb_add)
        
        try:
            db.session.add(carb_data)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue with the entry"    
    else:
        check = Data.query.order_by(Data.date_created).all()
        return render_template('home.html',check = check)
        
@app.route("/", methods = ['GET','POST'])
def proteins():
    if request.method =='POST':
        proadd = int(request.form2['quantity'])
        prodata = Data(proteins = proadd)
        try:
            db.session.add(carb_data)
            db.session.commit()
            return carb_data
        except:
            return "Issue with the entry"    
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
        update_content.content = request.form['content']
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