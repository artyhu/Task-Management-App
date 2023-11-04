from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # checks everything is good before registering
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in database', category='error')
        elif len(email) < 3:
            flash('Email must contain more than three characters', category ='error')
        elif len(name) < 2:
            flash('Name must contain more than two characters', category ='error')
        elif password1 != password2:
            flash('Passwords do not match', category ='error')
        elif len(password1) < 6:
            flash('Password must contain more than six characters', category ='error')

        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Success! Your account has been created', category='success')
            return redirect(url_for('views.home'))
            
            
    return render_template("register.html", user=current_user)
# checks everything is good before allowing user to login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Login Successful!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Login Failed!', category='error')
        else:
            flash('Email not found', category = 'error')
    
    return render_template("login.html", user=current_user)

@auth.route('/taskmanager')
def taskManager():
    return render_template("taskManager.html", user=current_user)

@auth.route('/projectmanager')
def projectManager():
    return render_template("projectManager.html", user=current_user)

@auth.route('/newtask')
def newTask():
    return render_template("newTask.html", user=current_user)

@auth.route('/newproject', methods=['GET', 'POST'])
def newProject():
    if request.method =='POST':
        name = request.form.get('name')
        # sdate = request.form.get('sdate')
        # deadline = request.form.get('deadline')
        info = request.form.get('description')
        new_prj = Project(name=name, info=info)   
        db.session.add(new_prj)
        db.session.commit()
        flash('Project Created!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template("newProject.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/view_users')
def view_users():
    users = User.query.all()
    projects = Project.query.all()
    return render_template('view_users.html', user=current_user, users=users, projects=projects)