import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
# property no. 3 is the width and property no. 4 is the height of the window
# this sizing is done to make sure that the video screen is always the same size on all devices.
cap.set(3, 640)
cap.set(4, 480)

# ----------------------------------- Detecting The hand ----------------------------------------------
detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0, 0]     # [AI, Player]


def read_image():
    # ------------------------------- READING THE BACKGROUND AND PLAYER -----------------------------------------
    # the bg image will be loaded continuously on every iteration. This is done because, other images will be loaded on
    # top of this image which should be changed on every iteration. When this image is loaded everytime, the image on
    # top of it will get erased and a new window will be displayed for the next iteration.
    imgBG_ = cv2.imread("Resources/BG.png")
    success_, img_ = cap.read()
    return imgBG_,success_, img_


def scale_image(img_):
    # ------------------------------- SCALING THE VIDEO TO FIT INTO THE PLAYER BOX -------------------------------
    # on opening the bg in paint we find that the height of the inner player box = 420 and width = 400 but the size of
    # the video screen is 480. so, we need to scale it down(scaling down involves reducing both height and width) by
    # (420/480) = 0.875. Once the height of the screen is fixed, we can crop its sides in order to fit it into the box.
    # now, width of the screen would be 640*0.875 = 560. but the width of the box is 400. So, the size of the box to be
    # reduced is 560-400=160. If cropping is done on both sides, each side should be reduced be 80units
    imgScaled_ = cv2.resize(img_, (0, 0), None, 0.875, 0.875)
    # no change is done for height, the width is cropped to get image from 80pixels to 480pixels
    imgScaled_ = imgScaled_[:, 80:480]
    return imgScaled_


def embed_video(imgScaled_):
    # -------------------------------- PUTTING THE IMAGE ON TOP OF THE BACKGROUND --------------------------------
    # we have to put the video screen on top of the background image at a specified position. This can be done by
    # specifying the coordinates of start(top left corner) and end point(bottom right corner). We can get the values
    # by opening the image in paint. The width and height should be exactly the same as the imgScaled for this to work.
    imgBG[234:654, 795:1195] = imgScaled_


def player(hands_, imgBG_):
    # this function is called once at the end of 3secs.
    # calculates the number of fingers that are up to calculate the playerMove
    # if no hand is detected, playerMove = 0
    # the playerMove is assigned values according to the images stored in Resources folder
    playerMove = 0
    if hands_:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers == [0, 0, 0, 0, 0]:
            playerMove = 1      # image number for Rock is 1
        elif fingers == [1, 1, 1, 1, 1]:
            playerMove = 2      # image number for paper is 2
        elif fingers == [0, 1, 1, 0, 0]:
            playerMove = 3      # image number for scissor is 3

    return playerMove


def playAI(imgBG_):
    # images are stored in numbers. a random num is generated and the corresponding image is displayed on screen
    randomNumber = random.randint(1, 3)
    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
    imgBG_ = cvzone.overlayPNG(imgBG_, imgAI, [145, 300])
    return randomNumber, imgAI


def evaluate_score(playerMove, randomNumber):
    # 1:Rock, 2:Paper, 3:Scissor according to images in Resources folder

    # Player wins
    if (playerMove == 1 and randomNumber == 3) or \
            (playerMove == 2 and randomNumber == 1) or \
            (playerMove == 3 and randomNumber == 2):
        scores[1] += 1

    # AI wins
    if (playerMove == 3 and randomNumber == 1) or \
            (playerMove == 1 and randomNumber == 2) or \
            (playerMove == 2 and randomNumber == 3):
        scores[0] += 1


def win_lose_message():
    if scores[1] == 5 and scores[0] < 5:
        cv2.putText(imgBG, "YOU WIN !!!", (820, 430), cv2.FONT_HERSHEY_PLAIN, 4, (0, 128, 255), 3)
        return True
    elif scores[0] == 5 and scores[1] < 5:
        cv2.putText(imgBG, "YOU LOSE!", (820, 430), cv2.FONT_HERSHEY_PLAIN, 4, (0, 128, 255), 3)
        return True
    return False


def show_text():
    cv2.putText(imgBG, "Press 'q' to quit", (532, 535), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 1)
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    cv2.putText(imgBG, str(scores[1]), (1115, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)


while True:
    imgBG, success, img = read_image()
    imgScaled = scale_image(img)
    # -------------------------------------------------- FIND HANDS -----------------------------------------------
    hands, img = detector.findHands(imgScaled)
    # if hands are detected, we can calculate the no. of fingers that are up to find if it is a rock, paper or scissor
    # startGame will be true whenever a player presses 's' key
    # if stateResult is False, it means the end of the timer has not been reached in that case, the timer will
    # be updated. if end of timer has been reached, we will ask it to state the result and make it true

    if startGame:
        # If end of time(3secs) is not reached, stateResult will be false
        if stateResult is False:
            # calculates time on every iteration(every 1 sec. So, it adds 1sec) and subtract initial time from it.
            # So, the difference increases by 1 on every iteration.
            timer = time.time() - initialTime
            # updates time on screen
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 6)
            # timer stops at 3 secs
            if timer > 3:
                stateResult = True
                timer = 0
                # calculates playerMove at the end of time
                playerMove = player(hands, imgBG)
                # calculates AI Move at the end of time
                randomNumber, imgAI = playAI(imgBG)
                # evaluates the score using the Moves
                evaluate_score(playerMove, randomNumber)
        else:
            cv2.putText(imgBG, "Press 's' to start", (527, 496), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 1)
    else:
        cv2.putText(imgBG, "Press 's' to start", (527, 496), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 1)

    # ------------------------------------------------ EMBED VIDEO ---------------------------------------------------
    # the video will be embedded until winner is False. If someone wins, winner message will be displayed in player box.
    winner = win_lose_message()
    if winner is False:
        embed_video(imgScaled)
        cv2.putText(imgBG, "SCORE 5 TO WIN", (510, 330), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


    # -------------------------------------------------- EMBED AI ------------------------------------------------------
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, [145, 300])

    # ---------------------------------------------- SHOW ALL TEXT ON SCREEN ------------------------------------------
    show_text()

    # ------------------------------------------------ DISPLAY WINDOW -------------------------------------------------
    cv2.imshow("Rock Paper Scissor - AI", imgBG)
    # displays the window infinitely
    key = cv2.waitKey(1)
    # --------------------------------------------------- START GAME ---------------------------------------------------
    # when s is pressed it starts the game
    if key == ord('s'):
        # this will reset the score. 's' should be pressed once again to start the game
        if winner is True:
            scores = [0, 0]

        # this will start the game
        else:
            startGame = True
            initialTime = time.time()
            stateResult = False
    # ----------------------------------------- QUIT GAME -----------------------------------------------
    if key == ord('q'):
        break
