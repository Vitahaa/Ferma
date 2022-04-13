import time
import pyautogui
import random
import pytweening

# chrome zoom 80%
number_of_slots = 7 # per working area
number_of_working_areas = 3
flipping_mode = True # True or False
flipping_after_loops_count = 1 # after 2 full loops bot will sell all sunflowers and buy seeds which were spent since previous flip
number_of_tabs = 1 # minimum 1
vegetable = 'sunflower' # 'sunflower' / 'potato' / 'pumpkin' / 'carrot' / 'cabbage' / 'beetroot'

def generateClickDelay():
    return random.uniform(0.06,0.11)

def generateCycleDelay():
    return random.uniform(0.06,0.11)

def generateLoopDelay():
    return random.uniform(15,20)

def generateMouseMovementSpeedShortDistance():
    return random.uniform(0.1,0.5)
def generateMouseMovementSpeedMediumDistance():
    return random.uniform(0.5,0.1)
def generateMouseMovementSpeedLongDistance():
    return random.uniform(0.1,2)

def generateMousePositionAdjustForClickX():
    return random.randint(-5,5)

def generateMousePositionAdjustForClickY():
    return random.randint(-1,3)

def generateMouseClearViewShift():
    return random.randint(100,200)

def generateCurveDegreeShortDistance():
    return random.randint(1,2)
def generateCurveDegreeMediumDistance():
    return random.randint(40,60)
def generateCurveDegreeLongDistance():
    return random.randint(100,200)


#------------------------------------------#
#                                          #
#     Not linear mouse movement module     #
#                                          #
#------------------------------------------#

def getPointOnCurve(x1, y1, x2, y2, n, tween=None, offset=0):
    """Returns the (x, y) tuple of the point that has progressed a proportion
    n along the curve defined by the two x, y coordinates.
    If the movement length for X is great than Y, then Y offset else X
    """
    # for compatibility Backward
    if getPointOnCurve.tween and getPointOnCurve.offset:  # need DEL
        tween = getPointOnCurve.tween                     # need DEL
        offset = getPointOnCurve.offset                   # need DEL

    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    if tween and offset:
        offset = (n - tween(n)) * offset
        if abs(x2 - x1) > abs(y2 - y1):
            y += offset
        else:
            x += offset
    return (x, y)

getPointOnCurve.tween = None
getPointOnCurve.offset = 0

def set_curve(func, tween=None, offset=0):
   func.tween = tween
   func.offset = offset

pyautogui.getPointOnLine = getPointOnCurve  #   Replacement
   
#------------------------------------------#
#                                          #
#              Bot functions               #
#                                          #
#------------------------------------------# 
   
def select_tabs():
    tab_locations = []
    i = 0
    while i < number_of_tabs:
        input(f'Hower mouse on browser tab {i+1} and press ENTER: ')
        tab_location_x, tab_location_y = pyautogui.position()
        tab_locations.append([tab_location_x, tab_location_y])    
        i += 1 
        
    return tab_locations

def selectWorkingArea():
    
    input('Hower mouse to upper left corner of working area and press ENTER: ')
    first_working_x, first_working_y = pyautogui.position()
    input('Hower mouse to bottom right corner of working area and press ENTER: ')
    second_working_x, second_working_y = pyautogui.position()
    
    return first_working_x, first_working_y, second_working_x, second_working_y

def harvestSunflowers(first_working_x, first_working_y, second_working_x, second_working_y):
    
    region = (first_working_x, first_working_y, second_working_x, second_working_y)
    vegetable_button = f'img/{vegetable}/02.jpg'
    
    button_location = pyautogui.locateOnScreen(vegetable_button, region = region, confidence=0.8)
    if button_location is not None:
        button_point = pyautogui.center(button_location)
        button_x, button_y = button_point
        
        set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeMediumDistance())
        pyautogui.moveTo(button_x + generateMousePositionAdjustForClickX(), button_y + generateMousePositionAdjustForClickY(), generateMouseMovementSpeedMediumDistance())
        pyautogui.click()
        time.sleep(generateClickDelay())
        set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeShortDistance())
        pyautogui.moveTo(button_x + generateMousePositionAdjustForClickX(), button_y + generateMousePositionAdjustForClickY(), generateMouseMovementSpeedShortDistance())
        pyautogui.click()
        print('Sunflower harvested')
        return button_x, button_y
    
    else:
        print('No sunflowers found')
        return None, None

def checkReward():
    reward_window = 'img/05.jpg'
    reward_button = 'img/06.jpg'
    close_reward_window_button = 'img/07.jpg'

    print('Checking rewards')
    try:
        window_location = pyautogui.locateOnScreen(reward_window, confidence=0.8)
        if window_location is not None:
            button_1_location = pyautogui.locateOnScreen(reward_button, confidence=0.8)
            
            if button_1_location is not None:
                button_point = pyautogui.center(button_1_location)
                button_x, button_y = button_point
                set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeLongDistance())
                pyautogui.moveTo(button_x + generateMousePositionAdjustForClickX(), button_y - generateMousePositionAdjustForClickY(), generateMouseMovementSpeedLongDistance())
                pyautogui.click()
            
            time.sleep(generateClickDelay())
            
            button_2_location = pyautogui.locateOnScreen(close_reward_window_button, confidence=0.8)
            button_point = pyautogui.center(button_2_location)
            button_x, button_y = button_point
            set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeMediumDistance())
            pyautogui.moveTo(button_x + generateMousePositionAdjustForClickX(), button_y + generateMousePositionAdjustForClickY(), generateMouseMovementSpeedMediumDistance())
            pyautogui.click()
            print('Rewards claimed')
            return True

        else:
            print('No any rewards')
            return False
    except:
        print('Error while checking rewards')
    
