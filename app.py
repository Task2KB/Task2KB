from crypt import methods
import re
from collections import Counter

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

import requests
import json

from flask_frozen import Freezer

app = Flask(__name__)
# freezer = Freezer(app)


@app.route('/task_steps/', methods=['POST', 'GET'])
def task_steps():
    if request.method == 'GET':
        task = request.values.get('task')
        if task == None:
            task = "Roast A Chicken"
        response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?task_step=' + task)
        response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
        data = json.loads(response_json) 

        related_article_response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?related_article=' + task)
        related_article_response_json = list(filter(None, related_article_response.content.decode('UTF-8').split('\n')))[0]
        related_article_data = json.loads(related_article_response_json)
            
        article_response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?advance_taskinfo=' + task)
        article_json = list(filter(None, article_response.content.decode('UTF-8').split('\n')))[0]
        article_data = json.loads(article_json)

        return render_template('task_steps.html', task=data['Task Name'], related_article=related_article_data['Related Wikihow Articles'], 
        steps=data['Methods'][0]['Steps:'][1:], questions=article_data['Questions'], reviews=article_data['Reviews'], 
        summary_text=article_data['Summary Text'], tips=article_data['Tips'],
        author_credibility=article_data['Author Credibility'])
    else:
        return render_template('index.html')

# @app.route('/task/', methods=['GET','POST'])
# def task():
#     task = request.form['todo-task-search']
#     if task == None:
#         task = "roast chicken"
#         similar_task = []
#         return render_template('task.html', task=task, similar_task=similar_task) 
#     response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?task=' + task)
#     response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
#     data = json.loads(response_json)
#     return render_template('task.html', task=data['Query'], similar_task=data['Similar Task']) 
    # if request.method == 'POST':
    #     if 'todo-task-search' in request.form.keys():
    #         task = request.form['todo-task-search']
    #         response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?task=' + task)
    #         response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
    #         data = json.loads(response_json)
    #         return render_template('task.html', task=data['Query'], similar_task=data['Similar Task']) 
    # else:
        # return render_template('task.html', task='roast a chicken', similar_task=[])


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'todo-task-search' in request.form.keys():
            task = request.form['todo-task-search']
            response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?task=' + task)
            response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
            data = json.loads(response_json)
            return render_template('task.html', task=data['Query'], similar_task=data['Similar Task']) 
        elif 'article-search' in request.form.keys():
            article = request.form['article-search']
            response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?related_article=' + article)
            response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
            data = json.loads(response_json)
            return render_template('article.html', article=article, related_article=data['Related Wikihow Articles']) 
        if 'task-step-search' in request.form.keys():
            task = request.form['task-step-search']
            response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?task_step=' + task)
            response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
            data = json.loads(response_json)

            related_article_response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?related_article=' + task)
            related_article_response_json = list(filter(None, related_article_response.content.decode('UTF-8').split('\n')))[0]
            related_article_data = json.loads(related_article_response_json)
            
            article_response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?advance_taskinfo=' + task)
            article_json = list(filter(None, article_response.content.decode('UTF-8').split('\n')))[0]
            article_data = json.loads(article_json)
            
            return render_template('task_steps.html', task=data['Task Name'], related_article=related_article_data['Related Wikihow Articles'], 
            steps=data['Steps'], questions=article_data['Questions'], reviews=article_data['Reviews'], 
            summary_text=article_data['Summary Text'], tips=article_data['Tips'],
            author_credibility=article_data['Author Credibility']) 
    else:
        return render_template('index.html')


@app.route('/topical_view/', methods=['POST', 'GET'])
def topical_view():
    if request.method == 'GET':
        response = requests.get('http://testproject-env.eba-fiuseaax.us-east-1.elasticbeanstalk.com/WikiHowKB.jsp?topic_stat=true')
        response_json = list(filter(None, response.content.decode('UTF-8').split('\n')))[0]
        data = json.loads(response_json) 
        # print(data)
        return render_template('topical_view.html', topical_data=data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.debug = False
    # app.testing = True
    # freezer.freeze()
