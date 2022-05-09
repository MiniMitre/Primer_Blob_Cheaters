import pyautogui
import time
import numpy as np
import random


def main():
    """Common Abbreviations in Variable Names:
        p: probability
        E: Expected / Expected Value
        S: Score / ScoreMaximizing
        C: Cost
        Flip: If a coin gets flipped in this situation
        GuessNow: If we guess the blobs at that point
        Total: Combination of Flip and GuessNow, based on which is better
        Strat: Output of which is better.

        All Data is stored in 2D numpy arrays.
        Index1: number of heads flipped up to this point
        Index2: number of tails flipped up to this point

        Whenever the game length maximizing, and the score maximizing Calculations are within the same loop,
        there will be an empty line seperating them (see array initilization).
        """

    heads, tails = 300, 180
    global Strat
    global pCheater
    
    # Base Data (Res = Result)
    pResIfCheat = np.zeros((heads, tails))
    pResIfFair = np.zeros((heads, tails))
    pCheater = np.zeros((heads, tails))
    

    # Maximizing Game Length
    EGuessNow = np.zeros((heads, tails))
    EFlip = np.zeros((heads, tails))
    ETotal = np.zeros((heads, tails))
    Strat = np.zeros((heads, tails))

    # Initialize probabilities
    pResIfCheat[0, 0] = 1
    pResIfFair[0, 0] = 1
    for i in range(1, heads):
        pResIfCheat[i, 0] = 0.75 * pResIfCheat[i - 1, 0]
        pResIfFair[i, 0] = 0.5 * pResIfFair[i - 1, 0]
    for j in range(1, tails):
        pResIfCheat[0, j] = 0.25 * pResIfCheat[0, j - 1]
        pResIfFair[0, j] = 0.5 * pResIfFair[0, j - 1]
        for i in range(1, heads):
            pResIfCheat[i, j] = 0.75 * pResIfCheat[i - 1, j] + 0.25 * pResIfCheat[i, j - 1]
            pResIfFair[i, j] = 0.5 * pResIfFair[i - 1, j] + 0.5 * pResIfFair[i, j - 1]

    for i in range(heads):
        for j in range(tails):
            pCheater[i, j] = pResIfCheat[i, j] / (pResIfCheat[i, j] + pResIfFair[i, j])
            pFair = 1 - pCheater[i, j]

            EGuessNow[i, j] = max(pCheater[i, j], pFair) * 15 + min(pCheater[i, j], pFair) * -30
            
    # The very last row and column have to be initialized with data for Flip,
    # since The Flip Arrays are filled back to front.
    for i in range(heads):
        EFlip[i, tails - 1] = -7.5
        ETotal[i, tails - 1] = EGuessNow[i, tails - 1]
        Strat[i, tails - 1] = (1 if pCheater[i, j] > 0.5 else -1)

    for j in range(tails):
        EFlip[heads - 1, j] = -7.5
        ETotal[heads - 1, j] = EGuessNow[heads - 1, j]
        Strat[heads - 1, j] = (1 if pCheater[i, j] > 0.5 else -1)

    for i in range(heads - 2, -1, -1):
        for j in range(tails - 2, -1, -1):
            pHeads = cheatTopHeads(pCheater[i, j])
            EFlip[i, j] = -1 + pHeads * ETotal[i + 1, j] + (1 - pHeads) * ETotal[i, j + 1]
            ETotal[i, j] = max(EGuessNow[i, j], EFlip[i, j])
            Strat[i, j] = (1 if pCheater[i, j] > 0.5 else -1) if EGuessNow[i, j] > EFlip[i, j] else 0
                
    print("Done.")
            

def cheatTopHeads(pCheater):
    return 0.5 + 0.25 * pCheater

def clickRandom(x1,x2,y1,y2):
    x = random.randint(x1,x2)
    y = random.randint(y1,y2)
    pyautogui.click(x,y)

def flipFiveTimes():
    pyautogui.moveTo(1138,890)
    pyautogui.click(1138,890)

def flipCoin():
    clickRandom(726,865,861,909)

def moveToFlip():
    pyautogui.moveTo(800,880)

def submitScore():
    pyautogui.moveTo(1000,925)
    clickRandom(863,1055, 907,946)

def resetGame():
    pyautogui.moveTo(1000,1025)
    clickRandom(826, 1097, 1004, 1049)

def labelCheater():
    pyautogui.moveTo(1000,1025)
    clickRandom(979,1241,1003,1054)
    resetScore()

def labelFair():
    pyautogui.moveTo(800,1025)
    clickRandom(697,921,1006,1048)
    resetScore()

def guess(cheating, count, sleepTime):
    global global_guesses
    count = count + 1
    global_guesses = global_guesses + 1
    
    if cheating:
        print("Guess" , count , "is Cheater")
        labelCheater()
    else:
        print("Guess" , count , "is Fair")
        labelFair()
        
    time.sleep(sleepTime)

    moveToFlip()
    
    return count

def resetScore():
    global global_heads
    global global_tails
    global_heads = 0
    global_tails = 0

def clickOn(img, search_region):
    pyautogui.click(pyautogui.locateCenterOnScreen(img, confidence = 0.9, region = search_region))

def find(screenshot, folderName):

    # dictionary for digits grouped by "y"
    found = dict()

    filePath = folderName + '/{}.png'

    # find all digits 
    for digit in range(10):
        
        positions = pyautogui.locateAll(filePath.format(digit), screenshot, True,confidence = 0.9)
        
        for x,y,_,_ in positions:
            if y not in found:
                found[y] = dict()
            found[y][x] = digit

    # recreate values
    result = 0
    
    for row in sorted(found):
        cols = sorted(found[row])
        value = ''.join(str(found[row][col]) for col in cols)
        result = value

    if folderName == 'Flips_Digits':
        pos = pyautogui.locateOnScreen(folderName+'/-.png', region = (1000,800,120,45))
    
        if pos != None:
            result = -1*int(result)
        
    return result

