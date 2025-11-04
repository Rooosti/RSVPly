from ctypes import resize
from app import myapp_obj
from flask import Flask, request, redirect, request, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy # Added SQLAlchemy
from app.forms import *
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from app.models import Event, User, Comment, Rating # importing from models.py
from app import db
from datetime import datetime # added datetime
# from <X> import <Y>

'''
Setup instructions:

Clone repo
Navigate to folder

run: 
python3 -m venv venv
source venv/bin/activate

install necessary libraries using pip3

run in terminal:
flask shell
from app import db
db.create.all()
exit()

python3 run.py

run in terminal to stop virtual environment:

deactivate

'''

@myapp_obj.route("/")
def home_page():
    return redirect(url_for("login"))

@myapp_obj.route("/events") # http://127.0.0.1:5000/events
def view_all_events():
    events = Event.query.all() # get all events
    return render_template("hello.html", events=events)

@myapp_obj.route("/event/new", methods=['GET', 'POST']) # http://127.0.0.1:5000/event/new
@login_required
def create_event():
    form = eventForm()
    if form.validate_on_submit():
        #create event
        new_event = event(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            tags=form.tags.data,
            date=datetime.now(),
            user_id=current_user.id
        )
        db.session.add(new_event) #adding to database
        db.session.commit()
        return redirect("/")
    return render_template("new.html", form=form) #event form

@myapp_obj.route("/event/<int:integer>", methods=['GET', 'POST']) # http://127.0.0.1:5000/event/<enter number here>
@login_required
def return_event(integer):
    event = Event.query.get(integer) # get event number
    if event is None:
        print("event not found") #prints to terminal
        return ""
    
    comment_form = CommentForm() # create comment form
    rating_form = RatingForm() # create rating form

    #comment and rating form
    if comment_form.validate_on_submit() and comment_form.submit.data:
            new_comment = Comment(comment=comment_form.comment.data, user_id=current_user.id, event_id=event.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(request.path)
    
    if rating_form.validate_on_submit() and rating_form.submit.data:
        existing_rating = Rating.query.filter_by(user_id=current_user.id, event_id=event.id).first()
        if existing_rating:
            existing_rating.score = rating_form.score.data
        else:
            new_rating = Rating(score=rating_form.score.data, user_id=current_user.id, event_id=event.id)
            db.session.add(new_rating)
        
        db.session.commit()
        return redirect(request.path)

    comments = event.comments
    return render_template("return_rec.html", event=event, comment_form=comment_form, rating_form=rating_form, comments=comments)

@myapp_obj.route("/event/<int:integer>/delete") # http://127.0.0.1:5000/event/<enter number here>/delete
def delete_event(integer):
    del_rec = Event.query.get(integer) # get event number
    if current_user == del_rec.user:
        db.session.delete(del_rec) #delete
        db.session.commit()
        flash("event successfully deleted", "success")
        return redirect(url_for("login"))
    else:
        flash("You must own a event to delete it.", "error")
        return redirect(url_for("login"))

@myapp_obj.route("/registration", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data #1
        email = form.email.data
        password = form.password.data #1
        users = User.query.all()
        if email in users:
            flash("Email is taken.", 'error')
            return redirect(url_for("register"))
        else:
            u = User(username=username, email=email, password=password) #1
            db.session.add(u)#1
            db.session.commit() #1
            print(f"User registered: {username}")
        return redirect("/")
    return render_template("registration.html", form=form)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(f'/view/{current_user.username}')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and  user.password == password:
            login_user(user)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for("view_profile", username=username))
        else:
            flash('Invalid username or password.', 'error')
    return render_template("login.html", form=form)

#Favorites
@myapp_obj.route("/toggle_favorite/<int:event_id>", methods=["POST"])
@login_required
def toggle_favorite(event_id):
    event = Event.query.get(event_id)
    if event is None:
        flash("event not found", 'error')
        return redirect(url_for("main"))
    if event not in current_user.favorites:
        current_user.favorites.append(event)
        db.session.commit()
        flash("event added to favorites", 'success')
    else:
        if event in current_user.favorites:
            current_user.favorites.remove(event)
            db.session.commit()
            flash("event removed from favorites", 'success')
    return redirect(url_for("view_favorites"))

# View Favorites
@myapp_obj.route("/favorites")
@login_required
def view_favorites():
    return render_template("favorites.html", favorites=current_user.favorites)

# Log out
@myapp_obj.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out succesfully', 'success')
    return redirect("/")

# View User Profile
@myapp_obj.route('/view/<string:username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", 'error')
    return render_template("user.html", user=user)

@myapp_obj.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
    return render_template("edit_user.html", user=current_user, form=form)

@myapp_obj.route('/event/<int:integer>/edit', methods=["GET", "POST"])
@login_required
def edit_event(integer):
    form = EditeventForm()
    event = Event.query.get(integer) # get event number
    if event == None:
        flash("Event does not exist.", "error")
        return redirect(url_for("login"))
    else:
        if event.user != current_user:
            flash("You cannot edit events you don't own.", "error")
            return redirect(url_for("login"))
        if form.validate_on_submit():
            #edit event
            if form.title.data:
                event.title = form.title.data
            if form.description.data:
                event.description = form.description.data
            if form.ingredients.data:
                event.ingredients = form.ingredients.data
            if form.instructions.data:
                event.instructions = form.instructions.data
            if form.tags.data:
                event.tags = form.tags.data
            db.session.commit()
            flash("event successfully changed.", "success")
            return redirect(f"/event/{integer}")
        return render_template("edit_event.html", event=event, form=form)

@myapp_obj.route('/search', methods =['GET', 'POST'])
def search_events():
    query = request.args.get('query')
    form = SearchForm()
    if not query:
        if form.validate_on_submit():
            search_query = form.search_query.data
            
            events = Event.query.filter(
                db.or_(
                    Event.title.ilike(f'%{search_query}%'),
                    Event.description.ilike(f'%{search_query}%'),
                    Event.ingredients.ilike(f'%{search_query}%'),
                    Event.instructions.ilike(f'%{search_query}%'),
                )
            ).all()
    else:
        events = Event.query.filter(
                db.or_(
                    Event.title.ilike(f'%{query}%'),
                    Event.description.ilike(f'%{query}%'),
                    Event.ingredients.ilike(f'%{query}%'),
                    Event.instructions.ilike(f'%{query}%'),
                )
            ).all()
        return render_template('search_result.html', events = events, form = form)
    return render_template('search.html', form = form)

@myapp_obj.route('/enhanced-search', methods=['GET', 'POST'])
def enhanced_search():
    form = EnhancedSearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data
        tags_input = form.tags.data

        # Start with base query
        query = Event.query

        # Apply text search if provided
        if search_query:
            query = query.filter(
                db.or_(
                    Event.title.ilike(f'%{search_query}%'),
                    Event.description.ilike(f'%{search_query}%'),
                    Event.ingredients.ilike(f'%{search_query}%'),
                    Event.instructions.ilike(f'%{search_query}%')
                )
            )

        # Apply tag filtering if provided
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                query = query.filter(event.tags.ilike(f'%{tag_name}%'))

        events = query.all()
        return render_template('enhanced_search_result.html', events=events, form=form)
    
    return render_template('enhanced_search.html', form=form)
