from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
import json
import time
import os
import sys
import base64
import getopt

def reportpdf(args: List[str]) -> None:

# Report TX Run
    if args[1].lower() == "1":
        reporturl = "http://127.0.0.1:8080/AMS/forward/view.action?url=report/ratingReport/txrunReport"
        reportfilename = "txrunReport.pdf"

# TX Run Remaining (scheduled)
    if args[1].lower() == "2":
        reporturl = "http://127.0.0.1:8080/AMS/forward/view.action?url=report/ratingReport/schedilingReport"
        reportfilename = "schedilingReport.pdf"

# TX Run Remaining (not yet scheduled)
    if args[1].lower() == "3":
        reporturl = "http://127.0.0.1:8080/AMS/forward/view.action?url=report/ratingReport/txrunRemainingReport"
        reportfilename = "txrunRemainingReport.pdf"

# Acquisation Report
    if args[1].lower() == "4":
        reporturl = "http://127.0.0.1:8080/AMS/forward/view.action?url=report/adminReport/acquisitionReport"
        reportfilename = "acquisitionReport.pdf"
        year = args[2]
        month = args[3]

# Create a timestamp folder under report folder
    savefolder = args[0]

# Selenium settings
    browser_options = webdriver.ChromeOptions()
    settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "landscape": True
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    browser_options.add_experimental_option('prefs', prefs)
#    browser_options.add_argument('--kiosk-printing')
    browser_options.add_argument('lang-zh_CN.UTF-8')
    browser_options.add_argument('-lang=zh')
#    browser_options.add_argument("--headless")

# Selenium print preference
    prefs = {
        'printing.print_preview_sticky_settings.appState' : json.dumps(settings),
        "savefile.default_directory" : savefolder,
        "displayHeaderFooter" : True,
        "mediaSize": {
            "height_microns" : 297000,
            "name" : "ISO_A4",
            "width_microns" : 210000,
            "custom_display_name" : "A4"
        },
        "landscape": True,
        "footerTemplate": "<div style='font-size: 8px; padding-top: 5px; text-align: center; width: 100%;'><span>Page </span><span class='pageNumber''></span> of <span class='totalPages'></span></div>",
    }
    browser_options.add_experimental_option('prefs', prefs)

# Create virtual browser
    webbrowser = webdriver.Chrome(options=browser_options)
    webbrowser.get("http://127.0.0.1:8080/AMS")
    username = webbrowser.find_element(By.ID,"username")
    username.send_keys("admin")
    password = webbrowser.find_element(By.ID,"password")
    password.send_keys("123456")
    button = webbrowser.find_element(By.ID,"button-login")
    button.click()
    webbrowser.get(reporturl)
    if args[1] == "4":
        yearbox = webbrowser.find_element(By.ID,"year")
        yearbox.send_keys(year)
        monthbox = webbrowser.find_element(By.ID,"month")
        monthbox.send_keys(month)
        button = webbrowser.find_element(By.ID,"button-search")
        button.click()

# Add timer for report webpage loading
    time.sleep(5)

# Set virtual browser printing preview timeout
    webbrowser.set_script_timeout(300)
    prefs_check = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
# Print the page as PDF
    #webbrowser.execute_script("window.print();")
    pdf_data = webbrowser.execute_cdp_cmd("Page.printToPDF", prefs)

    with open(savefolder + reportfilename, 'wb') as file:
        file.write(base64.b64decode(pdf_data['data']))

# Close virtual browser
    webbrowser.close

    return reportfilename

if __name__ == "__main__":
    reportpdf(sys.argv[1:])


