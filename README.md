# RockPaperScissorAI---OpenCV

Packages used:
1. opencv-python
2. cvzone
3. random
4. time

Steps:
1. User Video is embedded on top of the player box in the background image using OpenCV.
2. Initially, the score of the Player and The AI is set to 0. 
3. Once the player press the 's' key, the game starts.
4. HandDetector class from the cvzone package is used for detecting the player's hand.
5. A timer is set for 3 seconds at the end of which the player move and the AI move is calculated.
6. The player move is calculated by counting the numbers of fingers that are up when the timer ends. Player Move is assigned values corresponding to the images in the Resources folder.
7. The AI move is calculated by selecting a digit randomly from 1 to 3 and the corresponding image from the Resources folder is displayed.
8. Then, the moves are compared to calculate the score.
9. If the Player scores 5 before AI does, then he wins otherwise he loses.
10. The winner or loser message is displayed on the screen
11. At the end of the game, the player can press 's' to reset the score values and new game will start when 's' is pressed again.
12. The player can quit the game anytime by pressing the 'q' key.
