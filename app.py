from flask.helpers import flash
from flask_login.utils import login_required, login_user
from FDataBase import FDataBase
from sqlite3.dbapi2 import connect
from flask import Flask,render_template, request, url_for, session, abort, g
from werkzeug.utils import redirect
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user
from UserLogin import UserLogin

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'sdfwefwefsdfwef'


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)


#load and create object of UserLogin if have request from page
@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    #way to database
    conn = sqlite3.connect(app.config['DATABASE'])
    #transform rows from database to dict format 
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    #function for creating tables for db
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    #create connection to db if it not exist
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    return render_template('index.html', menu= dbase.getMenu())


@app.route('/popupForm')
def popupForm():
    return render_template('popupForm.html', menu= dbase.getMenu())


@app.route('/loginForm', methods = ['GET', 'POST'])
def loginForm():
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['UserEmail'])
        #check admin
        if user and check_password_hash(user['password'], request.form['UserPassword']) and user['rank'] == 'admin':
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('AdminProfile'))
        #check if employee
        if user and check_password_hash(user['password'], request.form['UserPassword']) and user['rank'] == 'employee':
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('EmployeeProfile'))
        #check if visitor
        if user and check_password_hash(user['password'], request.form['UserPassword']) and user['rank'] == 'visitor':
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('profile'))

        flash('Incorrect login or password')

    return render_template('popupForm.html',menu=dbase.getMenu())


#registration for users and insert to database
@app.route('/registrationForm', methods=['GET','POST'])
def registrationForm():
    if request.method == 'POST':
        if len(request.form['RegistrationEmail']) > 4 and len(request.form['RegistrationPassword']) > 4 and request.form['RegistrationPassword'] == request.form['RegistrationPassword2']:
            hash = generate_password_hash(request.form['RegistrationPassword'])
            res = dbase.addUser(request.form['RegistrationEmail'], hash)
            if res:
                flash('Thx for registration')
                return redirect(url_for('popupForm'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('popupForm.html',menu=dbase.getMenu())


@app.teardown_appcontext
def close_db(error):
    #closing connection to db if it exist
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Goodbye ;)")
    return redirect(url_for('loginForm'))


#profile for visitors without extra functions
@app.route('/profile')
@login_required
def profile():
    return render_template('UserProfile.html', menu=dbase.getMenu())


#profile for employee with medium functions
@app.route('/EmployeeProfile')
@login_required
def EmployeeProfile():
    if current_user.getRank() != 'employee':
        abort(404)
    return render_template('EmployeeProfile.html', menu=dbase.getMenu())


#profile for admin - full access to DB
@app.route('/AdminProfile')
@login_required
def AdminProfile():
    if current_user.getRank() != 'admin':
        abort(404)
    return render_template('AdminProfile.html', menu=dbase.getMenu())


#add employee by admin
@app.route('/AddEmployeeByAdmin', methods = ['GET', 'POST'])
@login_required
def AddEmployeeByAdmin():
    if request.method == 'POST':
        if len(request.form['AddByAdminEmail']) > 4 and len(request.form['AddByAdminPsw']) > 4 and request.form['AddByAdminPsw'] == request.form['AddByAdminPsw1']:
            hash = generate_password_hash(request.form['AddByAdminPsw'])
            res = dbase.addEmployee(request.form['AddByAdminEmail'], hash)
            if res:
                flash('Success add employee')
                return redirect(url_for('AdminProfile'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('AdminProfile.html', menu=dbase.getMenu())


#Add car by admin
@app.route('/AddCarByAdmin', methods = ['GET', 'POST'])
@login_required
def AddCarByAdmin():
    if request.method == 'POST':
        if len(request.form['CarModel']) > 4 and len(request.form['CarNumber']) > 4 and len(request.form['CarPrice']) >= 4:
            res = dbase.AddCarByAdmin(request.form['CarModel'],request.form['CarNumber'],request.form['CarPrice'])
            if res:
                flash('Success add car')
                return redirect(url_for('AdminProfile'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('AdminProfile.html', menu=dbase.getMenu())


#add client by employee
@app.route('/AddClientByEmployee', methods = ['GET', 'POST'])
@login_required
def AddClientByEmployee():
    if request.method == 'POST':
        if len(request.form['ClientName']) > 3 and len(request.form['ClientSurname']) > 3 and len(request.form['ClientPhone']) >= 2:
            res = dbase.AddClientByEmployee(request.form['ClientName'], request.form['ClientSurname'],request.form['ClientPhone'], current_user.get_id())
            if res:
                flash('Success add client')
                return redirect(url_for('EmployeeProfile'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('EmployeeProfile.html', menu=dbase.getMenu())


#add fine to client by employee
@app.route('/AddFinesToClient', methods = ['GET', 'POST'])
@login_required
def AddFinesToClient():
    if request.method == 'POST':
        if len(request.form['ClientName']) != 0 and len(request.form['ClientSurname']) != 0 and len(request.form['Reason']) != 0 and len(request.form['FineSum']) >= 3:

            clientID = dbase.getClientIDbyNameAndSurname(request.form['ClientName'], request.form['ClientSurname'])[0]

            res = dbase.AddFinesToClient(clientID, request.form['Reason'],request.form['FineSum'], current_user.get_id())
            if res:
                flash('Success add fine')
                return redirect(url_for('EmployeeProfile'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('EmployeeProfile.html', menu=dbase.getMenu())


#add fine to client by employee
@app.route('/AddReservation', methods = ['GET', 'POST'])
@login_required
def AddReservation():
    if request.method == 'POST':
        if len(request.form['ClientName']) != 0 and len(request.form['ClientSurname']) != 0 and len(request.form['CarModel']) != 0 and len(request.form['Time']) >= 3:

            clientID = dbase.getClientIDbyNameAndSurname(request.form['ClientName'], request.form['ClientSurname'])[0]

            carID = dbase.getCarIDByModel(request.form['CarModel'])[0]

            res = dbase.AddReservation(clientID, carID,request.form['Time'], current_user.get_id())

            if res:
                flash('Success add reservation')
                return redirect(url_for('EmployeeProfile'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('EmployeeProfile.html', menu=dbase.getMenu())


#Add record by employee
@app.route('/AddRecord', methods = ['GET', 'POST'])
@login_required
def AddRecord():
    if request.method == 'POST':
        if len(request.form['ClientName']) != 0 and len(request.form['ClientSurname']) != 0 and len(request.form['CarModel']) != 0 and len(request.form['Hours']) != 0 :

            clientID = dbase.getClientIDbyNameAndSurname(request.form['ClientName'], request.form['ClientSurname'])[0]

            carID = dbase.getCarIDByModel(request.form['CarModel'])[0]

            RecordSum = dbase.getPriceByCarID(carID)[0] * int(request.form['Hours'])

            res = dbase.AddRecord(clientID,carID, current_user.get_id(), RecordSum)

            if res:
                flash('Success add reservation')
                return redirect(url_for('EmployeeProfile'))
            else:
                flash('Error with database')
        else:
            flash('incorrect input')
    return render_template('EmployeeProfile.html', menu=dbase.getMenu())


@app.route('/listofclients')
@login_required
def listofclients():
    if current_user.getRank() != 'admin':
        abort(404)
    return render_template('listofclients.html', lines=dbase.GetAllClients())


@app.route('/listofcars')
@login_required
def listofcars():
    if current_user.getRank() != 'admin':
        abort(404)
    return render_template('listofcars.html', lines=dbase.GetAllCars())


#http://26.96.203.29:5000/
#host='0.0.0.0', port=5000,


if __name__ == "__main__":
    app.run(debug=True)