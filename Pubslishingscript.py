#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 15:02:52 2018

@author: nagasudheerravela
"""

#importing Necessary packages
from flask import Flask, request
import requests
import spacy


app = Flask(__name__)


FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = ''# <You have to generate a token , you can generate it by running  >
PAGE_ACCESS_TOKEN = ''# This token will be obtained from facebook>"





nlp = spacy.load('en')
departments = ['cs', 'ee', 'im', 'civil' ,'mechanical' , 'computer' , 'electrical','none' ]
details = ['info','details','about','information']
INIT=0
CHOOSE_DEPARTMENT=1
RESOLVED=2
Count = 0


scores = ['Gre:some scores1 , Toefl: some scores1 ,GPA:-  some scores1 ', 'Gre:some scores2 , Toefl: some scores2 ,GPA:-  some scores2','Gre:Gre:some scores3 , Toefl: some scores3 ,GPA:-  some scores3','Gre:some scores4 , Toefl: some scores4 ,GPA:-  some scores4','Gre:some scores5 , Toefl: some scores5 ,GPA:-  some scores5','Gre:some scores 6 , Toefl: some score6 ,GPA:-  some scores6','Gre:somescoere7 , Toefl:somescore7,GPA:- somescore8','none']

req = dict(zip(departments,scores))

def interpret(message):
    msg = message.lower()
    doc = nlp(msg)
    save_id = "none"
    Count = 0
    for token in doc:
           if token.text in details:
                 Count =Count + 1
           if token.text in departments: 
               save_id = token.text
               Count =Count + 5
            
    if Count <5:
       if Count==0:
            return "none",save_id
       else:
            return "info",save_id
    else:
         return "department_info",save_id  
     
        
def responds(policy_rules, state, message):
    (resp,dep) = interpret(message)
    (new_state, response) = policy_rules[(state, resp)]
    return new_state, response,dep


def send_messages(policy, state, message):
    
    new_state, response,dep = responds(policy_rules, state, message)
    if new_state == RESOLVED :
       reply = "BOT : {0} is {1}".format(response,req[dep])
    else:
       reply = "BOT : {}".format(response) 
    return new_state,reply



policy_rules = {
    (INIT, "info"): (INIT, "I'm a bot to help you regarding Graduate admissions at UT Tyler,What Course do u need ?"),
    (INIT, "none"): (CHOOSE_DEPARTMENT, "Please enter the departments which you want to choose 1.Electrical Enginnering , 2.Computer Science , 3.Mechanical Engineering , 4.Civil Engineering , 5.Industrial Managmenet  ?"),    
    (INIT, "department_info"): (RESOLVED, "Here is the information you needed "),
    (CHOOSE_DEPARTMENT, "department_info"): (RESOLVED, "perfect, here is the information "),
    (CHOOSE_DEPARTMENT, "none"): (CHOOSE_DEPARTMENT, "sorry,please contact ogs@uttyler.edu"),
    (RESOLVED,"none"):(RESOLVED,"Thank you"),
    (RESOLVED, "department_info"): (RESOLVED, "Thank you ")
    
}

class Extra:
    next_state = 'Null'


def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    if Extra.next_state =='Null' :
             state = INIT
    else :
             state = Extra.next_state

    Extra.next_state,reply = send_messages(policy_rules, state, message)
    bot_message = reply
    print(bot_message)
    return bot_message

    
    


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook",methods=['GET','POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"
    


def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()
    