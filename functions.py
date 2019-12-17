from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def authorise():
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth() 	#client_secrets.json need to be in the main directory
	drive = GoogleDrive(gauth)
	return drive

def list_all_files_in_drive(drive):
	fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	for file in fileList:
  		print('Title: %s, ID: %s' % (file['title'], file['id']))
	return fileList