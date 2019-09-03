from os import listdir
from os.path import isfile, join
from google.cloud import storage
#from .forms import replace_space

def replace_space(somewords):
    return str(somewords).replace(" ","-",-1)

def new_bucket(bucket_name):
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except:
        bucket = storage.Bucket('APItutorial', bucket_name)
        bucket.location = "asia-east1"
        bucket.storage_class = "STANDARD"
        
        bucket = storage_client.create_bucket(bucket)
        print('Bucket {} created.' .format(bucket_name))

def upload_blob(bucket_name, foldername, localFolder):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    existfile = list_blob(bucket_name, foldername)
    foldername = replace_space(foldername)
    files = [f for f in listdir(localFolder) if isfile(join(localFolder, f))]
    upload_files = set(files)-set(existfile)
    for file in upload_files:
        localFile = localFolder + file
        blob1 = bucket.blob(foldername + '/' + file)
        blob1.upload_from_filename(localFile)

def list_blob(bucket_name, foldername):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    files = bucket.list_blobs(prefix=foldername)
    filelist = [file.name for file in files if '.' in file.name]
    return filelist


def delete_blob(bucket_name, foldername, delete_list):
    client = storage.Client()
    bucket = client.get_bucket('hannibal-album-' + bucket_name)
    foldername = replace_space(foldername)
    filelist = [foldername + '/' + file for file in delete_list]
    bucket.delete_blobs(filelist)


def folder_move(bucket_name, filelist, old_foldername):
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        new_foldername = 'Uploaded'
        
        list_blob(bucket_name, old_foldername)
        
