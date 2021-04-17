# -*- coding: utf-8 -*-

import typing

import typer
import vobject
from sqlalchemy import select, func, Column, Integer, Text, UniqueConstraint

import db


class Contact(db.Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    surname = Column(Text)
    photo_data = Column(Text)
    __table_args__ = (
        UniqueConstraint('first_name', 'surname', name='_first_name_surname_uc'),
    )

    def __init__(self, first_name, surname, photo_data):
        self.first_name = first_name
        self.surname = surname
        self.photo_data = photo_data

    def __repr__(self):
        return f'Contact(first_name={self.first_name}, surname={self.surname})'


db.Base.metadata.create_all()


def get_contact_from_v_component(
    v_component,  # FIXME: Type.
) -> typing.Optional[Contact]:
    """
    Docstring

    :param v_component:  # FIXME:

    :return:

    """

    # FIXME: String constants.
    photo_data = v_component.getChildValue('photo')
    fn_field = v_component.getChildValue('fn')

    if not fn_field:
        typer.echo(f'No name detected - skipping...')  # FIXME: DEBUG so I don't have to import typer?
        return None

    first_name, surname = get_names_from_fn_field(fn_field)

    if photo_data is None:
        typer.echo(f'No photo data detected for {first_name} {surname} - skipping...')  # FIXME: DEBUG.
        return None

    return Contact(first_name, surname, photo_data)


def get_names_from_fn_field(
    fn_field: str,
) -> typing.Tuple[str, str]:
    """
    Extract firstname/surname from vCard 'fn' field.

    :param fn_field: a string containg vCard `fn` data .

    :return: strings for the first name and surname.

    Example:

        >>> get_names_from_fn_field('John Smith')
        ('John', 'Smith')
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

    return first_name, surname


def loadContactsFromVCard(
    vcard: str,
) -> typing.List[Contact]:

    contacts = [
        get_contact_from_v_component(v_component)
        for v_component in vobject.readComponents(vcard)
    ]

    return [
        contact
        for contact in contacts
        if contact is not None
    ]


def loadContactsIntoDb(
    contacts: typing.List[Contact],
) -> None:
    """Docstring.  FIXME"""

    s = db.Session()
    s.add_all(contacts)
    s.commit()


def getNContactsFromDb(
    n: int,
) -> typing.List[Contact]:

    s = db.Session()

    return s.query(Contact).order_by(func.random()).limit(n).all()
