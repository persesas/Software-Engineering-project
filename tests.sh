#!/bin/bash
python3 -m unittest test/mediator_test.py
python3 -m unittest test/auth_test.py 
python3 -m unittest test/controller_test.py 
python3 -m unittest test/db_test.py 