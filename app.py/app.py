from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask application
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define class for database schema
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create database tables
with app.app_context():
    db.create_all()

# HTML template
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)  # Add to session
        db.session.commit()   # Save to the database
        
    allTodo = Todo.query.all()    # Get all records
    return render_template('index.html',allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()     # Retrieve record by id
        todo.title = title
        todo.desc = desc
        db.session.add(todo)  # Add to session
        db.session.commit()   # Save to the database
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get(sno)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')


@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is the products page'

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=8000)


