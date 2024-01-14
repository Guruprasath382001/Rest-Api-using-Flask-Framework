from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Add User
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        new_user = User(name=name, contact=contact)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/all_users')
    return render_template('add_user.html')

# All Users
@app.route('/all_users', methods=['GET'])
def all_users():
    all_users = User.query.all()
    return render_template('all_users.html', users=all_users)

# Update User
@app.route('/update_user/<id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.contact = request.form['contact']
        db.session.commit()
        return redirect('/all_users')
    return render_template('update_user.html', user=user)

# Delete User
@app.route('/delete_user/<id>', methods=['GET', 'POST'])
def delete_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect('/all_users')
    return render_template('delete_user.html', user=user)

# Create database tables within the application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
