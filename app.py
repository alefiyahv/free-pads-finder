from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libraries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    has_period_products = db.Column(db.Boolean, default=False)
    hours_open = db.Column(db.String(100), nullable=False)

if not os.path.exists('libraries.db'):
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_library', methods=['GET', 'POST'])
def add_library():
    if request.method == 'POST':
        data = request.form
        try:
            new_library = Library(
                name=data['name'],
                address=data['address'],
                zip_code=data['zip_code'],
                hours_open=data['hours_open'],
                has_period_products='has_period_products' in data
            )
            db.session.add(new_library)
            db.session.commit()
            return render_template('success.html', message="Library added successfully!")
        except KeyError as e:
            return render_template('error.html', message=f"Missing field: {str(e)}")
        except ValueError as e:
            return render_template('error.html', message=f"Invalid field value: {str(e)}")
    return render_template('add_library.html')

@app.route('/libraries', methods=['GET'])
def get_libraries():
    zip_code = request.args.get('zip_code')
    if zip_code:
        libraries = Library.query.filter_by(zip_code=zip_code, has_period_products=True).all()
    else:
        libraries = Library.query.filter_by(has_period_products=True).all()

    return render_template('libraries.html', libraries=libraries)

if __name__ == '__main__':
    app.run(debug=True)
