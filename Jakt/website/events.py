from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Purchased
from .forms import CommentForm, EventForm, TicketForm, EditForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

bp = Blueprint('event', __name__, url_prefix='/events')

@bp.route('/<id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    commentForm = CommentForm()
    ticketForm = TicketForm()
    return render_template('events/show.html', event=event, form=commentForm, Tform = ticketForm)

@bp.route('/<id>/update')
def show_edit(id):
    event = Event.query.filter_by(id=id).first()
    editForm = EditForm()
    return render_template('events/update.html', event=event, Eform = editForm)
  


@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    event=Event(name=form.name.data, description=form.description.data, 
    image=db_file_path, venue=form.venue.data, date=form.date.data, start_time=form.start_time.data,
    end_time=form.end_time.data, genre=form.genre.data, status=form.status.data, price=form.price.data,
    tickets=form.tickets.data, user=current_user)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    print('Successfully created new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

#Checks the uploaded file is valid and returns it
def check_upload_file(form):
  fp=form.image.data
  filename=fp.filename
  BASE_PATH=os.path.dirname(__file__)
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  db_upload_path='/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<event>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event_obj, user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    return redirect(url_for('event.show', id=event))
  
@bp.route('/<event>/tickets', methods = ['GET', 'POST'])  
@login_required
def tickets(event):  
    Tform = TicketForm()
    update=db.session.query(Event).filter_by(id=event).first()
    if Tform.validate_on_submit():
        if (update.tickets >= int(Tform.tickets.data)):
            #get the adjusted total ticket amount and update database
            update.tickets = (update.tickets - int(Tform.tickets.data))
            purchase = Purchased(event=update.name, image=update.image, ticket_number = int(Tform.tickets.data), user_id=update.user_id)
            db.session.add(purchase)  
            flash('Your purchase has been processed. Your order ID is {0}'.format(update.id)) 
        else:
            flash('Your purchase exceeds the number of tickets available. There are {0} tickets left'.format(update.tickets))
        if (update.tickets == 0):
          #if total event tickets = 0 label event as sold-out
          update.status = "Sold-out"
        #commit all changes to database
        db.session.commit() 
    return redirect(url_for('event.show', id=event))


@bp.route('/<event>/update/edit', methods = ['GET', 'POST'])
@login_required
def edit(event):
  update=db.session.query(Event).filter_by(id=event).first()
  Eform = EditForm(obj=update)
  if Eform.delete.data:
    db.session.delete(update)
    db.session.commit()
    print('Successfully deleted event')
    #Always end with redirect when form is valid
    return redirect(url_for('event.edit', event=event))
  #update the details
  if Eform.validate_on_submit():
    update.name = Eform.name.data
    update.description = Eform.description.data
    update.image=check_upload_file(Eform)
    update.venue = Eform.venue.data
    update.date = Eform.date.data
    update.start_time = Eform.start_time.data
    update.end_time = Eform.end_time.data
    update.genre = Eform.genre.data
    update.status = Eform.status.data
    update.price = Eform.price.data
    update.tickets = Eform.tickets.data  
    # commit to the database
    db.session.commit()
    print('Successfully edited event')
    #Always end with redirect when form is valid
    return redirect(url_for('event.edit', event=event))
  return render_template('events/update.html', Eform=Eform)


