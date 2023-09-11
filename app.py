from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text):
        self.text = text
        
with app.app_context():       
    db.create_all()
    
        

@app.route('/', methods = ['POST', 'GET'])
def todo_app():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        todo = Todo(title = title, description = desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo = allTodo)

@app.route('/prod')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page' 

@app.route('/update/<int:sno>', methods = ['POST', 'GET'] )
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
            
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        text = request.form.get('feedback')
        if text:
            new_feedback = Feedback(text=text)
            db.session.add(new_feedback)
            db.session.commit()
            print(f"Added feedback: {text}")
    return redirect("/about")


@app.route('/view_feedback')
def view_feedback():
    feedback_records = Feedback.query.all()
    print(feedback_records)
    
    
    return render_template('feedback.html', feedback_records=feedback_records)

if __name__ == "__main__":
    app.run(debug= True, port = 8000)