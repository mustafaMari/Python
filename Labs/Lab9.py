import argparse
import datetime
import os
import smtplib
import sys

import bs4
import requests


def send_email():
    key = 'secret'
    password = os.getenv(key)
    login = 'login'
    username = os.getenv(login)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(username, password)
    message = f'Subject: Hello!! Today is {datetime.date.today()}' \
              f' and the time is {datetime.datetime.today().time()}\nHello\nJust testing the project'
    from_email = '252407@student.pwr.edu.pl'
    to = '252407@student.pwr.edu.pl'
    result = server.sendmail(from_email, to, message)
    if len(result) != 0:
        print(f"those user/s did not receive your email, double check their emails. {result}")
    server.quit()


def cats_facts():
    fetch_facts = requests.get('https://cat-fact.herokuapp.com/facts')
    original_facts = []
    for fact in fetch_facts.json():
        original_facts.append(fact['text'])
    # print(original_facts)
    return original_facts


def limitedNumber(howMany):
    if howMany < 1 or howMany > len(facts):
        print("The requested number is invalid")
        sys.exit()
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
                    return next_link

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
    if args.mail == "My message to the teacher":
        send_email()
    if args.cat_facts is not None:
        limitedNumber(int(args.cat_facts))
    if args.teachers is not None:
        printResearchers(args.teachers)
