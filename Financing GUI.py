import Tkinter as tk
from Tkinter import *
import os
import pickle
import pandas as pd
from datetime import datetime, timedelta
from Financing_Functions import *
from categories import categories_dict

df=0
def import_csv():
    df=get_data(*file_path)
    return
