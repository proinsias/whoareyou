# -*- coding: utf-8 -*-
import base64
import typing

import probablepeople as pp
import typer

from Contact import Contact


def get_names(
    fn_field: str,
) -> Contact:
    """
    Extract firstname/surname from vCard 'fn' field.

    :param fn_field: a string containg vCard `fn` data .

    :return: a Contact containing the first name and surname.

    Example:

        # FIXME: Update doctest.
        >>> get_names('John Smith')
        Extracting data for John Smith
        Contact(first_name='John', surname='Smith', photo_data=None)
    """
    # FIXME: Add unit tests.

    first_name = None
    surname = None

    # Use probablepeople to tag the parts of the name.

    full_name_dict = pp.tag(fn_field)[0]

    if 'GivenName' in full_name_dict:
        # If probablepeople has successfully extracted the first name,
        # use it.
        first_name = full_name_dict['GivenName']

    if 'Surname' in full_name_dict:
        # If probablepeople has successfully extracted the surname,
        # use it.
        surname = full_name_dict['Surname']

    # FIXME: String constants.

    try:
        fn_field_split = fn_field.split(' ')
    except (TypeError, AttributeError):
        fn_field_split = ['']

    if first_name is None:
        # If we can't get first name from probablepeople,
        # assume it's the first part of the string.
        first_name = fn_field_split[0]
        if first_name == surname:
            first_name = ''

    if surname is None:
        # If we can't get surname from probablepeople,
        # assume it's the second part of the string, if that exists.
        surname = fn_field_split[1] if len(fn_field_split) > 1 else ''

    return Contact(first_name, surname, photo_data=None)


def get_photo_data(
    photo_field,
) -> str:
    """
    Extract the photo data (if it exists) from a vCard 'photo' field.

    :param photo_field: the input vCard 'photo' field.  # FIXME: Docstring format?

    :return: a base64-encoded string containing the photo data.
    """
    # FIXME: Add unit tests.

    if photo_field is not None:
        photo_data = base64.b64encode(photo_field)
        photo_data = 'data:image/jpeg;base64,' + photo_data.decode('utf8')  # FIXME: String constants.
    else:
        photo_data = ''

    return photo_data


def get_contact(
    v_component,  # FIXME: Type.
) -> typing.Optional[Contact]:
    """
    Docstring

    :param v_component:  # FIXME:

    :return:

    """

    # FIXME: String constants.
    photo_field = v_component.getChildValue('photo')
    photo_data = get_photo_data(photo_field) if photo_field is not None else None

    fn_field = v_component.getChildValue('fn')

    if not fn_field:
        typer.echo(f'No name detected - skipping...')  # FIXME: DEBUG.
        return None

    contact = get_names(fn_field)

    if photo_data is None:
        typer.echo(f'No photo data detected for {contact.first_name} {contact.surname} - skipping...')  # FIXME: DEBUG.
        return None

    contact.photo_data = photo_data

    return contact


def loadContactsFromVCard(
    vcard: str,
) -> None:

    contacts = [
        vcard_utils.get_contact(v_component)
        for v_component in vobject.readComponents(vcard)
    ]

    contacts = [
        (contact.first_name, contact.surname, contact.photo_data)
        for contact in contacts
        if contact is not None
    ]

    # Fill the table.
    with con:
        con.executemany('INSERT OR IGNORE INTO contacts(first_name, surname, photo_data) VALUES (?, ?, ?)', contacts)

        # Print the table contents.
        for row in con.execute('SELECT first_name, surname FROM contacts'):
            print(row)

        print(con.execute('SELECT count(*) FROM contacts').fetchall())
