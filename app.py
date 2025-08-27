from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

# Initialize database at startup
# with app.app_context():
#     db.create_all()


    
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)

    def __repr__(self) -> str:
         return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    todo = Todo(title="Sample Todo", desc="This is a sample todo item.")
    db.session.add(todo)
    db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)