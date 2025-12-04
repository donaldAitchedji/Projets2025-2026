import cv2
import mediapipe as mp
from pyfirmata import Arduino


# Configurations
cam_source = 0
V_default = 0
J_default = 0
R_default = 0
B_default = 0
clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
# 
leds_states =[V_default, J_default, R_default, B_default]
prev_leds_states=[V_default, J_default, R_default, B_default]

board = Arduino('COM6')  
led_V_pin = board.get_pin('d:2:o')
led_B_pin = board.get_pin('d:3:o')
led_J_pin = board.get_pin('d:4:o')
led_R_pin = board.get_pin('d:5:o')

# Initialisation de Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Fonction pour calculer la distance entre deux points
def calculate_distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5
   
# Fonction pour vérifier si les doigts sont levés ou baissés
def check_finger_positions(hand_landmarks):
    WRIST = hand_landmarks.landmark[0]
    INDEX_FINGER_TIP = hand_landmarks.landmark[8]
    INDEX_FINGER_MCP = hand_landmarks.landmark[5]
    MIDDLE_FINGER_TIP = hand_landmarks.landmark[12]
    MIDDLE_FINGER_MCP = hand_landmarks.landmark[9]
    PINKY_TIP = hand_landmarks.landmark[20]
    PINKY_MCP = hand_landmarks.landmark[17]
    THUMB_BASE = hand_landmarks.landmark[1]
    INDEX_BASE = hand_landmarks.landmark[5]
    THUMB_TIP = hand_landmarks.landmark[4]

    


    distances = {
        "index": calculate_distance(WRIST, INDEX_FINGER_TIP) > calculate_distance(WRIST, INDEX_FINGER_MCP),
        "middle": calculate_distance(WRIST, MIDDLE_FINGER_TIP) > calculate_distance(WRIST, MIDDLE_FINGER_MCP),
        "pinky": calculate_distance(WRIST, PINKY_TIP) > calculate_distance(WRIST, PINKY_MCP),
        "thumb": calculate_distance(THUMB_TIP, INDEX_BASE) > calculate_distance(THUMB_BASE, INDEX_BASE),
    }
    return distances


# Convert landmark positions to leds's states
def positions_to_states(hand_landmarks):
    leds_states = [V_default, J_default, R_default, B_default]
    
    distances = check_finger_positions(hand_landmarks)

    
    # Control V1,V2,J,R1,R2 leds based on finger positions
    leds_states[0] = 0 if not distances["thumb"] else 1
    leds_states[1] = 0 if not distances["index"] else 1
    leds_states[2] = 0 if not distances["middle"] else 1
    leds_states[3] = 0 if not distances["pinky"] else 1
    
    return leds_states

def draw_leds_on_screen(image, leds_states):
    # Coordonnées de base pour l'affichage
    positions = [(50, 400), (150, 400), (250, 400), (350, 400)]
    colors_on = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (0, 255, 255)]     # Blanc, Vert, Rouge, Jaune
    colors_off = [(220, 220, 220), (2, 74, 2), (132, 4, 4), (127, 114, 0)]       # Tons sombres

    for i in range(4):
        color = colors_on[i] if leds_states[i] else colors_off[i]
        cv2.circle(image, positions[i], 30, color, -1)  # LED simulée



# Initialisation de la caméra
cap = cv2.VideoCapture(0)

with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Erreur lors de la capture de la vidéo")
            break

        # Conversion en RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        distances=None
        if results.multi_hand_landmarks :
            for hand_landmarks in results.multi_hand_landmarks:
                leds_states=positions_to_states(hand_landmarks)

                if leds_states != prev_leds_states:
                    print("Etats des leds:",leds_states)
                    prev_leds_states = leds_states

                    # Set leds states
                    led_V_pin.write(leds_states[0])
                    led_J_pin.write(leds_states[1])
                    led_R_pin.write(leds_states[2])
                    led_B_pin.write(leds_states[3])

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                

        # Affichage de la vidéo
        cv2.putText(image, str(leds_states), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        draw_leds_on_screen(image, leds_states)
        cv2.imshow("Test leds", image)

        # Quitter si la touche 'ESC' est pressée
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
