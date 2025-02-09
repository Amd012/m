from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Available")
    card_id = db.Column(db.String(50), nullable=True)
    date_issue = db.Column(db.String(20), nullable=True)
    date_return = db.Column(db.String(20), nullable=True)
    person_name = db.Column(db.String(100), nullable=True)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home (Dashboard)
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# Add a Book
@app.route('/add', methods=['POST'])
def add_book():
    name = request.form['name']
    author = request.form['author']
    new_book = Book(name=name, author=author)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

# Issue a Book
@app.route('/issue/<int:book_id>', methods=['POST'])
def issue_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.status = "Issued"
    book.card_id = request.form['card_id']
    book.date_issue = datetime.now().strftime('%Y-%m-%d')
    book.person_name = request.form['person_name']
    db.session.commit()
    return redirect(url_for('index'))

# Return a Book
@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.status = "Available"
    book.date_return = datetime.now().strftime('%Y-%m-%d')
    db.session.commit()
    return redirect(url_for('index'))

# Delete a Book
@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)