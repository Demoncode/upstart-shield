# upstart-shield

This is a quick script designed to run a command in a new process group, while
keeping a connection to the parent, spawned (pun intended) out of necessity
due to Upstart's behaviour of killing an entire process group, which plays
havoc with Celery's monitoring of its worker processes and prevents clean
shutdown of Celery masters.

If you run a command using upstart-shield and then send a TERM signal to the
upstart-shield process, it will send a TERM to the process of the command it
spawned (but not the process group). This allows things like celery to do their
relevant clean exits.

Similarly if the command's main process terminates then upstart-shield will
also terminate, allowing upstart to restart it (and therefore the app)


# Installation:

## Standard
`pip install git+git@github.com:Demoncode/upstart-shield.git#egg=upstart-shield`


## Developing upstart-shield

* `git clone git@github.com:Demoncode/upstart-shield.git`
* `workon my-dev-virtualenv`
* `cd upstart-shield`
* `python setup.py develop`


# Usage:

`upstart-shield cmd arg1 arg2 ...`

If you are using upstart, then don't use the `expect fork` or `expect daemon` options.
