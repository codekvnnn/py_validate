from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),sightings=Sighting.get_all())

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('create_sightings.html')

@app.route('/create',methods=['POST'])
def create():
    if not Sighting.validate(request.form):
        return redirect('/new')  
    Sighting.save(request.form)
    return redirect('/dashboard')

@app.route('/update/<id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/login')
    print(Sighting.select_one({"id": id}))
    return render_template('edit_sightings.html',user=User.get_by_id({"id":session['user_id']}),item=Sighting.select_one({"id": id}))

@app.route('/process',methods=['POST'])
def process_edit():
    if not Sighting.validate(request.form):
        return redirect(f'/update/{request.form["id"]}')  
        # return redirect('/new')  

    Sighting.update(request.form)
    return redirect('/dashboard')

@app.route('/view/<id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/login')
    print(Sighting.select_one({"id": id}))
    return render_template('view_sightings.html',user=User.get_by_id({"id":session['user_id']}),item=Sighting.select_one({"id": id}))

@app.route('/delete/<id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/login')
    Sighting.delete({"id": id})
    return redirect('/dashboard')