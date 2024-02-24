from app.db import get_db, db_models
import click

def init_db():
    db = get_db()
    db.connect()

    # Prepare db schema
    db.drop_tables(db_models)
    db.create_tables(db_models)

    # todo: add test data

    db.close()

def init_app_commands(app):
    app.cli.add_command(init_db_command)

@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database Initialized ...")