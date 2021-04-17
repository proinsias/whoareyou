# -*- coding: utf-8 -*-

import pathlib
import random
import typing

import typer

import dbcontacts
import images

app = typer.Typer()
NUM_CONTACTS_TO_TEST = 4


# FIXME: GT todo.txt.


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

    for i, contact in enumerate(contacts):
        typer.echo(f'{i+1}: {contact.first_name} {contact.surname}')

    guess = typer.prompt('Enter the number for the name that goes with this face')

    if int(guess) == choice + 1:
        typer.echo(f'Correct! It is {contacts[choice].first_name} {contacts[choice].surname}!!!')
    else:
        typer.echo(f'Afraid not! It is {contacts[choice].first_name} {contacts[choice].surname}. Try again!')


@app.command()
def faces():
    """
    Docstring. FIXME:
    """
    contacts = dbcontacts.getNContactsFromDb(NUM_CONTACTS_TO_TEST)

    choice = random.randint(0, NUM_CONTACTS_TO_TEST-1)

    typer.echo(
        'Which face goes with this name: '
        f'{contacts[choice].first_name} {contacts[choice].surname}?',
    )

    typer.echo('Is it...')

    guess = -1

    for i, contact in enumerate(contacts):
        ansi_colors = images.getAnsiColorsFromPhotoData(contact.photo_data)
        printAnsiColors(ansi_colors)
        response = typer.prompt(f'This face? (y/n)')
        if response == 'y':
            guess = i + 1
            break

    if int(guess) == choice + 1:
        typer.echo(f'Correct! This is {contacts[choice].first_name} {contacts[choice].surname}!!!')
    else:
        typer.echo(f'Afraid not! This is {contacts[choice].first_name} {contacts[choice].surname}. Try again!')

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
