#!/bin/bash
set -e
web: gunicorn lightrig_API.wsgi