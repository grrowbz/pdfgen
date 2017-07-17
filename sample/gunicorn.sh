#!/bin/sh
clear
gunicorn -b 0.0.0.0:8888 things:app
