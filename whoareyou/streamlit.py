# -*- coding: utf-8 -*-

import io
import random
import urllib

import streamlit as st

import config
import dbcontacts


NUM_CONTACTS_TO_TEST = 4


@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    """ Download a single file and make its content available as a string. """

    url = 'https://raw.githubusercontent.com/proinsias/whoareyou/main/' + path
    response = urllib.request.urlopen(url)

    return response.read().decode('utf-8')


def import_vcard(
) -> None:
    """
    Save the contact info from a vCard file to the database.

    Duplicates are ignored.
    """

    file = st.file_uploader(
        label='Upload vCard contacts',
        type='vcf',
        accept_multiple_files=False,
        key=None,
        # help='Help String',  # FIXME:
    )

    if file is not None:
        vcard = io.StringIO(file.getvalue().decode('utf-8')).read()
        file.close()

        contacts = dbcontacts.loadContactsFromVCard(vcard)
        dbcontacts.loadContactsIntoDb(contacts)

        num_contacts = dbcontacts.getNumberContactsFromDb()

        st.text(f'Imported contacts into database: now {num_contacts} contacts.')


def test_names():
    """
    Docstring. FIXME:
    """

    contacts = dbcontacts.getNContactsFromDb(NUM_CONTACTS_TO_TEST)

    choice = random.randint(0, NUM_CONTACTS_TO_TEST-1)

    st.image(
        image=contacts[choice].photo_data,
        use_column_width='always',
    )

    text = '''\
    Enter the number for the name that goes with this face:

    '''

    for i, contact in enumerate(contacts):
        text = f'''\
        {text}
        {i+1}: {contact.first_name} {contact.surname}
        '''

    st.markdown(text)

    guess = st.text_input(
        label='Guess',
        value='',
    )

    if len(guess) > 0:
        if int(guess) == choice + 1:
            st.text(f'Correct! It is {contacts[choice].first_name} {contacts[choice].surname}!!!')
        else:
            st.text(f'Afraid not! It is {contacts[choice].first_name} {contacts[choice].surname}. Try again!')


def app():
    # FIXME: Add whoareyou version __init__.__version__.
    readme_text = st.markdown(get_file_content_as_string('streamlit_instructions.md'))

    st.sidebar.title('What to do')
    app_mode = st.sidebar.selectbox(
        'Choose the app mode',
        ['Show instructions', 'Import Contacts', 'Test Faces', 'Test Names'],
    )
    if app_mode == 'Show instructions':
        st.sidebar.success('To continue select option from sidebar.')
    elif app_mode == 'Import Contacts':
        readme_text.empty()
        import_vcard()
    elif app_mode == 'Test Names':
        readme_text.empty()
        test_names()
    # FIXME:
    # elif app_mode == "Test Faces":
    #     readme_text.empty()
    #     test_faces()


if __name__ == '__main__':
    app()
