import cv2
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector

# global variables for cleanup
cap = None
player = None

def start_midi_controller(instrument_id=0, show_window=True):
    global cap, player

    # 🎹 Initialize Pygame MIDI
    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(instrument_id)  # 0 = Acoustic Grand Piano

    # 🎐 Initialize Hand Detector
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8)

    # Notes in C major scale for each finger
    notes = {
        "left": {
            "index": 65,   
            "middle": 64,    
            "ring": 62,
            "pinky": 60, 
        },
        "right": {
            "index": 67,   
            "middle": 69,    
            "ring": 71,
            "pinky": 72,  
        }
    }

    BUFFER_TIME = 0.1

    # Track Previous States to Stop Chords
    prev_state = (None, None, None)  # (Hand, Finger, Note)
    last_play_times = {}

    while True:
        success, img = cap.read()
        if not success:
            print("❌ Camera not capturing frames")
            continue

        hands, img = detector.findHands(img, draw=True)

        if hands:
            for hand in hands:
                hand_type = "left" if hand["type"] == "Left" else "right"
                lmList = hand["lmList"]
                thumb_tip = (lmList[4][0], lmList[4][1])  # Thumb tip coordinates
                fingers = detector.fingersUp(hand)
                finger_names = [("index", 8), ("middle", 12), ("ring", 16), ("pinky", 20)]
                shortest_distance = (None, None)

                for i, finger in enumerate(finger_names):
                    finger_name, finger_id = finger
                    finger_tip = (lmList[finger_id][0], lmList[finger_id][1])
                    distance = detector.findDistance(thumb_tip, finger_tip)[0]
                    if (shortest_distance[1] is None) or (distance < shortest_distance[1]):
                        shortest_distance = (finger_name, distance)

                note = notes[hand_type].get(shortest_distance[0])
                current_state = (hand_type, shortest_distance[0], note)  # (Hand, Finger, Note)

                # If finger is close to the thumb
                if shortest_distance[1] < 30:  
                    current_time = time.time()     

                    # Get last play time for the current note (default to 0 if not played before)
                    last_play_time = last_play_times.get(note, 0)

                    # If no previous state, play the note
                    if prev_state[0] is None or (current_time - last_play_time > BUFFER_TIME):
                        player.note_on(note, 127)  # Start playing
                    
                    elif prev_state != current_state:
                        player.note_off(prev_state[2], 127)  # Stop previous note
                        player.note_on(note, 127)  # Start new note

                    prev_state = current_state
                    last_play_times[note] = current_time  # Update last play time for this note

        if show_window:
            cv2.imshow("Hand Tracking MIDI Chords", cv2.flip(img, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stop_midi_controller()


def stop_midi_controller():
    global cap, player
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    if player:
        player.close()
    pygame.midi.quit()
