from git import refresh
import streamlit as st
import requests
import json 

api_url="http://127.0.0.1:8000/auth/Token"
url2="http://127.0.0.1:8000/todos/user"

if not "login" in st.session_state:
    st.session_state["login"] = False
    st.session_state["Prosjekt"]= None

def login(nr):
    if st.session_state["login"]:
        return True
    else:
        with st.form(key=f"loginForm {nr}"):
            st.title(f"Login")
            username=st.text_input(label="username",placeholder="Username")
            password=st.text_input(label="password",placeholder="password",type="password")
            col__=st.columns(6)
            with col__[0]:
                submit=st.form_submit_button("Login")
            with col__[1]:
                st.write("[Register?](http://127.0.0.1:8000/auth/register)")
            token=None
            if submit:
                data = {'username': username, 'password': password}
                response = requests.post(api_url, data=data)
                if response.status_code==200:
                    token=json.loads(response.content)["token"]
                    headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {token}"}
                if token is not None:
                    st.session_state["headers"]=headers
                    st.session_state["token"]=token
                    st.session_state["login"] = True
                    st.experimental_rerun()
                    return True
                else:
                    st.session_state["login"] = False
                    st.warning("Wrong password or username")
                    return False

def velg_prosjekt():
    r=requests.get(url2,headers=st.session_state["headers"])
    result=json.loads(r.content)
    with st.form("velgProsjekt"):
        velg_prosjekt=st.selectbox(options=([prosjekt["title"] for prosjekt in result]),label="Velg prosjekt")
        velg_prosjekt_knapp=st.form_submit_button("Velg prosjekt")
        if velg_prosjekt_knapp:
            velg_prosjekt
        return velg_prosjekt

def main():
    # button_=st.button("Read from database")
    # if button_
    refresh=st.button("Refresh")
    if refresh:
        r=requests.get(url2,headers=st.session_state["headers"])
        result=json.loads(r.content)
    try:
        r=requests.get(url2,headers=st.session_state["headers"])
        result=json.loads(r.content)
    except:
        st.warning("Token invalid, need to relog")
        st.session_state["login"]=False
        st.session_state["Prosjekt"]= None 
        st.experimental_rerun()
    # lag_p=st.checkbox("Lag nytt prosjekt")
    # if lag_p:

    with st.form("velgProsjekt"):
        velg_prosjekt=st.selectbox(options=([prosjekt["title"] for prosjekt in result]),label="Velg prosjekt")
        col_=st.columns(2)
        with col_[0]:
            velg_prosjekt_knapp=st.form_submit_button("Velg prosjekt")
        with col_[1]:
            st.write("[Legg til prosjekt](http://127.0.0.1:8000/projects/add-project)")
        if velg_prosjekt_knapp:
            velg_prosjekt
            st.session_state["Prosjekt"]=velg_prosjekt
            st.experimental_rerun()

def main2():
    prosjekt=st.session_state["Prosjekt"]
    st.title("Norspunt")
    st.title(f"Prosjekt {prosjekt}")
    log=st.sidebar.button(label="Logout")
    tt=st.sidebar.button(label="Velg nytt prosjekt")
    if log:
        st.session_state["login"]=False
        st.session_state["Prosjekt"]= None 
        # if this is not set to none, it will remember prosject when logged out: can be nice  with validate token/cookie 
        st.experimental_rerun()
        #Test if validate_cookie har expierd, if set login to false og rerun
    if tt:
        st.session_state["Prosjekt"]=None
        st.experimental_rerun()
    st.write("Insert norspunt app()")
    p=st.slider("pick a number",1,100)
    pp=st.number_input(label="pick a number ")
    st.write(p*pp/3.4151)
    

if __name__ == "__main__":
    login(0)
    if st.session_state["login"] and st.session_state["Prosjekt"] is None:
        main()
    elif st.session_state["login"] and st.session_state["Prosjekt"] is not None:
        main2()
    # elif not st.session_state["login"]:
    #     login(1)

    