from googleAPILib import Service

from textToSpeech import TextToSpeech
from uploadFileToDrive import upload_basic
from googleAPILib import Service

def shareFile(fileID):
    
    service  = Service()

    batch = service.new_batch_http_request()
    user_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    batch.add(service.permissions().create(
            fileId=fileID,
            body=user_permission,
            fields='id',
    ))
    batch.execute()
    print(f'File audio.mp3 has been uploaded to Google Drive and shared publicly.')