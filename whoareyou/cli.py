# -*- coding: utf-8 -*-
import pathlib
import sqlite3

import typer
import vobject

import vcard_utils

app = typer.Typer()
con = sqlite3.connect('contacts.sqlite')
with con:
    # Create table
    con.execute('''
        CREATE TABLE IF NOT EXISTS contacts
        (
            first_name text,
            surname text,
            photo_data text,
            UNIQUE(first_name, surname)
        )
    ''')


@app.command('import')
def import_vcard(
    file: pathlib.Path,  # help = 'the input file'  # FIXME: Add details, include 'file' help name.
) -> None:
    """
    Extract the contact info from a vCard file.
    """

    with open(file, 'r') as f:
        vcard = f.read()
        vcard_utils.loadContactsFromVCard(vcard)

    # FIXME: Add a help text for a CLI argument
    # FIXME: metavar


@app.callback()
def callback(
):
    pass


if __name__ == '__main__':
    app()
