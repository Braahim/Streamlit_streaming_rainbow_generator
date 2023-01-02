import configparser
import streamlit as st
import os,uuid
from io import StringIO
import pandas 

def account_info(blob_service_client):
    # configuration management

# [END auth_from_connection_string]

    return blob_service_client.get_account_information()

def upload_to_blob(blob_client,df,file_format):
    # Create a local directory to hold blob data
    csv_buffer = StringIO()
    local_path = "./tmp"
    #os.mkdir(local_path)
    if file_format == 'csv':
        df =  df.to_csv(csv_buffer, header = 0, index = False)
        csv_buffer = csv_buffer.getvalue()
    else:
        csv_buffer =  df.to_json(orient='records')
    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + ".{}".format(file_format)
    upload_file_path = os.path.join(local_path, local_file_name)
        


    # Write text to the file
    file = open(file=upload_file_path, mode='w')
    file.write(csv_buffer)
    file.close()
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

