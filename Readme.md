# Anna - The xil XMPP bot

### Installation

#### Install python3 packages
    pip3 install sleekxmpp configobj

##### Command-specific packages
* localtime - `python-dateutil`
* topic - `jinja2`

#### Set up the database
    sqlite3 db.sq3 < db.sql

#### Config file
Copy `config.example.ini` to `config.ini` and edit it to your liking.

**Note:** By default all the handlers are enabled, so make sure you have all their packages installed. The modules are imported inside functions so you won't see any missing package errors until you try to use the command.

#### Run the bot
	python3 mucbot.py


#### Security notes:
Its possible to access __class__.__base__.__subclasses__.... on the functions passed to the template. Disable topic if you dont trust your users.
