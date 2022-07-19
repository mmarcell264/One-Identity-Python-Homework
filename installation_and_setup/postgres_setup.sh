#!/bin/bash

flag_number=0
#Source:https://www.baeldung.com/linux/use-command-line-arguments-in-bash-script
while getopts u:p:d: flag
do
    case "${flag}" in
        u) username=${OPTARG}
           flag_number=$((flag_number + 1));;
        p) password=${OPTARG}
           flag_number=$((flag_number + 1));;
	d) database=${OPTARG}
	   flag_number=$((flag_number + 1));;
    esac
done

if [[ $flag_number -eq 3 ]]
then
	#Source:https://stackfame.com/creating-user-database-and-adding-access-on-postgresql
	#Switch to postgres user
	#Create db
	#Create user
	#Grant privileges to database
	#Add creatdb privilige to user
	#Message user about the process
	#Exit postgres user
	sudo -i -u postgres <<EOF
	psql -c "CREATE DATABASE $database;"
	psql -c "CREATE USER $username WITH ENCRYPTED PASSWORD '$password';"
	psql -c "grant all privileges on database $database to $username;"
	psql -c "ALTER USER $username CREATEDB;"
	echo "Postgres User '$username' and database '$database' created."
	exit
EOF
	#Create .env file
	cd ..
	cd backend/key_value_server/key_value_server
	sudo touch .env
	#Add enviroment variables to .env file
	echo "DB_NAME=$database" >> .env
	echo "DB_USER_NAME=$username" >> .env
	echo "DB_USER_PW=$password" >> .env
	echo "DB_HOST=localhost" >> .env
	echo "DB_PORT=5432" >> .env
else
	echo "Please use this way the script: sudo bash postgres_setup.sh -u <db_username> -p <db_password> -d <db_name>"
fi

