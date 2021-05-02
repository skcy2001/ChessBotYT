from distutils.core import setup # Need this to handle modules
import py2exe 
import tkinter as tk
from tkinter import *
from tkinter import font, PhotoImage, ttk 
from threading import *
from collections import defaultdict
import urllib, PIL.Image, PIL.ImageTk, sys, re, pytchat

setup(windows=['app.py']) # Calls setup function to indicate that we're dealing with a single console application