def gameOver():
    print('Game over')
    time.sleep(4)
    enterDetails()
    while pyautogui.pixel(1070,930) != (50, 50, 50):
        submitScore()
        time.sleep(20)
    
def enterDetails():
    pyautogui.moveTo(977,772)
    pyautogui.click(977,772)
    pyautogui.write("Your name here")
    pyautogui.moveTo(998,856)
    pyautogui.click(998,856)
    pyautogui.write("email@mail.com")
    

def refreshBrowser():
    pyautogui.press("F5")
    time.sleep(3)
    pyautogui.moveTo(1732,395)
    pyautogui.scroll(-5000)
    pyautogui.click(1289,815)
    pyautogui.click(742,963)
    pyautogui.moveTo(750,900)

def throwGame():
    pyautogui.click(1114,888)
    

def decideFlipOrGuess(count):
    
    global global_heads
    global global_tails
    global currentScore

    headsScoreImg = pyautogui.screenshot(region = (1042,427,88,30))
    tailsScoreImg = pyautogui.screenshot(region = (1025,467,88,30))
    flipsLeftImg = pyautogui.screenshot(region = (1000,800,120,45))
    scoreImg = pyautogui.screenshot(region = (760,800,120,40))

    headsScore = int(str(find(headsScoreImg, 'Heads_Tails_digits')))
    tailsScore = int(str(find(tailsScoreImg, 'Heads_Tails_digits')))
    flipsLeft = int(find(flipsLeftImg, 'Flips_Digits'))
    
    scoreReading = int(find(scoreImg, 'Score_Digits'))
    
    if scoreReading != 0:
        currentScore = scoreReading
        
    #headsScore cannot go down - flip again and re-read score
    if global_heads > headsScore:
        print("Error detecting heads score")
        print("Previous score =",global_heads, " current score =",headsScore)
        flipCoin()
        return count

    if global_tails > tailsScore:
        print("Error detecting tails score")
        print("Previous score =",global_tails, " current score =",tailsScore)
        flipCoin()
        return count

    global_heads = headsScore
    global_tails = tailsScore

    probCheater =  pCheater[headsScore][tailsScore]

    if flipsLeft > 30:
        sleepTimer = 2.5
    else:
        sleepTimer = 4

    #Game over
    if pyautogui.pixel(913,702) == (245, 245, 245):

        pyautogui.PAUSE = 1

        if currentScore > 4000:
            #Submit Score
            gameOver()
        
        count = 0
        
        pyautogui.PAUSE = 2
        refreshBrowser()

        pyautogui.PAUSE = pause_const

        return count

    #Game is lost
    if flipsLeft <= 0:
        #Wait for final death screen to appear
        time.sleep(5)
        
    #No more flips available
    if flipsLeft == 0 and pyautogui.pixel(800,860) <= (200, 200, 200):
        print('Heads',headsScore,' Tails', tailsScore, ' Flips', flipsLeft, ' Score', currentScore)
        print("No Flips Left, probability of cheater is", probCheater)
        
        if probCheater > 0.5:
            count = guess(True, count, sleepTimer)
        else:
            count = guess(False, count, sleepTimer)

        #Wait for final death screen to appear in case we lose
        time.sleep(5)

        return count

    #Enter 'do not lose' mode
    if flipsLeft < 40 and currentScore > 1000:
        print('Heads',headsScore,' Tails', tailsScore, ' Flips', flipsLeft, ' Score', currentScore)
        print("Do not lose enabled, probability of cheater is",probCheater)

        #Try to prevent bugging the game out with excessive clicking
        pyautogui.PAUSE = 1
        
        if probCheater > 0.85:
            count = guess(True, count, sleepTimer)
        elif probCheater < 0.15 :
            count = guess(False, count, sleepTimer)
        else:
            flipCoin()

        return count

    max = 4536
    #Incase we mis-read the score
    if currentScore >= max and currentScore <= max + 1:
        
        sleepTimer = 5
        if flipsLeft > 28:
            throwGame()
            return count
        else:
            print('Count =', count, 'Global_Guesses = ', global_guesses, 'Heads',headsScore,' Tails', tailsScore, ' Flips', flipsLeft, ' Score', currentScore) 
            currentScore = 1
        
        #Guess WRONG
        if probCheater < 0.5:
            count = guess(True, count, sleepTimer)
        else:
            count = guess(False, count, sleepTimer)

        pyautogui.PAUSE = 1
        gameOver()

        count = 0
        
        pyautogui.PAUSE = 2
        refreshBrowser()

        pyautogui.PAUSE = pause_const

        return count

    #Normal operation
    pyautogui.PAUSE = pause_const
    if Strat[headsScore][tailsScore] == 1:
        print('Heads',headsScore,' Tails', tailsScore, ' Flips', flipsLeft, ' Score', currentScore)
        count = guess(True, count, sleepTimer)
                
    elif Strat[headsScore][tailsScore] == -1:
        print('Heads',headsScore,' Tails', tailsScore, ' Flips', flipsLeft, ' Score', currentScore)
        count = guess(False, count, sleepTimer)
                
    else:
        flipCoin()

    return count  

global_heads = 0
global_tails = 0
global_guesses = 0
currentScore = 0

pause_const = 0.15
pyautogui.PAUSE = pause_const
               
main()
count = 0

while True:
    
    count = decideFlipOrGuess(count)


