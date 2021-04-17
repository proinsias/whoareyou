# -*- coding: utf-8 -*-

import pathlib
import random
import typing

import typer

import dbcontacts
import images

app = typer.Typer()
NUM_CONTACTS_TO_TEST = 4


@app.command('import')
def import_vcard(
    file: pathlib.Path,  # help = 'the input file'  # FIXME: Add details, include 'file' help name.
) -> None:
    """
    Extract the contact info from a vCard file.
    """

    with open(file, 'r') as f:
        vcard = f.read()
        contacts = dbcontacts.loadContactsFromVCard(vcard)
        dbcontacts.loadContactsIntoDb(contacts)

    # FIXME: Add a help text for a CLI argument
    # FIXME: metavar


@app.command()
def names():
    """
    Docstring. FIXME:
    """

    contacts = dbcontacts.getNContactsFromDb(NUM_CONTACTS_TO_TEST)

    choice = random.randint(0, NUM_CONTACTS_TO_TEST-1)

    ansi_colors = images.getAnsiColorsFromPhotoData(contacts[choice].photo_data)
    printAnsiColors(ansi_colors)

    for contact in contacts:
        typer.echo(f'{contact.first_name} {contact.surname}')

    typer.echo(f'{contacts[choice].first_name} {contacts[choice].surname}')


@app.command()
def faces():
    """
    Docstring. FIXME:
    """
    contacts = dbcontacts.getNContactsFromDb(NUM_CONTACTS_TO_TEST)

    choice = random.randint(0, NUM_CONTACTS_TO_TEST-1)

    typer.echo(f'{contacts[choice].first_name} {contacts[choice].surname}')

    for contact in contacts:
        ansi_colors = images.getAnsiColorsFromPhotoData(contact.photo_data)
        printAnsiColors(ansi_colors)

    ansi_colors = images.getAnsiColorsFromPhotoData(contacts[choice].photo_data)
    printAnsiColors(ansi_colors)


@app.callback()
def callback(
):
    pass


def printAnsiColors(
    ansi_colors: typing.List[typing.List[str]],
) -> None:
    for ansi_color_row in ansi_colors:
        for ansi_color in ansi_color_row:
            typer.echo(ansi_color, nl=False)
        typer.echo()


if __name__ == '__main__':
    app()
