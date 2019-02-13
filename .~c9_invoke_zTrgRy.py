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

@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
    )
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)