from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import re
import time

driver = webdriver.Chrome()

# Open Website
driver.get("https://arithmetic.zetamac.com/")

# Start the Zetamac 
startButton = driver.find_element(By.XPATH, '//input[@value="Start"]')
startButton.click()

while True:
    try:
        # Check if time is up to exit out of the loop
        try:
            secondsLeftSpan = driver.find_element(By.XPATH, '//span[@class="left" and contains(text(), "Seconds left: 0")]')
            print("Game ended")
            break
        except:
            pass  
        
        # Get the math problem 
        problemSpan = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'problem')))
        problemText = problemSpan.text
        print(f"Problem text: '{problemText}'")
        
        # Find the mathematical symbol
        mathSymbols = {'+', '–', '÷','×'}
        symbolIndices = [index for index, char in enumerate(problemText) if char in mathSymbols]

        # Check if any symbols were found
        if symbolIndices:
            sign_index = symbolIndices[0]
            sign = problemText[sign_index] 

            # Calculation
            if sign == '–':
                newProblemText = problemText.replace('–', '-')
                answer = eval(newProblemText) 
            elif sign == '+':
                answer = eval(problemText)
            elif sign == '×':
                newProblemText = problemText.replace('×', '*')
                answer = eval(newProblemText)
            elif sign == '÷':
                newProblemText = problemText.replace('÷', '/')
                answer = eval(newProblemText)
            
            print(f"Calculated answer: {answer}")
            
            # Ensure answer is an integer if it's a whole number
            if isinstance(answer, float) and answer.is_integer():
                answer = int(answer)
            
            print(f"Final answer to enter: {answer}")
            
            # Enter the answer
            answerInput = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'answer')))
            answerInput.send_keys(str(answer))  
            answerInput.send_keys(Keys.RETURN)
        else:
            print(f"No math symbols found in problem: {problemText}")
            continue
        
        # Wait for the new problem to load
        try:
            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return jQuery.active == 0'))
            time.sleep(0.5)
        except Exception as e:
            print(f"Error waiting for new problem: {e}")
            time.sleep(1)
            
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(2)
        continue 
    
# Wait 2 minutes before closing the browser
time.sleep(120)
driver.quit()
