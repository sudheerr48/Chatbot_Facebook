#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 16:56:28 2018

@author: nagasudheerravela
"""

Back up

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 01:05:36 2018

@author: nagasudheerravela
"""

import spacy

nlp = spacy.load('en')

msg = " hello , can i know info about about Computers"

departments = ['cs', 'ee', 'im', 'civil' ,'mechanical' , 'computer' , 'electrical','none' ]
details = ['info','details','about','information']
INIT=0
CHOOSE_DEPARTMENT=1
RESOLVED=2
Count = 0
save_id = "none"

scores = ['Gre:310.1 , Toefl:100,GPA:- 3.5', 'Gre:310.2 , Toefl:100,GPA:- 3.5','Gre:310.3 , Toefl:100,GPA:- 3.5','Gre:310.4 , Toefl:100,GPA:- 3.5','Gre:310.5 , Toefl:100,GPA:- 3.5','Gre:310.6 , Toefl:100,GPA:- 3.5','Gre:310.7 , Toefl:100,GPA:- 3.5','none']

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
     
        
policy_rules = {
    (INIT, "info"): (INIT, "I'm a bot to help you regarding Graduate admissions at UT Tyler,What Course do u need ?"),
    (INIT, "none"): (CHOOSE_DEPARTMENT, "Please enter the departments which you want to choose 1.Electrical Enginnering , 2.Computer Science , 3.Mechanical Engineering , 4.Civil Engineering , 5.Industrial Managmenet  ?"),    
    (INIT, "department_info"): (RESOLVED, "Here is the information you needed "),
    (CHOOSE_DEPARTMENT, "department_info"): (RESOLVED, "perfect, here is the information "),
    (CHOOSE_DEPARTMENT, "none"): (CHOOSE_DEPARTMENT, "sorry,please contact ogs@uttyler.edu"),
    (RESOLVED,"none"):(RESOLVED,"Thank you"),
    (RESOLVED, "department_info"): (RESOLVED, "Thank you ")
    
}

def respond(policy_rules, state, message):
    (resp,dep) = interpret(message)
    (new_state, response) = policy_rules[(state, resp)]
    return new_state, response,dep

def send_message(policy, state, message):
    print("USER : {}".format(message))
    new_state, response,dep = respond(policy_rules, state, message)
    if new_state == RESOLVED :
       print("BOT : {0} is {1}".format(response,req[dep]))
    else:
       print("BOT : {}".format(response)) 
    return new_state


class Extra:
    next_state = 'Null'


def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    if Extra.next_state =='Null' :
             state = INIT
    else :
             state = Extra.next_state

    Extra.next_state,reply = send_message(policy_rules, state, message)
    bot_message = reply
    
    return bot_message



get_bot_response("hello")


    
    
    