from ctypes import resize
from app import myapp_obj
from flask import Flask, request, redirect, request, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy # Added SQLAlchemy
from app.forms import *
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from app.models import Event, User, EventComment, Rsvp, RsvpStatus # importing from models.py
from app import db
from datetime import datetime # added datetime

@myapp_obj.route("/")
def home_page():
    return redirect(url_for("login"))

# http://127.0.0.1:5000/events
@myapp_obj.route("/events")
def view_all_events():
    events = Event.query.all() # get all events
    return render_template("hello.html", events=events)

# http://127.0.0.1:500/event/new
@myapp_obj.route("/event/new", methods=["GET", "POST"])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # Create a new Event object
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            wishlist=form.wishlist.data,
            starts_at=form.starts_at.data,
            ends_at=form.ends_at.data,
            capacity=form.capacity.data,
            is_public=form.is_public.data,
            address_line1=form.address_line1.data,
            address_line2=form.address_line2.data,
            organizer_id=current_user.id,
        )

        # If categories are part of the form (e.g. SelectMultipleField)
        if hasattr(form, "categories") and form.categories.data:
            new_event.categories = form.categories.data

        db.session.add(new_event)
        db.session.commit()

        flash("Event created successfully!", "success")
        return redirect(url_for("return_event", integer=new_event.id))

    return render_template("new.html", form=form)

# http://127.0.0.1:5000/event/<enter number here>
@myapp_obj.route("/event/<int:integer>", methods=['GET', 'POST'])
@login_required
def return_event(integer):
    event = Event.query.get(integer) # get event number
    if event is None:
        print("event not found") #prints to terminal
        return ""
    
    # Find existing RSVP of user (if any)
    if current_user:
        rsvp = Rsvp.query.filter_by(
            user_id=current_user.id,
            event_id=event.id
        ).first()

    comment_form = CommentForm() # create comment form
    rating_form = RatingForm() # create rating form

    #comment and rating form
    if comment_form.validate_on_submit() and comment_form.submit.data:
            new_comment = EventComment(event_id=event.id, user_id=current_user.id, comment=comment_form.comment.data)
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
    return render_template("return_rec.html", event=event, comment_form=comment_form, rating_form=rating_form, comments=comments, rsvp=rsvp)

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
        #users = User.query.all()
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is taken.", 'error')
            return redirect(url_for("register"))
        u = User(username=username, email=email)
        u.set_password(password)
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
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for("view_profile", username=username))
        else:
            flash('Invalid username or password.', 'error')
    return render_template("login.html", form=form)

@myapp_obj.route("/toggle_rsvp/<int:event_id>", methods=["POST"])
@login_required
def rsvp(event_id):
    event = Event.query.get(event_id)
    if event is None:
        flash("Event not found", "error")
        return redirect(url_for("main"))

    # Find existing RSVP (if any)
    rsvp = Rsvp.query.filter_by(
        user_id=current_user.id,
        event_id=event.id
    ).first()

    if rsvp is None:
        # Create a new RSVP
        new_rsvp = Rsvp(
            user=current_user,
            event=event,
            status=RsvpStatus.going, #kind of forgot we have enums for the rsvps; just set to default "going" for RSVPs to reduce project scope
            guests_count=0
        )
        db.session.add(new_rsvp)
        db.session.commit()
        flash("Event added to RSVPs", "success")
    elif rsvp.status == RsvpStatus.going:
            flash("RSVP Removed", "success")
            db.session.delete(rsvp)
            db.session.commit()

    return redirect(url_for("return_event", integer=event.id))


# View RSVPs
@myapp_obj.route("/rsvps")
@login_required
def view_rsvps():
    rsvps = Rsvp.query.filter_by(
        user_id=current_user.id,
        status=RsvpStatus.going
    ).all()

    events = [r.event for r in rsvps]

    return render_template("rsvps.html", events=events)


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
    form = EditEventForm()
    event = Event.query.get(integer) # get event number
    if event == None:
        flash("Event does not exist.", "error")
        return redirect(url_for("login"))
    else:
        if event.organizer != current_user:
            flash("You cannot edit events you don't own.", "error")
            return redirect(url_for("login"))
    if request.method == "POST":
        if form.validate_on_submit():
            #edit event
            if form.title.data:
                event.title = form.title.data
            if form.description.data:
                event.description = form.description.data
            if form.wishlist.data:
                event.wishlist = form.wishlist.data
            if form.starts_at.data:
                event.starts_at = form.starts_at.data
            if form.ends_at.data:
                event.ends_at = form.ends_at.data
            if form.capacity.data:
                event.capacity = form.capacity.data
            event.is_public = form.is_public.data
            if form.address_line1.data:
                event.address_line1 = form.address_line1.data
            if form.address_line2.data:
                event.address_line2 = form.address_line2.data
            db.session.commit()
            flash("event successfully changed.", "success")
            return redirect(f"/event/{integer}")
    else:
        # Pre-populate form with existing event data
        form = EditEventForm(obj=event)

    # Pass both form and event to template
    return render_template("edit_event.html", form=form, event=event)

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
