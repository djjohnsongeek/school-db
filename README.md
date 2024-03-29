# School DB Project

## Relevant Links
[Mock Website](https://djjohnsongeek.github.io/school-db-mockup/)<br/>
[Mock Website Repo](https://github.com/djjohnsongeek/school-db-mockup)<br/>

### Library Docs
[Flask Docs](https://flask.palletsprojects.com/en/3.0.x/)<br/>
[Flask WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)<br/>
[WTForms Docs](https://wtforms.readthedocs.io/en/3.1.x/)<br/>
[Peewee Docs](http://docs.peewee-orm.com/en/latest/)<br/>


## First Time Project Setup
- Fork the repo
- Clone your repo to your device
- Create a python virtual environment inside the project directory
```bash
py -3 -m venv .venv
```
- Activate the venv
```bash
.venv/scripts/activate
```
- Install dependencies from requirements.txt
```bash
pip install -r /path/to/requirements.txt
```
- Install [MySQL](https://dev.mysql.com/downloads/installer/)
- Install [MySQL work bench](https://dev.mysql.com/downloads/workbench/)
- Using MySQL Workbench create a new schema (a database)
- Create and folder named "instance" in the project directory
- Move config.example.py to the instance folder, and rename it to "config.py"
- Edit the DB config values so the project can connect to the database
- Run the flask click command to initialize the database
```bash
flask init-db
```

## Running the project
(From the project directory)
- Activate the venv
```bash
.venv/scripts/activate
```
- Run the project
```bash
flask run --debug
```


## Contributing Instructions
- Fork the repo
- Create a new branch for the feature you are working on
- Use this [Trello Board](https://trello.com/b/0HApmQFn/school-db) as a todo list
- Please move the card you are working on from the "To Do" list to the "In Progresss" list, and add your name to the card.
- When ready, submit a pull request to the original repo
- Once merged, we can then move the trello card to completed