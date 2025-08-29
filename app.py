from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder='static')

# static folder is added to serve CSS and JS files
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
        if title and desc:  # Only add if both fields have data
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect('/')  # Redirect after POST to prevent form resubmission
    
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
# ...................update
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/view/<int:sno>')
def view(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('view.html', todo=todo)
# end of update....................
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        # Search in both title and description
        search_results = Todo.query.filter(
            db.or_(
                Todo.title.contains(query),
                Todo.desc.contains(query)
            )
        ).all()
    else:
        search_results = []
    
    return render_template('search.html', todos=search_results, query=query)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)