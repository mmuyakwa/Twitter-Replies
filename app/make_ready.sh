#!/bin/bash

pipenv check
pipenv update
pipenv lock -r > requirements.txt
