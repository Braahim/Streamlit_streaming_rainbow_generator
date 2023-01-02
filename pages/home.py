import streamlit as st


import configparser
import time


################################################################################
###################### SETUP : BEGINNING #######################################
################################################################################
# import your page modules here

import utils.app_utils
from azure.storage.blob import  BlobServiceClient,generate_container_sas, ContainerSasPermissions


def page():


    # streamlit display config
    ################################################################################
    ###################### SETUP : ENDING ##########################################
    ################################################################################
    col1, col2, col3= st.columns(3)

    with col2:
        st.image("https://azure.github.io/Storage/images/storage-logo.png")

    st.write("---")
    # configuration management
    config = configparser.ConfigParser()
    configpath = st.session_state.path_this + '/data/config.conf'
    config.read(configpath)

    # Azure account choice
    azureaccountslist = config.sections()
    st.selectbox('Azure Storage account selected', azureaccountslist, index = 0, key = 'app_selectboxaccount')

    st.warning('To add a storage account, please update conf file')

    # tokens
    st.session_state.data_azureaccount = config.get(st.session_state.app_selectboxaccount, 'account')
    st.session_state.secret_accountKey = config.get(st.session_state.app_selectboxaccount, 'account_key')
    st.session_state.secret_url = config.get(st.session_state.app_selectboxaccount, 'url')
    st.session_state.blob_service_client = BlobServiceClient(st.session_state.secret_url, st.session_state.secret_accountKey)

    st.write("---")
    
    with st.spinner('Wait for it...'):

        time.sleep(5)
        st.info('Azure storage account : ' + st.session_state.data_azureaccount)
        account_info = st.session_state.blob_service_client.get_account_information()
        st.info('Using Storage SKU: {}'.format(account_info['sku_name']))
        st.info('Version: {}'.format(account_info['version']))
        if 'balloons' not in st.session_state:
            st.session_state.balloons = st.balloons()
        else : st.session_state.balloons = st.balloons()


    st.write("---")

