import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Add configuration
app.config["MONGO_DBNAME"] = 'task-manager'
app.config["MONGO_URI"] = 'mongodb://admin:Strat3gic@ds029575.mlab.com:29575/task-manager'

mongo = PyMongo(app) # Create an instance of PyMongo

@app.route('/')
@app.route('/get_tasks') # This will be the default function called
def get_tasks():
    return render_template("tasks.html", # When get_tasks is called, it will redirect to tasks.html
    tasks=mongo.db.tasks.find()) # Using the find method (function?) all the tasks from the database will be returned

# Add task takes the user to the add task page
@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
    categories=mongo.db.categories.find())

# Insert task allows the user to add a new task to the database
@app.route('/insert_task', methods=['POST']) # Because you're using POST here, you have to set that via methods
def insert_task():
    tasks = mongo.db.tasks # Get the tasks collection
    tasks.insert_one(request.form.to_dict()) # Whenever you submit something, it is submitted as a request object. We need to convert to a dictionary so that it can be understood by mongo
    return redirect(url_for('get_tasks')) # Once submitted, we redirect to get_tasks (the function above) so that we can view our collection

@app.route('/edit_task/<task_id>')
# This function essential gets the task that matches this task id
def edit_task(task_id):
    # So we want to find on particular task from the task collection
    # We're looking for a match for the ID
    # We wrap task_id with ObjectId in order to make it a format acceptable to mongodb
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    # We also need a list of all the categories in order to populate the edit form
    all_cats = mongo.db.categories.find()
    # Render edit_task.html and pass across the_task and cats
    return render_template('edittask.html', task=the_task, cats=all_cats)
    
@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id): # We pass in the task_id as that is the hook into the 'primary key' (not strictly correct terminology as this is not a relational database)
    tasks = mongo.db.tasks # Access the tasks collection
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get['task_name'],
        'category_name': request.form.get['category_name'],
        'task_description': request.form.get['task_description'],
        'due_date': request.form.get['due_date'],
        'is_urgent': request.form.get['is_urgent']
    })
    return redirect(url_for('get_tasks'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)