"""
To-Do

Proper comments
Error Handling and Message displaying
cd works for relative paths only, implement it differently for absolute paths


More known issues - 

1. if we use contains in query to Drive, then substring..multiple files found ex-
 files--
 abc
 abcd

 if we search abc, we get multiple files found

2. can't download google doc files
3. upload/download folders

"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Driver:
    """
    Class for DriveGit
    

    Data members 
    drive : pydrive.auth.GoogleDrive variable 
    current_dir : id for current directory

    Member Functions
    """

    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  #client_secrets.json need to be in the main directory
        self.drive = GoogleDrive(gauth)
        self.current_dir = 'root'
        self.name_structure = []
        self.id_structure = []
       
    def pwd(self):
        print('/'.join(self.name_structure)) 

    def ls(self):
        fileList = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.current_dir}).GetList()
        folders = []
        print("Files-------")
        for files in fileList:
            if(files['mimeType'] != 'application/vnd.google-apps.folder'):
                print(files['title'])
            else:
                folders.append((files['title'],files['id']))

        print("Folders-----")
        for one_folder in folders:
            print(one_folder[0])

    def cd(self,dest):

        if dest=='..':
            if self.current_dir != 'root':
                self.current_dir = self.id_structure.pop()
                del self.name_structure[-1]
                print("Changing to",'/'.join(self.name_structure))
            return

        #Getting id of the folder
        folders = self.drive.ListFile({'q': "title contains '%s' and trashed=false and mimeType = 'application/vnd.google-apps.folder'" % dest}).GetList()
        if len(folders)==0:
            print("No such folder found!")
        elif len(folders)==1:
            
            self.name_structure.append(dest)
            self.id_structure.append(folders[0]['id'])
            self.current_dir = folders[0]['id']
            print("Changing to",'/'.join(self.name_structure))

        else:
            print("Multiple folders found! Use cd command again")
            for i in folders:
                print(i['title'])

    def mkdir(self,folder_name):
        folder = self.drive.CreateFile({'title': folder_name,
                                        "parents":  [{"id": self.current_dir}],
                                        "mimeType": "application/vnd.google-apps.folder"})

        folder.Upload()
        print("Successfully created folder",folder_name,"!")

    def upload_file(self,file_path):
        the_file = self.drive.CreateFile({"parents":  [{"id": self.current_dir}]})
        the_file.SetContentFile(file_path)
        the_file.Upload()

    def download_file(self,file_name):
        
        the_file = self.drive.ListFile({'q': "title contains '%s' and trashed=false and mimeType != 'application/vnd.google-apps.folder'" % file_name}).GetList()
        if len(the_file) == 0:
            print("No file with prefix filename %s found!"%file_name)
        elif len(the_file) == 1:
            print("Downloading the file",the_file[0]['title'])
            the_file[0].GetContentFile(the_file[0]['title'])
        else:
            print("Multiple files found!")
            for files in the_file:
                print(files['title'])
