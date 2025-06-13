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
    "🎻 Violin": 40
}

if "instrument" not in st.session_state:
    st.session_state.instrument_name = list(INSTRUMENTS.keys())[0]

st.subheader("Select Instrument")
left_spacer, content, right_spacer = st.columns([1, 10, 1]) # Adjust the ratio as needed 

with content: # set main content area
    col1, col2, col3 = st.columns(3)

#make buttons for each intrument 
with col1:
    if st.button("🎹 Acoustic Grand Piano", use_container_width=True):
        st.session_state.instrument_name = "🎹 Acoustic Grand Piano"
with col2:
    if st.button("🎸 Acoustic Guitar", use_container_width=True):
        st.session_state.instrument_name = "🎸 Acoustic Guitar"
with col3:
    if st.button("🎻 Violin", use_container_width=True):
        st.session_state.instrument_name = "🎻 Violin"

instrument_session_name = st.session_state.instrument_name
st.markdown(f"**Selected Instrument:** {instrument_session_name}")

instrument = INSTRUMENTS[instrument_session_name]

if "running" not in st.session_state:
    st.session_state.running = False

def start_midi_controller():
    MidiController(instrument_id=instrument, show_window=True)

if st.button("Start MIDI Controller" if not st.session_state.running else "Stop MIDI Controller"):
    if not st.session_state.running:
        st.session_state.running = True
        start_midi_controller()
    else:
        st.session_state.running = False
        st.write("MIDI Controller stopped.")
