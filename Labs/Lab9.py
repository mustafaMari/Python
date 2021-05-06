import argparse
import datetime
import os
import smtplib
import sys
from email.mime.text import MIMEText

import bs4
import requests


# def read_config(file_name="email_configuration_file"):
#     try:
#         values = {}
#         with open(file_name) as config_file:
#             for line in config_file.readlines():
#                 content = line.strip('\n').split('=')
#                 variable_name = content[0]
#                 variable_value = content[1]
#                 values[variable_name] = variable_value
#             return values
#     except FileNotFoundError:
#         print("The file does not exist")


def send_email(subject):
    key = 'secret'
    password = os.getenv(key)
    msg = MIMEText(f"The current timestamp is {str(datetime.datetime.now())}")
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login('252407@student.pwr.edu.pl', password)
    server.sendmail(
        '252407@student.pwr.edu.pl',
        '252407@student.pwr.edu.pl', msg.as_string()
    )
    server.quit()


def cats_facts():
    fetch_facts = requests.get('https://cat-fact.herokuapp.com/facts')
    original_facts = []
    for fact in fetch_facts.json():
        original_facts.append(fact['text'])
    # print(original_facts)
    return original_facts


def limitedNumber(howMany):
    for fact in facts:
        print(fact)
        howMany -= 1
        if howMany == 0:
            break


researchers = {}


def list_researchers(letter, link='https://wiz.pwr.edu.pl/pracownicy?letter='):
    page = requests.get(f"{link}{letter}")
    page.raise_for_status()
    content = bs4.BeautifulSoup(page.text, 'html.parser')
    for element in content.select('div .news-box'):
        descriptions = element.select('a')
        email = element.find('p')
        name = descriptions[0].get('title')
        email = str(email).strip('<p>Email: ').strip('</')
        researchers[name] = email

    def checkForAnewPage():
        for pa in content.select('div .pagination'):
            dis = pa.select('a')
            for x in dis:
                if x.get('title') == 'Następna strona':
                    next_link = f"https://wiz.pwr.edu.pl{x.get('href')[:-1]}"
                    return next_link, True

    if checkForAnewPage() is not None:
        list_researchers(letter, checkForAnewPage()[0])


def printResearchers(letter):
    list_researchers(letter)
    if len(researchers) == 0:
        print(f"There are no researchers with the initial {letter}")
        sys.exit(0)
    print(f"The list of researchers with the initial {letter}:")
    print("{:<50} {:<1}".format('Name', 'Email'))
    for researcher in researchers:
        x = researcher
        y = researchers[researcher]
        print("{:<50} {:<1}".format(x, y))


if __name__ == '__main__':
    facts = cats_facts()
    parser = argparse.ArgumentParser(description="The idea of the application is to practice internet access")
    parser.add_argument('--mail', help="Sending an email to the teacher")
    parser.add_argument('--cat-facts', help="Print a given number of facts about cats")
    parser.add_argument('--teachers', help="To list the name and emails of the researchers with the provided initial")
    args = parser.parse_args()
    if args.mail is not None:
        send_email(args.mail)
    if args.cat_facts is not None:
        limitedNumber(int(args.cat_facts))
    if args.teachers is not None:
        printResearchers(args.teachers)
