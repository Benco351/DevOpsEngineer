import logging
from threading import Timer
from datetime import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import autosms
import testere
logging.basicConfig(format='%(asctime)s:$(levelname)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
IDbuttonlist = dict()
TempIDbuttonlist = dict()
Phonenumberslist = list()
options = webdriver.ChromeOptions()
options.binary_location = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
# options.add_argument('--headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(executable_path=r'C:/Users/97254/Desktop/chromedriver.exe', options=options)
url = "https://app.site123.com/manager/login/login.php?l=he"
driver.get(url)

# -----testlist = ["05448296154"]


# Gets into the main Iframe
def changeIframetoManagement():
    wait1 = WebDriverWait(driver, 10)
    wait1.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "moduleManagement")))


# Gets into Orders Iframe
def changeIframetoOrders():
    wait2 = WebDriverWait(driver, 10)
    wait2.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "orderInfo")))


# reach to today orders
def RetrieveDate():
    wait3 = WebDriverWait(driver, 10)
    element = wait3.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reportrange:last-of-type")))
    element.click()
    second_li_element = wait3.until(EC.visibility_of_element_located((By.XPATH, "(//li[@data-range-key])[2]")))
    second_li_element.click()


def SecondOperation():
    changeIframetoManagement()
    OrderStatus = Select(driver.find_element_by_class_name("status-filter"))
    OrderStatus.select_by_value("2")
    # choose the today date in the program
    RetrieveDate()
    # running on all the table and grab the info


def FirstOperation():
    username = testere.ferent.decrypt(testere.encUsername).decode()
    password = testere.ferent.decrypt(testere.encPassword).decode()
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_css_selector(
        "button, html input[type=\"button\"], input[type=\"reset\"], input[type=\"submit\"]").click()
    # Entering menu page
    driver.get("https://app.site123.com/versions/2/wizard/modules/mDash.php?wu=795480&t=112&e=1")
    SecondOperation()


def Testtiming(IDbuttonsId, last_time_of_readd):
    UpdatedUsers = dict()
    for counter in range(len(IDbuttonsId)):
        if list(IDbuttonsId.items())[counter][1][11:] == last_time_of_readd:
            UpdatedUsers[list(IDbuttonsId.items())[counter][0][0:]] = list(IDbuttonsId.items())[counter][1][0:]
    return UpdatedUsers


def CheckSMS(nowtime):
    # -----------------------------------------------------------------------------------------------------------
    # every day at 12 PM check to who sent another sms
    Nextdayschedule = nowtime.today().replace(day=now.day, hour=12, minute=0, second=0, microsecond=0) + timedelta(
        days=1)
    delta_t = Nextdayschedule - nowtime.today()
    secs = delta_t.total_seconds()
    schedule_command = Timer(secs, autosms.CHECKfor28DAYSSMS)
    schedule_command.start()
    # -----------------------------------------------------------------------------------------------------------


FirstOperation()
now1 = datetime.now()
last_time_of_read = now1.strftime("%H:%M")
while True:
    now = datetime.now()
    timestamp = now.strftime("%H:%M")
    logging.debug(CheckSMS(now))
    print(last_time_of_read)
    print(timestamp)
    # Get all the rows and columns of the order list
    rows = driver.find_elements_by_xpath("//html/body/div[1]/div/div/div[3]/div[2]/div[1]/table/tbody/tr")
    x = len(rows)

    # fill IDBUTTON with date and ID order
    for row in range(x):
        IDbuttonlist[rows[row].text[0:13]] = driver.find_element_by_xpath("//html/body/div[1]/div/div/div[3]/div["
                                                                          "2]/div[ "
                                                                          "1]/table/tbody/tr[" + str(row + 1) + "]/td["
                                                                          "4]").text
    print(IDbuttonlist)
    # Filter the exist list with the time
    IDbuttonlist = Testtiming(IDbuttonlist, last_time_of_read)
    # -----print(IDbuttonlist)
    # IF there is a new order within the same time
    if bool(IDbuttonlist):
        wait4 = WebDriverWait(driver, 10)
        logging.info("New Order/s" + str(IDbuttonlist) + "preparing the SMS : ")
        # Taking all the phone number into a list
        for i in range(len(IDbuttonlist)):
            for x in range(len(rows)):
                if list(IDbuttonlist.items())[i][0] == driver.find_element_by_xpath(
                        "//html/body/div[1]/div/div/div[3]/div[2]/div["
                        "1]/table/tbody/tr[" + str(x + 1) +
                        "]/td[7]/div["
                        "1]/a").get_attribute(
                        "data""-message-id"):
                    driver.find_element_by_xpath(
                        "//html/body/div[1]/div/div/div[3]/div[2]/div[1]/table/tbody/tr[" + str(
                            x + 1) + "]/td[7]/div[1]/a").click()
                    changeIframetoOrders()
                    Phonenumberslist.append(
                        driver.find_element_by_xpath("//html/body/div[1]/div/div/div[3]/table/tbody/tr[2]/td[2]").text)
                    driver.switch_to.default_content()
                    changeIframetoManagement()
                    wait4.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "div.modal-dialog button.bootbox-close-button"))).click()
        logging.warning('Sending the SMS')
        autosms.SendCompleteSMS(Phonenumberslist, str(now.date().today()))
        logging.info('SMS sent and submitted')
        Phonenumberslist.clear()
        IDbuttonlist.clear()
        last_time_of_read = timestamp
        logging.warning('Waiting minute to check again for orders')
        sleep(20)
        driver.refresh()
        driver.switch_to.default_content()
        SecondOperation()

    else:
        logging.warning('No new order wait a minute')
        last_time_of_read = timestamp
        driver.switch_to.default_content()
        sleep(20)
        driver.refresh()
        SecondOperation()

# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# logging.warning('Numbers retrieved')


# driver.find_element_by_css_selector("body > div.container.theme-showcase > div > div > div.row.ajaxed-area >
# div.col-xs-12.ajaxed-inner > div:nth-child(1) > table > tbody > tr:nth-child(1) > td.o-t-manage-buttons.noLongText
# > div:nth-child(1) > a").click()


# driver.refresh()
