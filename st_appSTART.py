import streamlit as st

import os
import data
import configparser







import streamlit as st

import os
#import configparser


################################################################################
###################### SETUP : BEGINNING #######################################
################################################################################
# import your page modules here
from pages import home, app, st_generate_twitter
# streamlit display config

st.set_page_config( page_title = 'Cloud Azure app', page_icon = ':cloud:')#, layout = "wide", initial_sidebar_state = "expanded")
################################################################################
###################### SETUP : ENDING ##########################################
################################################################################

class multipage:
    def __init__(self):
        self.pages = []
    def add_page(self, title, func):
        self.pages.append({
            'title': title,
            'function': func})
    def run(self):
        page = st.sidebar.radio(
            'Menu',
            self.pages,
            format_func = lambda page : page['title'])
        st.session_state.app_pagename = page['title']
        page['function']()

page = multipage()

################################################################################
###################### SETUP : BEGINNING #######################################
################################################################################
# sidebar titles management
st.sidebar.title('Cloud Azure management')
# add all your application here
page.add_page('Home', home.page)
page.add_page('Streaming Demo', app.page)
page.add_page('Generate tweets', st_generate_twitter.page)



################################################################################
###################### SETUP : ENDING ##########################################
################################################################################

# general path management
st.session_state.path_root = os.getcwd()
st.session_state.path_this = os.path.dirname(os.path.realpath(__file__))
st.session_state.path_data = '/'.join(st.session_state.path_this.split('/')[:-1])

# the main app
page.run()

