#!/bin/bash

# pip install -r requirements.txt 

FLASK_APP=main.py FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=5000
