# Catalog-Item-Server-version
# Project: Linux Server Configuration
This is the steps of setting up the web application server and other important informations.

I rent an an Amazon Lightsail instance and host the catalog item project on it.


## Information of the AWS server
The public IP address is 18.217.228.219, and the SSH port used is `2200` as required.

You can visit the website by http://18.217.228.219


## Set up AWS instance
### Create an instance with Amazon Lightsail
1. Follow the instruction in the prject details page. I create an Unix instance on Amazon Lightsail. It has public IP address: 18.217.228.219


### Connect to the instance on a local machine
1. Download the default private key in account setting page.
2. Put the private key in the directory of `~/.ssh` by using mv command
3. Copy the content of downloaded .pem file into the created .rsa file in `~/.ssh`
4. Run `chmod 600 ~/.ssh/'the rsa file created'`
5. Then I can log in with authentication by typing `ssh -i ~/.ssh/'the rsa file created' ubuntu@your.public.address`


### Upgrade and update packages
1. Run `sudo apt-get update` to let the server know the which packages that are available for updating
1. Run `sudo apt-get upgrade` to update available packages


### Set up firewall
1. Use text editor to open the /etc/ssh/sshd_config file, and change the SSH port number from `22` to `2200`
2. Run `sudo service ssh restart` to restart ssh
3. Run `sudo ufw default deny incoming` to deny every incoming
4. Run `sudo ufw default allow outgoing` to allowing every outgoing
5. Run `sudo ufw allow ssh` to allow SSH
6. Run `sudo ufw allow 2200/tcp` to allow tcp for port 2200.
7. Run `sudo ufw allow www` to allow http
8. Run `sudo ufw allow 123/udp to allow NTP
9. Run `sudo ufw deny 22` to deny port `22` to shut down `port 22` for safety reason
10. Run `sudo ufw enable` to enable the firewall
11. Go to AWS account page to change the firewall settings by creating port 80(TCP), port 2200(TCP) and port 123(UDP). Then disable the port 22


### Create the new user `grader` and give it `sudo` permission
1. Run `sudo adduser grader` to add the new user named `grader`
2. Follow the prompt instruction of setting up password and information of this new user
3. Run `sudo visudo`
4. Add  `grader ALL=(ALL:ALL) ALL` below the line `root ALL=(ALL:ALL) ALL`
5. Save and quit the text editor


### Create a pair of keys for `grader`
1. Run `ssh-keygen` on my personal computer
2. Type in the name of key files
3. Follow the instruction to set passphrase
4. It will generate two files: one private key and one public key
5. Run `mkdir .ssh` onn server in `grader`'s home directory to create a directory to store the public key file
6. Run `cat ~/.ssh/'the name you set for grader's key'.pub` to open the public key file
7. Run `touch .ssh/authorized_keys` and copy the public key content you created in to this file
8. Run `chmod 700 .ssh` and then `chmod 644 .ssh/authorized_keys`
9. Then we can run `ssh -i ~/.ssh/'the key you created' -p 2200 grader@the public IP address` to log in the server by key authentication as user `grader`



### Configure the local timezone to UTC
1. Run `sudo dpkg-reconfigure tzdata`. Select `UTC` in `None of above` catagory


### Install Apache
1. Run `sudo apt-get install apache2` to install Apache
2. We can visit the public address by open it in a browser to check if `Apache2` was installed successfully. (If the Apache2 Ubuntu default page is shown, Apache2 was installed successfully.)

### Install PostgreSQL and make sure PostgreSQL is not allowing remote connections
1.Run `sudo apt-get install postgresql` to install PostgreSQL

### Install mod_wsgi
1. Run `sudo apt-get install libapache2-mod-wsgi python-dev` to install `mod_wsgi` package to support Flask app with python-dev
2. Run `sudo a2enmod wsgi` to enable it.


