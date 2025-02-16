import streamlit as st

st.title('Session State Counter')

if "a_counter" not in st.session_state:
    st.session_state.a_counter = 0

if "boolean" not in st.session_state:
    st.session_state.boolean = False

st.write("st.session_state object:", st.session_state)

st.write("a_counter is :", st.session_state.a_counter)
st.write("boolean is :", st.session_state["boolean"])

for key in st.session_state.keys():
    st.write(key)

for value in st.session_state.values():
    st.write(value)

for item in st.session_state.items():
    st.write(item)


button = st.button("Increment")
"before pressing button", st.session_state
if button:
    st.session_state.a_counter += 1
    st.session_state.boolean = not st.session_state.boolean
    "after pressing button", st.session_state


for key in st.session_state.keys():
    del st.session_state[key]

st.session_state


number = st.slider('Select a number:', 1, 10, key="slider")

st.write(st.session_state.slider)

