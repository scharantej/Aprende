 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spanish_learning_plan.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class LearningPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('learning_plans', lazy=True))

    def __repr__(self):
        return '<LearningPlan %r>' % self.title

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learning_plan_id = db.Column(db.Integer, db.ForeignKey('learning_plan.id'), nullable=False)
    learning_plan = db.relationship('LearningPlan', backref=db.backref('progress', lazy=True))
    date = db.Column(db.Date, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Progress %r>' % self.date

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Resource %r>' % self.title

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/learning_plans')
def learning_plans():
    return render_template('learning_plans.html')

@app.route('/progress_tracking')
def progress_tracking():
    return render_template('progress_tracking.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
