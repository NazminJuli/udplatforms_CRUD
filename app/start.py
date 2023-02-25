from flask import Flask, render_template, request, \
    session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import sqlite3


app = Flask(__name__, template_folder='C:/Users/MTT/PycharmProjects/udplatforms/templates')

SECRET_KEY = 'secret key'

# Configure Flask by providing the SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/MTT/PycharmProjects/udplatforms/app/database1.db'

app.config['SECRET_KEY'] = SECRET_KEY

# Model declaration
db = SQLAlchemy(app)


class Parents(db.Model):
    # parent model
    __tablename__ = 'parent'
    # unique user id
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    # Here for simplicity parent's name field has been made as UNIQUE
    firstname = db.Column(db.String(25), unique=True, nullable=False)
    lastname = db.Column(db.String(25), unique=True, nullable=False)
    street = db.Column(db.String(25), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip_code = db.Column(db.String(25), nullable=False)

    # make a relationship with 'Child' model
    parent_child_relation = db.relationship("Child", backref=db.backref("parent"), cascade="all, delete-orphan")


    def __init__(self, firstname, lastname, street, city, state, zip_code):
        self.firstname = firstname
        self.lastname = lastname
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code


class Child(db.Model):
    # Child model
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)

    child_firstname = db.Column(db.String(25), unique=False, nullable=False)
    child_lastname = db.Column(db.String(25), unique=False, nullable=False)

    # make a relationship with 'Child' model
    parent_id = db.Column(db.Integer, ForeignKey('parent.id'), nullable=False)

    def __init__(self, child_firstname, child_lastname, parent_id):
        self.child_firstname = child_firstname
        self.child_lastname = child_lastname
        self.parent_id = parent_id


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    print("In Home page")
    return render_template('home.html')


@app.route('/register', methods=["POST","GET"])
def register():

    if request.method == "POST":
       #if session['firstname'] and session['lastname'] is None:
        try:
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            street = request.form.get('street')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip_code')

            session['firstname'] = firstname
            session['lastname'] = lastname

            if firstname == '' or lastname == '' or street == '' or city == '' or state == '' or zip_code == '':
                flash("Please enter all input fields!")
                return redirect(url_for("register", status="disabled"))

            if db.session.query(Parents).filter_by(firstname=firstname).scalar() or db.session.query(Parents).filter_by(lastname=lastname).scalar() is not None:
                flash("User already exists!", "Register with new name")
                return redirect(url_for("register", status="disabled"))

            parent_entry = Parents(firstname=firstname, lastname=lastname, street=street, city=city, state=state, zip_code=zip_code)
            #print('', session['firstname'])
            db.session.add(parent_entry)
            db.session.commit()
            db.session.flush()

            session['parentid'] = parent_entry.id

            if "btn1" in request.form: # save
                print("parent ID", session['parentid'])
                flash('Parent Successfully saved!', "Child not added")
                return render_template("abc.html") # after saving render to search page

            if "btn2" in request.form: #add child
                print("parent ID .....", session['parentid'])
                flash('Parent Successfully saved!', "now add child")
                return render_template("addchild.html")
        except Exception:
            db.session.rollback()
            print(Exception)
    return render_template('home.html', status="disabled")


@app.route("/addchild", methods=["POST", "GET"])
def addchild():
    print("now in add-child..........")
    if request.method == "POST":

            child_firstname = request.form.get('child_firstname')
            child_lastname = request.form.get('child_lastname')
            #print("parent id in child page, childs name", session['parentid'], child_firstname,child_lastname)
            child_entry = Child(child_firstname=child_firstname, child_lastname=child_lastname, parent_id = session['parentid'])

            db.session.add(child_entry)
            db.session.commit()
            db.session.flush()
            #flash("child added succesfully")

            if "btn1" in request.form: #add child
                flash("child added succesfully")
                return redirect('/addchild')
            if "btn2" in request.form:
                return render_template('abc.html') #save children and render to search page

    return render_template('addchild.html', status = "disabled")


# Edit Parent's Address
@app.route('/edit_parent', methods=["POST", "GET"])
def edit_parent():
    if request.method == "POST":

     try:
            #firstname = request.form.get('firstname')
            #lastname = request.form.get('lastname')
            street = request.form.get('street')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip_code')

            query_parent = db.session.query(Parents).filter(Parents.firstname.like(session['name1']), Parents.lastname.like(session['name2'])).update({"street": street, "city": city, "state": state, "zip_code": zip_code})

            db.session.commit()
            flash("Seems Your address has been modified!!!!")
            return redirect(url_for('search')) # redirect to search page after update

     except sqlite3.Error as e:
            print("Database integrity error")
            print(e)

    return render_template('edit.html', status = "disabled")


# Delete parents along with it's child
@app.route('/delete', methods=["POST", "GET"])
def delete():
    print("session in delete:", session['name1'], session['name2'])

    parent = Parents.query.filter_by(id=session['parentID']).first()
    print(parent)
    if parent:
        db.session.delete(parent)
        db.session.commit()
        session.pop('parentID', default=None)
        session.pop('firstname', default=None)
        session.pop('lastname', default=None)

        flash('Looks like you have deleted your account!', "success")
    # flash("Parent deleted")
    return redirect('/search')


# search parent details based on firstname and lastname
@app.route('/search', methods=["POST", "GET"])
def search():
    print("In search......")
    if request.method == "POST":
        firstname1 = request.form.get('firstname')
        lastname1 = request.form.get('lastname')


        if firstname1 == '' or lastname1 == '':
            flash("please fill registered firstname and lastname")
            return render_template('abc.html')

        query_parent_id = db.session.query(Parents.id).filter(Parents.firstname.like(firstname1), Parents.lastname.like(lastname1)).scalar()
        if query_parent_id:
            query_parent_all = db.session.query(Parents).filter(Parents.firstname.like(firstname1),Parents.lastname.like(lastname1))

            session['parentID'] = query_parent_id
            print("id...", session['parentID'])
            query_child = db.session.query(Child).filter_by(parent_id = query_parent_id)
            # print("parent table:", query_parent)
            # print("child table:", query_child)
            return render_template('search.html', query_parent_all = query_parent_all, query_child=query_child)
    return render_template('abc.html', status = "disabled")


if __name__ == '__main__':
    app.run(debug=True)

