# G2T03ESD 

# Project setup
Ensure that WAMP or MAMP is running

Import sql codes into phpmyadmin to set up the databases 
# Warning: If your MYSQL server version is below 8, ensure that in the user database, the token field can accept varchar(1000)

In compose.yaml, replace <nichgoh> in the images with your own dockerid and replace the authentication environment DBPASS if required

Drag the entire ESD_Proj file into your www folder for WAMP users or htdocs folder for MAMP users

In your console, go to the directory with the compose.yaml file
and run
docker compose build
docker compose up -d

Click this http://localhost:4000/users/syncUserswithOutsystem to sync your user database with the one in outsystems

The starting page should be http://localhost/ESD_Proj/login for WAMP and http://localhost:8888/ESD_Proj/login.html for MAMP

Example user account:
User1 account
username: user1
password: password

Example restaurant account:
WineConnection account
username: WineConnection
password: password

