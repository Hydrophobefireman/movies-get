import base64
import gc
import json
import os
import queue
import re
import threading
import time
from urllib.parse import quote, unquote

from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template, request, session, url_for
from selenium import webdriver

##END OF IMPORTS##
##MAIN code##

app = Flask(__name__)
# Every module in python has a special attribute
# called __name__ . The value of __name__  attribute is set to '__main__'  when module run as main program.
#  Otherwise the value of __name__  is set to contain the name of the module. se we are just using a small variable instead of the module name.


@app.route("/")
# This basically means our homepage(route defines path)
def index():
    # name of function
    return "hi"  # Python language uses indentations more examples below


if __name__ == "__main__":
    app.run()
    # This basically means iff the user is directly running this script..the app will run


def functions_():
    a = 5
    # I told you about duck typing right? no need to define variable types ===>a=5 means a is int;a='5' means a is string etc
    print(a)
    return a
    # basic ..check the indentatons though in the next function


def some_function(a, b):  # a b are variables..when we call this function to execute code(the coe isnt executed right now..we will supply variable values)
    if a > b:  # notice these colons in places
        while b <= a:
            print(b)
            b += 1
            # basically if a is bigger than b..print(b) and increase its value untill it geats equal to a
    elif b > a:
        while a <= b:
            print(a)
            a += 1
    else:
        print("equal values of a and b")
    # Check the indents^^^^^^^
# None of these functions will do anything unless we call it for example if you want functions_ to work(line 34)
# you would need to type this without the # obvs
# functions_()
# if you needed the function on line 40 you would do this
# some_function(10,100)#a's value replaced by 10....
# if you dont do that the compiler will give an error
#
