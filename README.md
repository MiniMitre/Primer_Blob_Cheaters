# Primer_Blob_Cheaters
A script to automatically play the blob cheater game on primerlearning.org

# Prerequisites

- Python
  - Pyautogui
  - numpy

# Setup instructions

Go to www.primerlearning.org, and start a game in full screen mode on your main display (verified as working on 16x9 1080p displays only).
Run the `auto-flipper.py` script, the code will stop when it is close to 4540 correct guesses, at which point you take over and decide what score you would like to attempt to submit.

Due to a bug in the submission of the scores, attempts with a lot of flips remaining after 4500 correct guesses are more likely to be submitted without error.

You can run `print.py` to automatically continue to attempt to submit the score after manually throwing away (guessing incorrectly) the run at the desired score.