### Create new Postgresql database and user
1. Run `sudo su - postgres` to switch to user `postgres` then run `psql` to connect to postgresql shell
2. Run `CREATE ROLE catalog WITH LOGIN;` to create a new user named 'catalog'
3. Run `ALTER ROLE catalog CREATEDB;` to change the role of catalog to have the permission to create databases
4. Switch back to the user we log in to server before
5. Run `sudo adduser catalog` to create a new user called `catalog`
6. Follow the steps to fill in the information and create password for `catalog`
7. Run `sudo visudo` and add `catalog ALL=(ALL:ALL) ALL` after the line `grader ALL=(ALL:ALL) ALL`
8. Log into the server as `catalog` and run `createdb catalog` to create a database called `catalog`

### Clone the catalog item project from github
1. Run `sudo apt-get install git` to install `git`
2. Switch to `/var/www` dirctory and run `mkdir catalog` to create a directory called `catalog`
3. Run `cd catalog` to switch into that directory
4. Run `https://github.com/lllli/Catalog-Item-Server-version.git` to clone the catalog item project server version. I just made all modifications to the original project to make it available to host it on the server. These modifications include: change the database method from `sqllite` to `postgresql`, change `run(0.0.0.0, port = 5000)` to `run`, change `the json file path` to its full path (This spent me a lot of time to deal with 'no such file or directory' problem), also the main script file's name is changed to `__init__.py`.
5. Run `sudo chown -R ubuntu:ubuntu catalog/` to change the owner of this directory to ubuntu (the user we log in as)

### Install and set up virtual environment.
1. Run `sudo apt-get install python-virtualenv` to install virtual environment
2. Run `sudo apt-get install python-pip` to install pip for installing other python packages
3. Run `/var/www/catalog/catalog` to switch to the project directory
4. Run `virtualenv venv` to create the virtual environment named `venv`
5. Run `. venv/bin/activate` to activate virtual environment `venv`
6. Run `pip install sqlalchemy`, `pip install --upgrade oauth2client`, `pip install flask`,`pip install httplib2`, `pip install requests`, `pip install psycopg2`, `sudo apt-get install libpq-dev` to install all necessary packages
7. Run `deactivate` to exit virtual environment
8. Run `cd /etc/apache2/sites-available/` to switch to this directory
9. Run `sudo nano game.conf` to create a configuration file and put the following lines into it.
10. 	<VirtualHost *:80>
			ServerName your server ip address
			ServerAdmin your admin address
			WSGIScriptAlias / /var/www/catalog/catalog.wsgi
			<Directory /var/www/catalog/catalog/>
				Order allow,deny
				Allow from all
				Options -Indexes
			</Directory>
			Alias /static /var/www/catalog/catalog/static
			<Directory /var/www/catalog/catalog/static/>
				Order allow,deny
				Allow from all
				Options -Indexes
			</Directory>
			ErrorLog ${APACHE_LOG_DIR}/error.log
			LogLevel warn
			CustomLog ${APACHE_LOG_DIR}/access.log combined
	     </VirtualHost>
11. Run `sudo a2ensite catalog` to activate the running
12. Run `sudo service apache2 reload`
13. Run `cd /var/www/catalog` and Run `sudo nano catalog.wsgi` to create a wsgi file and then put the following lines into that file
14. 
	```
	activate_this = '/var/www/catalog/catalog/venv/bin/activate_this.py'
	execfile(activate_this, dict(__file__=activate_this))

	#!/usr/bin/python
	import sys
	import logging
	logging.basicConfig(stream=sys.stderr)
	sys.path.insert(0,"/var/www/catalog/")

	from catalog import app as application
	application.secret_key = your secret key in your inity script
	```
15. Run `sudo service apache2 restart` to restart `Apache2`
16. Run `sudo chown -R www-data:www-data catalog` to change the owner of this app to catalog

### Setup db and import data
1. Run `. venv/bin/activate` to activate the virtual environment
2. Run `python setup_db.py` to setup database
3. Run `python import_data.py` to import initial data
4. Run `deactivate` to exit virtual environment
5. Run `sudo service apache2 restart` to restart Apache2
6. Resart Apache again: `sudo service apache2 restart`

## Now the web app should be available in your ip address

## Reference:
All Udacity videos
Flask offical websites:(http://flask.pocoo.org)
Digital Ocean tutorial: (https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
A lot of Udacity forum and stackoverflow posts
