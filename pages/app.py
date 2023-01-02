import streamlit as st

from utils import app_utils

import random
import pandas as pd
from datetime import date, datetime
import time
from io import StringIO
from azure.storage.blob import  BlobServiceClient
import datetime


def page():
    # display title
    st.title('Streaming simulation to Blob')
    # display picture
    

    
    st.image("https://bugshunterblog.blob.core.windows.net/posts/Open-Live-Writer/Migrer-de-WindowsAzure.Storage.-ou.Blobs_AAE9/azure_blob_0aaa3b34-75a1-4f28-81ac-6e748971db29.png", width = 700)    
    st.write("---")

    # sidebar display
    st.sidebar.write("---")
    st.sidebar.success('Account : ' + st.session_state.data_azureaccount)

    # destination container
    # blob container selectbox
    st.session_state.blob_service_client = BlobServiceClient(st.session_state.secret_url, st.session_state.secret_accountKey)

    """
    I. Get all containers from Account storage, 
    II. Choose container
    """
    all_containers = st.session_state.blob_service_client.list_containers()
    containers = ['Choose container'] + list([x['name'] for x in all_containers])
    if 'data_container' not in st.session_state:
        st.session_state.data_container = containers[0]
    st.session_state.data_container = st.selectbox('Destination Container', containers, index = containers.index(st.session_state.data_container))
    if st.session_state.data_container == containers[0]:
        st.error('Please choose a container')
    else:
        #display container info
        container_client = st.session_state.blob_service_client.get_container_client(st.session_state.data_container)
        #st.write(container_client.get_container_properties())
        #st.subheader('Container Info ')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(":key: <span style='color:blue;'>** Name **</span>", unsafe_allow_html = True)
        with col2:
            st.markdown(":computer: <span style='color:purple;'>** Last Modified **</span>", unsafe_allow_html = True)
        col1, col2 = st.columns(2)
        with col1:
            st.code(container_client.get_container_properties()['name'])
        with col2:
            st.code(container_client.get_container_properties()['last_modified'])
        
        #properties = blob_client.get_blob_properties()
        # [END upload_blob_to_container]

        # [START list_blobs_in_container]
        period = '.'
        slash = '/'
        tmp_list = container_client.list_blobs()
        blobs_list = ['Choose blob'] + list([x['name'] for x in tmp_list])
        for item in blobs_list.copy():
            if period in item or slash in item:
                blobs_list.remove(item)
        if 'data_blob' not in st.session_state:
            st.session_state.data_blob = blobs_list[0]
        st.session_state.data_blob = st.selectbox('Blobs', blobs_list, index = blobs_list.index(st.session_state.data_blob))
        if st.session_state.data_blob == blobs_list[0]:
            st.error('Please choose a blob')
        else:
            blob_client = container_client.get_blob_client(blob = st.session_state.data_blob)
            st.text(blob_client.get_blob_properties())
            #display container info
            container_client = st.session_state.blob_service_client.get_container_client(st.session_state.data_container)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(":calendar: <span style='color:blue;'>** Creation Date **</span>", unsafe_allow_html = True)
            with col2:
                st.markdown(":computer: <span style='color:purple;'>** Last Modified **</span>", unsafe_allow_html = True)
            col1, col2 = st.columns(2)
            with col1:
                st.code(blob_client.get_blob_properties()['creation_time'])
            with col2:
                st.code(blob_client.get_blob_properties()['last_modified'])

#####################################################################
            # format selectbox
            formatlist = ['json', 'csv']
            if 'data_format' not in st.session_state:
                st.session_state.data_format = 'json'
            st.session_state.data_format = st.selectbox('Destination files format', formatlist, index = formatlist.index(st.session_state.data_format))

            st.write("---")

            # display random game parameters
            st.subheader('Rainbow colors and numbers parameters')
            # colors
            colors = st.multiselect('Rainbow colors drawn at random', ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet', 'Black', 'Grey', 'Brown', 'White'], ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet'])
            # numbers
            numbers = st.multiselect('Numbers drawn at random', [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], [1,2,3,4,5,6,7,8,9,10])
            # draws by file
            numberofdraws = st.number_input('Number of draws', value = 5)
            st.write("---")

            # dataframe generation function
            def drawsgeneration(fileformat):

                gamedf = pd.DataFrame(columns = ['timestamp', 'color', 'number'])
                for draw in range(0, numberofdraws):
                    gamedf = gamedf.append({'timestamp': datetime.datetime.now(), 'color': random.choice(colors), 'number': random.choice(numbers)}, ignore_index = True)
                    df =  gamedf

                    
                # upload file to S3
                # bufferize file
                # upload to S3 bucket
                now = datetime.datetime.now().strftime('%Y_%m_%d_%Hh%Mmn%Ss')
                
                    
                    #app_utils.upload_to_blob(blob_client,csv_buffer)
                blob_client = st.session_state.blob_service_client.get_blob_client(container = st.session_state.data_container, blob=st.session_state.data_blob +'/'+fileformat + '/colors-and-numbers_' + str(datetime.datetime.now()) + ".{}".format(fileformat))

                app_utils.upload_to_blob(blob_client,df,fileformat)
                st.markdown(":file_folder: <span style='color:blue;'>** colors-and-numbers_" + str(now) + "**</span>", unsafe_allow_html = True)
                st.markdown("<span style='color:purple;'>** ______ uploaded to Azure Blob Stroage in " + st.session_state.data_blob +'/'+fileformat + "**</span>", unsafe_allow_html = True)
                #return

            # display random game launch
            st.subheader('streaming simulation parameters')
            # looping time
            loopingtime = st.number_input('Looping time in seconds', value = 5)

            # looping time
            totaltime = st.number_input('Total time in seconds', value = 300)

            # launch loop to simulate streaming
            def buttonstreamtoBlob():
                # create folder(s) if necessary
                
                #app_utils.upload_to_blob(blob_client,csv_buffer)
                # loop
                start_loopingtime = time.time()
                start_totaltime = time.time()
                st.info("Last stream launched at " + datetime.datetime.now().strftime("%H H %M"))
                while True:
                    current_time = time.time()
                    elapsed_loopingtime = current_time - start_loopingtime
                    elapsed_totaltime = current_time - start_totaltime
                    # write stream
                    if elapsed_loopingtime > loopingtime:
                        # call of dataframe generation function
                        drawsgeneration(st.session_state.data_format)
                        
                        start_loopingtime = time.time()
                    # end stream
                    if elapsed_totaltime > totaltime:
                        st.info("Last stream ended at " + datetime.datetime.now().strftime("%H H %M"))
                        break
                return
            # display launch button
            col1, col2 = st.columns((0.70,0.30))
            with col2:
                st.button('Stream draws to BLOB', on_click = buttonstreamtoBlob, key = 'app_buttonstreamtoblob')
            st.write("---")
