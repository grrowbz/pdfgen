#!/bin/sh

clear
gunicorn -b 0.0.0.0:8000 --reload things:app 
