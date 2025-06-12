import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from midi_controller import MidiController

with st.sidebar:
    st.title("🛠️ Powered by")
    st.markdown("""
    - [OpenCV](https://opencv.org) for camera and image processing  
    - [cvzone](https://github.com/cvzone/cvzone) for hand tracking  
    - [pygame.midi](https://www.pygame.org/docs/ref/midi.html) for MIDI output  
    - [Streamlit](https://streamlit.io) for the web UI  
    - [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras) for layout utilities
    """)
    add_vertical_space(2)

st.title("Chord_sign")

INSTRUMENTS = {
    "🎹 Acoustic Grand Piano": 0,
    "🎸 Acoustic Guitar": 25,
    "🎻Violin": 40
}

if "running" not in st.session_state:
    st.session_state.running = False

instrument_name = st.selectbox("Select Instrument" , list(INSTRUMENTS.keys()))
instrument = INSTRUMENTS[instrument_name]

def start_midi_controller():
    MidiController(instrument_id=instrument, show_window=True)

if st.button("Start MIDI Controller" if not st.session_state.running else "Stop MIDI Controller"):
    if not st.session_state.running:
        st.session_state.running = True
        start_midi_controller()
    else:
        st.session_state.running = False
        st.write("MIDI Controller stopped.")
