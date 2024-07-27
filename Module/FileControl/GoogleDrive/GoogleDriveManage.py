from ..FileManage import OpenCSV
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Drive:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("token.json")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile("token.json")
        elif gauth.access_token_expired:
            gauth.Refresh()
            gauth.SaveCredentialsFile("token.json")
        else:
            gauth.Authorize()
        self.__drive = GoogleDrive(gauth)

    def create_table_file(self, 
                          file_name: str, 
                          file_name_drive: str, 
                          column_title: list | tuple, 
                          columns: list | tuple
                          ) -> str:
        file = OpenCSV(file_name=file_name)
        file.create(column_title=column_title, columns=columns)

        dfile = self.__drive.CreateFile(metadata={'title': file_name_drive})
        dfile.SetContentFile(filename=file_name)
        dfile.Upload()

        dfile.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })

        link = dfile['alternateLink']

        return link
