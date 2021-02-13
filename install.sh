sudo apt update
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
sudo update-alternatives --config python3
python3 -m pip install --user --upgrade pip
pip3 install -r requirements.txt
sudo apt-get install -y postgresql postgresql-contrib