def harvestAndClaimRewardAndPlant(first_working_x, first_working_y, second_working_x, second_working_y):
    button_x, button_y = harvestSunflowers(first_working_x, first_working_y, second_working_x, second_working_y)
    time.sleep(generateClickDelay())
    
    is_claimed = checkReward()
    time.sleep(generateClickDelay())
    
    if is_claimed:
        if button_x != None:
            set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeLongDistance())
            pyautogui.moveTo(button_x + generateMousePositionAdjustForClickX(), button_y + generateMousePositionAdjustForClickY(), generateMouseMovementSpeedLongDistance())
            pyautogui.click()
            time.sleep(generateClickDelay())

def flipSunflowers():
    
    def locateAndClickButton(img, distance):
        try:
            if distance == 'short':
                curve_degree = generateMouseMovementSpeedShortDistance()
                mouse_movement_speed = generateMouseMovementSpeedShortDistance()
            elif distance == 'medium':
                curve_degree = generateCurveDegreeMediumDistance()
                mouse_movement_speed = generateMouseMovementSpeedMediumDistance()
            elif distance == 'long':
                curve_degree = generateCurveDegreeLongDistance()
                mouse_movement_speed = generateMouseMovementSpeedLongDistance()
            
            button_location = pyautogui.locateOnScreen(img, confidence=0.8)
            button_point = pyautogui.center(button_location)
            button_x, button_y = button_point
            set_curve(getPointOnCurve, pytweening.easeInOutCubic, curve_degree)
            pyautogui.moveTo(button_x + generateMousePositionAdjustForClickX(), button_y - generateMousePositionAdjustForClickY(), mouse_movement_speed)
            pyautogui.click()
            return True
        except:
            return False
        
    print('Entering shop')
    enter_shop_button = 'img/shop/01.jpg'
    result = locateAndClickButton(enter_shop_button, 'long')
    if result == False:
        return
    time.sleep(generateClickDelay())
    
    print('Selling stuff')
    sell_section_button = 'img/shop/02.jpg'
    result = locateAndClickButton(sell_section_button, 'medium')
    time.sleep(generateClickDelay())
    
    vegetable_select_button = f'img/{vegetable}/shop/02.1.jpg'
    result = locateAndClickButton(vegetable_select_button, 'medium')
    time.sleep(generateClickDelay())

    sell_button = 'img/shop/03.jpg'
    sell_confirm_button = 'img/shop/04.jpg'
    result = locateAndClickButton(sell_button, 'medium')
    time.sleep(generateClickDelay())
    result = locateAndClickButton(sell_confirm_button, 'medium')
    time.sleep(generateClickDelay())
    print('Stuf sold')
        
    print('Buying stuff')
    buy_section_button = 'img/shop/05.jpg'
    result = locateAndClickButton(buy_section_button, 'medium')
    time.sleep(generateClickDelay())
    
    seed_button = f'img/{vegetable}/shop/06.jpg'
    result = locateAndClickButton(seed_button, 'medium')
    time.sleep(generateClickDelay())
    
    buy_button = 'img/shop/07.jpg'
    i = 0
    while i < number_of_slots * number_of_working_areas * flipping_after_loops_count:
        result = locateAndClickButton(buy_button, 'short')
        if result == False:
            break
        i += 1
    print('Stuff bought')

    print('Exiting shop')
    exit_button = 'img/shop/08.jpg'
    result = locateAndClickButton(exit_button, 'medium')
    time.sleep(generateClickDelay())
    
    print('Flipped stuff')

def main():
    
    tab_locations = select_tabs()
    
    working_areas = []
    while True:
        try:
            j = 0
            while j < number_of_working_areas:
                first_working_x, first_working_y, second_working_x, second_working_y = selectWorkingArea()
                working_areas.append([first_working_x, first_working_y, second_working_x, second_working_y])
                j += 1
            break
        except:
            print('Wrong entry, try again')
            continue
    
    i = 0
    j = 0
    while True:
        for tab in tab_locations:
            set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeLongDistance())
            pyautogui.moveTo(tab[0], tab[1], generateMouseMovementSpeedLongDistance())
            pyautogui.click()
            
            for area in working_areas:
                while i < number_of_slots:
                    
                    harvestAndClaimRewardAndPlant(area[0], area[1], area[2], area[3])
                    print('Cycle completed')
                    
                    delay = generateCycleDelay()
                    print(f'Sleeping {delay} seconds')
                    time.sleep(delay)
                    
                    print(f'Cycle {i+1} completed')
                    i += 1
                    
                i = 0

            try:
                button_x, button_y = pyautogui.position()
                set_curve(getPointOnCurve, pytweening.easeInOutCubic, generateCurveDegreeLongDistance())
                pyautogui.moveTo(button_x + generateMouseClearViewShift(), button_y + generateMouseClearViewShift(), generateMouseMovementSpeedLongDistance())
            except:
                pass
            print('Loop completed')

            j += 1
            
            if j >= flipping_after_loops_count and flipping_mode == True:
                flipSunflowers()
                j = 0
            
        delay = generateLoopDelay()
        print(f'Sleeping {delay} seconds')
        time.sleep(delay)

main()

