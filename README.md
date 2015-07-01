flask_brownbag
==============

This is a Isilon brown bag that is dedicated to teaching what flask is, how to use it, and what are some useful plugins.

Running The Notebook
===================
* Install Python3
* git clone git@github.west.isilon.com:alord/flask_brownbag.git
* cd flask_brownbag
# You might have to sudo the next command if you're using the system python.
* pip install -e . # This will take 3-4 minutes.
* ipython notebook # This will open a web browser with the notebook directory available to you.

If you don't want to have to use sudo

* Install Python3 #apt-get, yum, brew, or direct download.
* git clone git@github.west.isilon.com:alord/flask_brownbag.git
* cd flask_brownbag
* sudo pip install virtualenvwrapper
On Debian systems
* source /usr/local/bin/virtualenvwrapper.sh
OR
* source /usr/bin/virtualenvwrapper.sh
* mkvirtualenv --python=/usr/bin/python3 flask_brownbag
* workon flask_brownbag
* pip install -e . # This will take 3-4 minutes.
* ipython notebook # This will open a web browser with the notebook directory available to you.
