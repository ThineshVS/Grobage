import streamlit as st
import pickle as pkle
import os.path
import pyrebase
import socket
import codecs
from streamlit.hashing import _CodeHasher
import streamlit.components.v1 as stc


config = {
    "apiKey": "AIzaSyAG3rD_v048j8lz2QH8_ZfXDT0Cx8cdR_U",
    "authDomain": "grobage.firebaseapp.com",
    "databaseURL": "https://grobage-default-rtdb.firebaseio.com/",
    "projectId": "grobage",
    "storageBucket": "grobage.appspot.com",
    "messagingSenderId": "342165659797",
    "appId": "1:342165659797:web:0bc3271cae24a079547b9c",
    "measurementId": "G-S3TEHSRTM1"}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
auth = firebase.auth()
st.title("Grobage")
st.subheader("")
name = ""
name1 = ""
upload_string = ""
i = 1
next = st.sidebar.button('Next')

new_choice = ['Home', 'Spacer', 'Forum', 'Track', 'Account Info', 'About us']

if os.path.isfile('next.p'):
    next_clicked = pkle.load(open('next.p', 'rb'))

    if next_clicked == len(new_choice):
        next_clicked = 0
else:
    next_clicked = 0


if next:

    next_clicked = next_clicked + 1

    if next_clicked == len(new_choice):
        next_clicked = 0


choice = st.sidebar.radio(
    "go to", ('Home', 'Spacer', 'Forum', 'Track', 'Account Info', 'About us'), index=next_clicked)


pkle.dump(new_choice.index(choice), open('next.p', 'wb'))

if choice == 'Home':
    def html_file(html_file2, width=100, height=100):
        file_in = codecs.open(html_file2, 'r')
        page = file_in.read()
        stc.html(page, width=width, height=height)
    html_file("srm.html")
elif choice == 'Spacer':
    st.subheader(name1)

    def spacer_input():
        email_info = st.text_input("Email Address \n")
        stock_name = st.text_input("Service Name \n")
        area_name = st.text_input("Area \n")
        contact_info = st.text_input("Contact Info\n")
        plant_count = st.slider(
            "How many plants/trees can be planted?", 1, 60, 1)
        image_file = st.file_uploader(
            "Upload Image of your plantation space", type=['png', 'jpeg', 'jpg'])
        st.write(type(image_file))
        get_location = st.button('Locate Me!')
        if get_location:
            import requests
            import json
            send_url = "http://api.ipstack.com/check?access_key=716837ec670b004b7728dfe71a174afd"
            geo_req = requests.get(send_url)
            geo_json = json.loads(geo_req.text)
            latitude = geo_json['latitude']
            longitude = geo_json['longitude']
            city = geo_json['city']
            location1 = "https://www.google.com/maps?q={},{}".format(
                latitude, longitude)
            st.write(location1)
        submit = st.button('Submit')
        if submit:
            name_of_the_file = "images/" + \
                str(stock_name) + str(plant_count) + ".jpg"
            path_on_cloud = name_of_the_file
            storage.child(path_on_cloud).put(image_file)
            email_info1 = email_info.rstrip("@gmail.com")
            from firebase import firebase
            Firebase = firebase.FirebaseApplication(
                'https://grobage-default-rtdb.firebaseio.com/', None)
            data = {'Service': stock_name,
                    'Name': email_info1,
                    'Area': area_name,

                    'imageid': name_of_the_file
                    }
            upload_string = "/" + stock_name + "/" + email_info1 + "/"
            result = Firebase.post(upload_string, data)
    spacer_input()
elif choice == 'Forum':
    st.subheader(name1)
    st.write(
        'Our team is working on this new feature and soon will update reflect in the webapp')
elif choice == 'Track':
    from firebase import firebase
    Firebase = firebase.FirebaseApplication(
        'https://grobage-default-rtdb.firebaseio.com/', None)
    result2 = Firebase.get("/plantation/", name)
    key1 = tuple(result2.keys())[0]
    key2 = tuple(result2[key1].keys())[0]
    #key3 = tuple(result2[key2].keys())[0]
    area = result2[key1][key2]['Area']
    name_final = result2[key1][key2]['Name']
    service_of = result2[key1][key2]['Service']
    imageid_of = result2[key1][key2]['imageid']
    # st.write(result2)
    # st.write(area)

    intro00 = "Request" + str(i)
    intr01 = "Area " + "-" + area
    intr02 = "Name " + "-" + name_final
    intr03 = "Area " + "-" + service_of
    intr04 = "Area " + "-" + imageid_of
    st.write(intro00)
    st.write(intr01)
    st.write(intr02)
    st.write(intr03)
    st.write(intr04)
    i = i+1
elif choice == 'Account Info':

    usern = st.empty()
    passw = st.empty()

    username = usern.text_input("Email \n")
    Password = passw.text_input("Password \n")

    def login(email, password):
        popup = st.empty()
        popup.write("Log in...")
        name = username.rstrip("@gmail.com")
        name1 = "welcome" + name + "!"
        st.subheader(name1)
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            popup.write("Successfully logged in!")

        except:
            #popup.write("Invalid email or password")

            return
    col1, col2, logg, col4, col5 = st.beta_columns(5)
    col1, col2, newuse, col4, col5 = st.beta_columns(5)
    if logg.button('Login') == True:
        login(username, Password)
        un = username
        login(usern, passw)
        usern.empty()
        passw.empty()
        username = ""
        password = ""

        from firebase import firebase
        Firebase = firebase.FirebaseApplication(
            'https://grobage-default-rtdb.firebaseio.com/', None)
        result2 = Firebase.get("/plantation/", name)
        key1 = tuple(result2.keys())[0]
        key2 = tuple(result2[key1].keys())[0]
        #key3 = tuple(result2[key2].keys())[0]
        area = result2[key1][key2]['Area']
        name_final = result2[key1][key2]['Name']
        service_of = result2[key1][key2]['Service']
        imageid_of = result2[key1][key2]['imageid']
        # st.write(result2)
        # st.write(area)

        intro00 = "Request" + str(i)
        intr01 = "Area " + "-" + area
        intr02 = "Name " + "-" + name_final
        intr03 = "Area " + "-" + service_of
        intr04 = "Area " + "-" + imageid_of
        st.write(intro00)
        st.write(intr01)
        st.write(intr02)
        st.write(intr03)
        st.write(intr04)
        i = i+1

        # st.write(result2)
    elif newuse.button('New user'):
        st.write("creating a new account")

        def signup(email, password):
            print("Sign up...")
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)

                st.write("please reload the page and proceed with login")
            except:
                print("Email already exists")
            return
        signup(username, Password)
