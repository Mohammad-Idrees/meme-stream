sudo service postgresql restart
sudo -u postgres createuser xmemeadmin
sudo -u postgres createdb xmeme
sudo -u postgres psql -c "alter user xmemeadmin with encrypted password 'pass';"
sudo -u postgres psql -c "grant all privileges on database xmeme to xmemeadmin;"
uvicorn main:app --reload --port 8081 