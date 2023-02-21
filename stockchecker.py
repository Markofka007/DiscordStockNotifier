#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from termcolor import colored
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# mail client stuff
sender_email = ''  # SENDER EMAIL
rec_email = ''  # RECEIVER EMAIL
password = ''  # SENDER EMAIL PASSWORD
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(sender_email, password)


def send_email(product_name, product_url):
    mail_subject = f'{product_name}'
    mail_body = f'{product_url}'
    msg = f'Subject: {mail_subject}\n\n{mail_body}'
    server.sendmail(sender_email, rec_email, msg)


# google chrome driver (user agent)
PATH = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# get URLs
urls = []
done = False
print("Enter URL and press enter to submit. Submit blank response when done.")
while not done:
    url_input = input("Enter URL: ")
    if url_input == "":
        break
    else:
        urls.append(url_input)

print(colored(f'Now Testing [{len(urls)}] Sites', 'yellow'))

while True:
        for url in urls:
            driver.get(url)
            time.sleep(1)
            if "Sold Out" in driver.page_source:
                print(f"{colored(f'{datetime.now()}', 'white')}: {url} {colored('CURRENTLY SOLD OUT', 'red')}")
            else:
                print(f"{colored(f'{datetime.now()}', 'white')}: {url} {colored('BACK IN STOCK', 'green')}")
                send_email('ITEM IN STOCK!!!', url)