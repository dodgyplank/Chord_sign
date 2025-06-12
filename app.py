import streamlit as st 
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space

with st.sidebar:
    st.title('ChordSign')
    st.markdown('''
    ## About
    This app uses opencv and streamlit to detect hand gestures and convert them into musical chords.:
    - [Streamlit](https://streamlit.io/)
    - [OpenCV](https://opencv.org/)
    ''')
    add_vertical_space(3)
    st.write('This is my linkedin🤗: )')
 
def main():
    np.set_printoptions(suppress=True)
    image = st.camera_input(label ="Capture Image", key="First Camera", label_visibility="hidden")# this captures the image 
    if image is not None:
        st.success("Image captured successfully! (Processing can be added here)")

# Run the app
if __name__ == "__main__":
    main()