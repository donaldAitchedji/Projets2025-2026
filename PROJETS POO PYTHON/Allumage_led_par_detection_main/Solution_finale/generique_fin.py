import cv2
import mediapipe as mp
from pyfirmata import Arduino


# Configurations
cam_source = 0
x_default = 75
y1_default = 75
y2_default = 120
y3_default = 50
z_default = 40
claw_default= 180
palm_angle_min, palm_angle_mid = -50, 20
clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
# Angles initiaux pour les servos
servo_angle = [x_default, y1_default, y2_default, y3_default, z_default, claw_default]


board = Arduino('COM10')  
servo_x_pin = board.get_pin('d:3:s')
servo_y1_pin = board.get_pin('d:5:s')
servo_y2_pin = board.get_pin('d:6:s')
servo_y3_pin = board.get_pin('d:9:s')
servo_z_pin  = board.get_pin('d:10:s')
servo_claw_pin = board.get_pin('d:11:s')
increment = 2  # Pas de changement de l'angle


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
    RING_TIP=hand_landmarks.landmark[16]
    RING_MCP=hand_landmarks.landmark[13]

    


    distances = {
        "index": calculate_distance(WRIST, INDEX_FINGER_TIP) > calculate_distance(WRIST, INDEX_FINGER_MCP),
        "middle": calculate_distance(WRIST, MIDDLE_FINGER_TIP) > calculate_distance(WRIST, MIDDLE_FINGER_MCP),
        "pinky": calculate_distance(WRIST, PINKY_TIP) > calculate_distance(WRIST, PINKY_MCP),
        "thumb": calculate_distance(THUMB_TIP, INDEX_BASE) > calculate_distance(THUMB_BASE, INDEX_BASE),
        "ring": calculate_distance(WRIST, RING_TIP) > calculate_distance(WRIST, RING_MCP)
    }
    return distances




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

        # Initialisation des landmarks pour les deux mains
        right_hand_landmarks = None
        left_hand_landmarks = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[idx].classification[0].label
                if hand_label == "Left":
                    right_hand_landmarks = hand_landmarks
                elif hand_label == "Right":
                    left_hand_landmarks = hand_landmarks

                # Dessiner les landmarks
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

            if right_hand_landmarks and left_hand_landmarks:
                # Vérification si l'index gauche est levé
                #lef = is_finger_up(left_hand_landmarks, wrist_index=0, tip_index=8, mcp_index=5)
                distances_left = check_finger_positions(left_hand_landmarks)
                distances_right= check_finger_positions(right_hand_landmarks)


                

                if distances_left.get("index"):  # Exécution autorisée uniquement si l'index gauche est levé
                    # Vérification pour l'index droit
                    right_index_up = distances_right.get("index")

                    if right_index_up==0:
                        # Si l'index droit est baissé, incrémenter l'angle
                        new_angle = servo_angle[1] + increment
                    else:
                        # Si l'index droit est baissé, décrémenter l'angle
                        new_angle = servo_angle[1]- increment

                    # Limiter l'angle à [0, 180]
                    new_angle = clamp(new_angle, 0, 170)

                    # Envoyer l'angle uniquement s'il est différent
                    if new_angle != servo_angle[1]:
                        servo_y1_pin.write(new_angle)
                        servo_angle[1] = new_angle


                if distances_left.get("middle"):  # Exécution autorisée uniquement si le majeur gauche est levé
                    # Vérification pour le majeur droit
                    right_middle_up = distances_right.get("middle")

                    if right_middle_up:
                        # Si l'index droit est baissé, incrémenter l'angle
                        new_angle = servo_angle[2] + increment
                    else:
                        # Si l'index droit est baissé, décrémenter l'angle
                        new_angle = servo_angle[2] - increment

                    # Limiter l'angle à [60, 180]
                    new_angle = clamp(new_angle, 60, 180)

                    # Envoyer l'angle uniquement s'il est différent
                    if new_angle != servo_angle[2]:
                        servo_y2_pin.write(new_angle)
                        servo_angle[2] = new_angle
                
                if distances_left.get("ring"):  # Exécution autorisée uniquement si l'annulaire gauche est levé
                    # Vérification pour l'annulaire droit
                    right_ring_up = distances_right.get("ring")

                    if right_ring_up==0:
                        # Si l'annulaire droit est baissé, incrémenter l'angle
                        new_angle = servo_angle[3] + increment
                    else:
                        # Si l'annulaire droit est levé, décrémenter l'angle
                        new_angle = servo_angle[3] - increment

                    # Limiter l'angle à [200, 50]
                    new_angle = clamp(new_angle,50 , 200)

                    # Envoyer l'angle uniquement s'il est différent
                    if new_angle != servo_angle[3]:
                        servo_y3_pin.write(new_angle)
                        servo_angle[3] = new_angle

                if distances_left.get("pinky"):  # Exécution autorisée uniquement si l'auriculaire gauche est levé
                    # Vérification pour l'auriculaire droit
                    right_pinky_up = distances_right.get("pinky")

                    if right_pinky_up:
                        # Si l'auriculaire droit est levé, incrémenter l'angle
                        new_angle = servo_angle[4] + increment
                    else:
                        # Si l'auriculaire droit est baissé, décrémenter l'angle
                        new_angle = servo_angle[4] - increment

                    # Limiter l'angle à [0, 180]
                    new_angle = clamp(new_angle, 0, 180)

                    # Envoyer l'angle uniquement s'il est différent
                    if new_angle != servo_angle[4]:
                        servo_z_pin.write(new_angle)
                        servo_angle[4] = new_angle


                if distances_left.get("thumb"):  # Exécution autorisée uniquement si le pouce gauche est levé
                    # Vérification pour le pouce droit
                    right_thumb_up = distances_right.get("thumb")

                    if right_thumb_up:
                        # Si le pouce droit est baissé, incrémenter l'angle
                        new_angle = servo_angle[5] + increment
                    else:
                        # Si le pouce droit est baissé, décrémenter l'angle
                        new_angle = servo_angle[5] - increment

                    # Limiter l'angle à [0, 180]
                    new_angle = clamp(new_angle, 0, 180)

                    # Envoyer l'angle uniquement s'il est différent
                    if new_angle != servo_angle[5]:
                        servo_claw_pin.write(new_angle)
                        servo_angle[5] = new_angle
                    
                print("Angle du servo:",servo_angle)
                    
                

        # Affichage de la vidéo
        cv2.putText(image, str(servo_angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("Test Servo", image)

        # Quitter si la touche 'ESC' est pressée
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
