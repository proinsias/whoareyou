# -*- coding: utf-8 -*-

import pathlib
import random
import typing

import typer

import __init__
import dbcontacts
import images


app = typer.Typer()
NUM_CONTACTS_TO_TEST = 4


def printAnsiColors(
    ansi_colors: typing.List[typing.List[str]],
) -> None:
    for ansi_color_row in ansi_colors:
        for ansi_color in ansi_color_row:
            typer.echo(ansi_color, nl=False)
        typer.echo()


def version_callback(
        value: bool,
) -> None:

    if value:
        typer.echo(f'{config.name} version: {__init__.__version__}')
        raise typer.Exit()


@app.command('import')
def import_vcard(
    file: pathlib.Path = typer.Argument(
        ...,
        help='The vCard file to ingest',
        metavar='file',
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    """
    Save the contact info from a vCard file to the database.

    Duplicates are ignored.
    Command exits with code 1 if the file is not found.
    """

    with file.open() as f:
        vcard = f.read()
        contacts = dbcontacts.loadContactsFromVCard(vcard)
        dbcontacts.loadContactsIntoDb(contacts)


@app.command()
def names():
    """
    Identify which name goes with a random face.
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
    Identify which face goes with a random name.
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
    version: typing.Optional[bool] = typer.Option(
        None,
        '--version',
        '-v',
        callback=version_callback,
        is_eager=True,
    ),
):
    """Practice remembering important names and faces."""
    pass


if __name__ == '__main__':
    app()
