import cv2
import mediapipe as mp
from pyfirmata import Arduino

# Configuration de la broche du servo
servo_pin = 3  # Broche Arduino connectée au servo
board = Arduino('COM14')  # Remplacez 'COM13' par votre port Arduino
servo = board.get_pin(f'd:{servo_pin}:s')  # Configuration de la broche en mode servo

# Initialisation de Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Fonction pour vérifier si un doigt est levé ou baissé
def is_finger_up(landmarks, wrist_index, tip_index, mcp_index):
    WRIST = landmarks.landmark[wrist_index]
    FINGER_TIP = landmarks.landmark[tip_index]
    FINGER_MCP = landmarks.landmark[mcp_index]
    return (FINGER_TIP.y < FINGER_MCP.y) and (FINGER_TIP.y < WRIST.y)

# Clamp pour limiter les angles
clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

# Variables initiales
servo_angle = 90  # Angle initial du servo
increment = 1  # Pas de changement de l'angle

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
                if hand_label == "Right":
                    right_hand_landmarks = hand_landmarks
                elif hand_label == "Left":
                    left_hand_landmarks = hand_landmarks

                # Dessiner les landmarks
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

            if right_hand_landmarks and left_hand_landmarks:
                # Vérification si l'index gauche est levé
                left_index_up = is_finger_up(left_hand_landmarks, wrist_index=0, tip_index=8, mcp_index=5)

                if left_index_up:  # Exécution autorisée uniquement si l'index gauche est levé
                    # Vérification pour l'index droit
                    right_index_up = is_finger_up(right_hand_landmarks, wrist_index=0, tip_index=8, mcp_index=5)

                    if right_index_up:
                        # Si l'index droit est levé, incrémenter l'angle
                        new_angle = servo_angle + increment
                    else:
                        # Si l'index droit est baissé, décrémenter l'angle
                        new_angle = servo_angle - increment

                    # Limiter l'angle à [0, 180]
                    new_angle = clamp(new_angle, 0, 180)

                    # Envoyer l'angle uniquement s'il est différent
                    if new_angle != servo_angle:
                        servo.write(new_angle)
                        servo_angle = new_angle
                        print(f"Angle du servo: {servo_angle}")

        # Affichage de la vidéo
        cv2.imshow("Test Servo", image)

        # Quitter si la touche 'ESC' est pressée
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
