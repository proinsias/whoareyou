# -*- coding: utf-8 -*-

import urllib

import streamlit as st

import dbcontacts


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
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
        help='Help String',  # FIXME:
    )

    if file is not None:

        vcard = file.read()
        contacts = dbcontacts.loadContactsFromVCard(vcard)
        dbcontacts.loadContactsIntoDb(contacts)

        file.close()


def app():
    # readme_text = st.markdown(get_file_content_as_string('streamlit_instructions.md'))
    readme_text = st.markdown('abc')

    st.sidebar.title('What to do')
    app_mode = st.sidebar.selectbox(
        'Choose the app mode',
        ['Show instructions', 'Import Contacts', 'Test Faces', 'Test Names'],
    )
    if app_mode == 'Show instructions':
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == 'Import Contacts':
        readme_text.empty()
        import_vcard()
    # elif app_mode == "Test Faces":
    #     readme_text.empty()
    #     test_faces()
    # elif app_mode == "Test Names":
    #     readme_text.empty()
    #     test_names()


if __name__ == '__main__':
    app()
