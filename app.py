from flask import Flask, url_for, render_template, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_migrate import Migrate

app = Flask(__name__, template_folder= "templates")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dkfalkd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

class Module1(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)

class Module2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    module1_id = db.Column(db.Integer, db.ForeignKey('module1.id'), nullable=False)
    module1 = db.relationship('Module1', backref='module2', lazy=True)

@app.route("/")
def base():
    return render_template('base.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
        user = User(username = username, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('successfully created an account')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # Correct the variable assignment
        password = request.form['password']  # Correct the variable assignment
        user = User.query.filter_by(username=username).first()  # Correct the usage of 'username'
        if user and bcrypt.check_password_hash(user.password, password):
            flash('Login successful')
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check your credentials')
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('logout')
    return redirect(url_for('login'))

@app.route('/module1', methods=['GET', 'POST'])
def module1():
    if request.method == 'POST':
       name = request.form['name']
       description = request.form['description']
       module1 = Module1(name= name, description= description)
       db.session.add(module1)
       db.session.commit()
       flash('module1 is created successfully')
    module1_records=  Module1.query.all()
    return render_template('module1.html', module1_records = module1_records)

@app.route('/module1/add', methods=['GET', 'POST'])
def add_module1():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        module1 = Module1(name= name, description = description)
        db.session.add(module1)
        db.session.commit()
        flash('module1 is added succressfully')
    return render_template('add_module1.html')

@app.route('/module1/edit/<int:id>', methods =['POST', 'GET'])
def edit_module1(id):
    module1 = Module1.query.get(id)
    if request.method == 'POST':
        module1.name = request.form['name']
        module1.description = request.form['description']
        db.session.commit()
        flash('module is edit successfully')
        return redirect(url_for('module1'))
    return render_template('edit_module1.html', module1 = module1)

@app.route('/module1/delete/<int:id>', methods=['POST'])
def delete_module1(id):
    module1 = Module1.query.get(id)
    db.session.delete(module1)
    db.session.commit()
    flash('module1 is deleted successfully')
    return redirect(url_for('module1'))
@app.route('/module2', methods=['GET', 'POST'])
def module2():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        module1_id = request.form['module1_id']

        module2 = Module2(name=name, description=description, module1_id=module1_id)
        db.session.add(module2)
        db.session.commit()
        flash('Module 2 record created successfully!', 'success')

    module2_records = Module2.query.all()
    return render_template('module2.html', module2_records=module2_records)

@app.route('/module2/add', methods=['GET', 'POST'])
def add_module2():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        module1_id = request.form['module1_id']

        module2 = Module2(name=name, description=description, module1_id=module1_id)
        db.session.add(module2)
        db.session.commit()
        flash('Module 2 record created successfully!', 'success')
        return redirect(url_for('module2'))

    # You might want to provide options for selecting the related Module1 here
    module1_options = Module1.query.all()

    return render_template('add_module2.html', module1_options=module1_options)

@app.route('/module2/edit/<int:id>', methods=['GET', 'POST'])
def edit_module2(id):
    module2 = Module2.query.get(id)

    if request.method == 'POST':
        module2.name = request.form['name']
        module2.description = request.form['description']
        db.session.commit()
        flash('Module 2 record updated successfully!', 'success')
        return redirect(url_for('module2'))

    return render_template('edit_module2.html', module2=module2)

@app.route('/module2/delete/<int:id>', methods=['POST'])
def delete_module2(id):
    module2 = Module2.query.get(id)
    db.session.delete(module2)
    db.session.commit()
    flash('Module 2 record deleted successfully!', 'success')
    return redirect(url_for('module2'))



@app.route('/complete_data')
def complete_data():
    module1_data = Module1.query.all()
    module2_data = Module2.query.all()

    return render_template('complete_data.html', module1_data=module1_data, module2_data=module2_data)

if __name__=='__main__':
    app.run(debug=True)