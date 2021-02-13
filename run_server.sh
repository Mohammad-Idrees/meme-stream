sudo -u postgres psql
create database xmeme
create user postgres with password '1234'
uvicorn main:app --reload --port 8081