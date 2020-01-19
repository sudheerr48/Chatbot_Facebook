#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 19:42:43 2018

@author: nagasudheerravela
"""

# Define the INIT state
INIT = 0

# Define the CHOOSE_COFFEE state
CHOOSE_COURSE = 1

# Define the ORDERED state
ORDERED = 2

# Define the policy rules
policy = {
    (INIT, "ask_explanation"): (INIT, "I'm a bot to help you regarding Graduate admissions at UT Tyler"),    
    (INIT, "info"): (CHOOSE_COURSE, "Which course  COMPUTER SCIENCE or ELECTRICAL ENGINEERING?"),
    (INIT, "none"): (INIT, "Thank's for contacting gradbot ,how can I help you today "),
    (CHOOSE_COURSE, "specify_course"): (ORDERED, "perfect, the beans are on their way!"),
    (CHOOSE_COURSE, "none"): (CHOOSE_COURSE, "I'm sorry - would you like to know about COMPUTER SCIENCE or ELECTRICAL ENGINEERING?"),
}

# Create the list of messages
messages = [
    "I'd like to know  about Courses",
    "cs",
    "well then I'd like to info about courses",
    "my favourite animal is a zebra",
    "cs"
]

def interpret(message):
    msg = message.lower()
    if 'info' in msg:
        return 'info'
    if 'what' in msg:
        return 'ask_explanation'
    if 'cs' in msg or 'ee' in msg:
        return 'specify_course'
    return 'none'

def respond(policy, state, message):
    (new_state, response) = policy[(state, interpret(message))]
    return new_state, response

def send_message(policy, state, message):
    print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state

# Call send_message() for each message
state = INIT
for message in messages:    
    state = send_message(policy, state, message)

