import pyautogui

def take_screenshot(name="screenshot.png", region=(0,70, 500, 800)):
    myScreenshot = pyautogui.screenshot(region=region)
    myScreenshot.save(r''+name)
    return name

take_screenshot()
