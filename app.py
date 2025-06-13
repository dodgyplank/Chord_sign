import streamlit as st
import pyttsx3
from streamlit_extras.add_vertical_space import add_vertical_space
from midi_controller import start_midi_controller, stop_midi_controller

# Start the pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Sidebar layout and credits
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

# Main title and description
st.title("Chord Sign - Hand Tracking MIDI Controller")

st.markdown("""
**Application Description:** This is a hand tracking MIDI controller that converts hand gestures into musical notes. 
Use your camera to detect hand positions and play music by touching your thumb to different fingers.
""")

# Instrument mapping with General MIDI program numbers
INSTRUMENTS = {
    "🎹 Acoustic Grand Piano": 0,
    "🎸 Acoustic Guitar": 25,
    "🎻 Violin": 40
}

# Initialize session state variables
if "instrument_name" not in st.session_state:
    st.session_state.instrument_name = list(INSTRUMENTS.keys())[0]

# Subheader and column layout for instrument selection
st.subheader("Select Instrument")
left_spacer, content, right_spacer = st.columns([1, 10, 1]) # Adjust the ratio as needed 

with content: # set main content area
    col1, col2, col3 = st.columns(3)

# Buttons for each instrument
with col1:
    if st.button("🎹 Acoustic Grand Piano", use_container_width=True):
        st.session_state.instrument_name = "🎹 Acoustic Grand Piano"
        engine.say("Acoustic Grand Piano selected")
        engine.runAndWait()

with col2:
    if st.button("🎸 Acoustic Guitar", use_container_width=True):
        st.session_state.instrument_name = "🎸 Acoustic Guitar"
        engine.say("Acoustic Guitar selected")
        engine.runAndWait()

with col3:
    if st.button("🎻 Violin", use_container_width=True):
        st.session_state.instrument_name = "🎻 Violin"
        engine.say("Violin selected")
        engine.runAndWait()

# Display selected instrument
instrument_session_name = st.session_state.instrument_name
st.markdown(f"**Selected Instrument:** {instrument_session_name}")

# Get MIDI instrument number
instrument = INSTRUMENTS[instrument_session_name]
button_label = "Start MIDI Controller" if not st.session_state.running else "Stop MIDI Controller"
# Button to start/stop the MIDI controller
if st.button(button_label):
    if not st.session_state.running:
        st.session_state.running = True
        start_midi_controller(instrument_id=instrument, show_window=True)
        engine.say(f"{instrument_session_name} MIDI Controller started")
        engine.runAndWait()
    else:
        st.session_state.running = False
        stop_midi_controller()
        st.write("MIDI Controller stopped.")
        engine.say(f"{instrument_session_name} MIDI Controller stopped")
        engine.runAndWait()
