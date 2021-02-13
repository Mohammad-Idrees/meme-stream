sudo -u postgres createuser xmemeadmin
sudo -u postgres createdb xmeme
sudo -u postgres psql -c "alter user xmemeadmin with encrypted password 'pass';"
sudo -u postgres psql -c "grant all privileges on database xmeme to xmemeadmin;"