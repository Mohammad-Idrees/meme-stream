sudo apt update -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.8 -y
sudo apt install virtualenv -y
sudo apt install postgres postgresql-contrib -y
sudo -u postgres createuser xmemeadmin
sudo -u postgres createdb xmeme
sudo -u postgres psql -c "alter user xmemeadmin with encrypted password 'pass';"
sudo -u postgres psql -c "grant all privileges on database xmeme to xmemeadmin;"
sudo apt install -y python3-pip
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt