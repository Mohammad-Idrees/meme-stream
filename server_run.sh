sudo -u postgres createdb db
sudo -u postgres createuser user
sudo -u postgres psql --command '\password'
uvicorn main:app --reload --port 8081