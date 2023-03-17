from googleAPILib import Service

def getViewLink(fileID):
    service = Service()
    fileMetaData = service.files().get(fileId=fileID, fields='webViewLink').execute()    
    return fileMetaData['webViewLink']