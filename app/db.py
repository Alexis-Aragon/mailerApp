import mysql.connector

import click

from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

#obtener base de datos y cursor
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

# cerrar conexión de base de datos
def close_db(e=None):
    db = g.pop('db', None) # quitar propiedad db a g

    if db is not None:
        db.close()

# inicializar base de datos
def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

# ejecutar comando en terminal
@click.command('init-db')
@with_appcontext # acceder a las variables de configuracion
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)