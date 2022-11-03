from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db
from .models import User


#create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    if (register.validate_on_submit() == True):
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            number = register.contact_num.data
            street_address= register.streetAddress.data
            
            #check if a user exists
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            # don't store the password - create password hash
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email, 
                            contactNum=number, address=street_address)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')


@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
     print('In Login View function')
     login_form = LoginForm()
     error=None
     if(login_form.validate_on_submit()==True):
         user_name = login_form.user_name.data
         password = login_form.password.data
         u1 = User.query.filter_by(name=user_name).first()
         #If there is no user with that name saved in
         if u1 is None:
             error='Incorrect user name'
         elif not check_password_hash(u1.password_hash, password): # takes the hash and password
             error='Incorrect password'
         if error is None:
             login_user(u1)
             return redirect(url_for('main.index'))
         else:
             flash(error)
     return render_template('user.html', form=login_form, heading='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You have been logged out'