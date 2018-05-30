import base64
#Base64 is an encoding..if you go to https://newspy.herokuapp.com and search for a website to generate a screenshot it will be in base 64..nothing special

import gc 
#GC stands for Garbage COllector it is rarely used but i 'might' need it(gc clears memory..i.e garbage from memory)

from flask import Flask, redirect, render_template, request, session, url_for
#This is the main thing Flask is a micro framework that allows you to build and serve websites from flask we are importing
#a)Flask..the main thing b)redirect..it allows us to redirect users from the server(this is how bit.ly works)
#c) render_template:this is important 
# it allows you to use python variables in an html page to manipulate  and then serve it to the user
# (the python work is done before serving it to the user)

import json
#JSON stands for Javascript Object Notation (it is a way of presenting data..like..uh lists etc..you'll see)

import os
#OS allows us to...work with...........the Operating System

import queue
#imported by mistake...maybe useful later(queue is actually used for multiprocessing)

import re
#re==>regex==>RegularExpression..it is used to find particular stuff from large text 
# for example you can find all instances of the word "Google" in google's wikipedia article using this

import threading
#Multiprocesses (threads..2 tasks at once..kindof)

import time
#Time....

from urllib.parse import quote, unquote
#urllib.parse-->works with urls it converts them..you'll see later

from bs4 import BeautifulSoup as bs
#Python library that allows us to work on HTML (you can find elements with an id etc etc etc) 
# useful as we are working on....html pages to get data lol

from selenium import webdriver
#Selenium is a library that allows us to automate a WEBBROWSER
#  even headless(headless means that the UI is not visible(less ppower intensive..and we will use this so that we can automate clicks on a webpage(i'll explain)))

