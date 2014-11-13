This is a quick script designed to run a command in a new process group, while
keeping a connection to the parent, spawned (pun intended) out of necessity
due to Upstart's behaviour of killing an entire process group, which plays
havoc with Celery's monitoring of its worker processes and prevents clean
shutdown of Celery masters.

Installation:

Use pip or with your virtualenv activated do 'python setup.py develop'

Usage:

upstart-shield cmd arg1 arg2 ...

upstart-shield-test
