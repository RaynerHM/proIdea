#!/bin/bash

#Activate Virtualenv
source $HOME/.virtualenv/projectideas/bin/activate

#Load environment variables
source $HOME/projectideas/variables

#Synchronize LDAP users
python $HOME/projectideas/manage.py ldap_sync_users

#Change user password
python $HOME/projectideas/manage.py runscript change_password
