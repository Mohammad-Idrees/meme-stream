sudo apt update -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.8 -y
sudo apt install virtualenv -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install -y python3-pip
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt