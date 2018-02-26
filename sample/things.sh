#!/bin/sh

export LANG=ja_JP.UTF-8

clear
gunicorn -b 0.0.0.0:8000 --reload things:app 
