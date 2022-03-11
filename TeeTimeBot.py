import pyautogui
import time
from datetime import date, datetime


#Important Data
desired_date = '03/19/2022'
trigger_time = '06:00:00'
desired_courses = [True, True, True, False, False, False, False, True, False, False, False, True, False, True, False, False, False] #True means check box for course on home page

def wait_until_time(trigger_time, sec_sleep=0.05):
    '''
    Does nothing until time is reached.
    
    Parameters:
        trigger_time (str): timestamp in %H:%M:%S format
        sec_sleep (float): time between checks in seconds   
    '''
    while datetime.now().strftime('%H') != 5:
        time.sleep(60*30)

    while datetime.now().strftime('%M') < 57:
        time.sleep(60*2)

    while datetime.now().strftime('%H:%M:%S') < trigger_time:
        time.sleep(sec_sleep)

def goSnipe(trigger_time, desired_date, desired_courses):
    '''
    Executes Sniping Logic.
    
    Parameters:
        trigger_time (str): timestamp in %H:%M:%S format
        desired_date (str): date of tee time of form DD/MM/YYYY  
        desired_courses (array): boolean array depicting which courses to select
    '''

    wait_until_time(trigger_time)


    pyautogui.click(86, 97) #Click refresh button
    time.sleep(1.5)

    ### SETUP DATE
    date_box_coords = locateButton('calendar.png')
    pyautogui.click(date_box_coords[0]-100, date_box_coords[1]-2) #Click date field
    for i in range(0,12): #Bad but only way to input desired date
        pyautogui.press('left')
        pyautogui.press('delete')
    pyautogui.write(desired_date)
    pyautogui.click(date_box_coords[0]+300, date_box_coords[1]-25) #Exit date field

    ### SCROLL
    with pyautogui.hold('space'): #this process scrolls down on payment page
        pyautogui.press('down')
    time.sleep(.5) 

    ### CHECK LOCATIONS
    courses = pyautogui.locateAllOnScreen('buttons/checkbox.png', confidence = .9) #Create generator of all checkbox fields to click
    count = 0
    for course in courses: #Click select checkboxes
        if desired_courses[count]:
            pyautogui.click(course.left/2 + course.width/2 - 5, course.top/2 + course.height/2 - 5)
        count += 1
    pyautogui.click(locateButton('search.png')) #Click search

    checkLogin() #Checks if page prompts a login

    ### START SNIPING
    time.sleep(1.1)
    pyautogui.click(locateButton('view.png')) #Click first available tee time
    time.sleep(.7)
    pyautogui.click(locateButton('continue.png')) #Click continue on booking tee time

    checkLogin() #Checks if page prompts a login

    time.sleep(1)

    with pyautogui.hold('space'): #this process scrolls down on payment page
        pyautogui.press('down')

    pyautogui.click(locateButton('continue.png')) #click continue
    pyautogui.click(locateButton('finish_reservation.png')) #click finish reservation

def locateButton(path):
    '''
    Locates putton coordinates.
    
    Parameters:
        path (str): file name of button image
    '''
    position = pyautogui.locateCenterOnScreen('buttons/' + path, confidence = .9)
    return (position.x/2, position.y/2)

def checkLogin():
    '''
    Checks for login page prompt.
    '''
    try:
        pyautogui.click(locateButton('login.png'))
        time.sleep(.7)
    except:
        pass

    
time.sleep(1)
goSnipe(trigger_time, desired_date, desired_courses)