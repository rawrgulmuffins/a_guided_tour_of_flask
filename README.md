#Heart Beat?

This is a basic flask application with two views. `/version` and `/ping`.

`/version` accepts get requests and returns the current version of code on the
server.

`/ping` accepts posts requests and is used to track how often the self
service health checker is run. `/ping` requires that a JSON object be passed
that contains each of these keys.

    client_start_time: Type=db.DateTime
    logset_gather_time: Type=db.DateTime
    one_fs_version: Type=db.String
    esrs_enabled: Type=db.Boolean
    tool_version: Type=db.String
    sr_number: Type=db.Integer

#How Do I Install Heart Beat?

in the `heart_beat` directory you'll find `setup.py`. Run

    python3 setup.py build && install

This will add a heart_beat module to the instance of python you used to run
`setup.py`. If you don't want to install `heart_beat` to your system Python 
instance (which you probably don't want to do) then it is suggested that you

install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)

On a Linux distribution this means

    $ sudo pip install virtualenvwrapper
    # For Debian
    $ source /usr/local/bin/virtualenvwrapper.sh
    # For Red Hat
    $ source /usr/bin/virtualenvwrapper.sh 
    # On Red Hat you'll have to install Python3 via yum
    $ mkvirtualenv --python=/usr/local/bin/python3 heart_beat
    $ workon heart_beat
    $ cd /path/to/heart_beat/repository
    $ python setup.py build && install

It's also suggested that you add the source line (which is appropriate for you
distribution) to your bashrc

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh

If you want to run this program on windows check out 
[virtualenvwrapper-win](https://github.com/davidmarble/virtualenvwrapper-win)

#How Do I Run The Unit Tests?

Any directory in the Heart Beat git repository should be able to run the unit
tests. Just run

    nosetests

to run each test. All tests should pass at all times (in master). If any test
fails which is checked into master then the build is broken.

In order to see the test coverage on the project run

    nosetests --with-coverage --cover-erase --cover-branches --cover-html --cover-package=heart_beat

#Dependencies
Python=3
A OS which can run Python3
DateTime==4
Flask==0.10
Flask-SQLAlchemy==2
Jinja2==2.7
MarkupSafe==0.23
SQLAlchemy==1
Werkzeug==0.10
itsdangerous==0.24
nose==1.3
pytz==2015
zope.interface==4.1

#Change Log

##0.1
*Initial release.
*Includes the `/version` and `/ping` views and all components required to use
both views.
