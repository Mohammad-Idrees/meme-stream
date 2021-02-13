sudo -u postgres createdb data
sudo -u postgres createuser us
sudo -u postgres psql --command '\password'
hypercorn main:app --reload --port 8081