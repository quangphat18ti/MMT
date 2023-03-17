from __future__ import print_function
from googleAPILib import Service


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_basic(nameFile):
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    folderId = ["1IQWclUawk8A-Lgj1dmTGMUUsto2eTeBx"]

    try:
        # create drive api client
        service = Service()

        file_metadata = {
            'name': nameFile,
            # "parents": folderId
        }
        media = MediaFileUpload(nameFile,
                                mimetype='audio/mpeg')
        # pylint: disable=maybe-no-member
        file = service.files().create(
                                        body=file_metadata, 
                                        media_body=media,
                                        fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


if __name__ == '__main__':
    upload_basic("audio.mp3")