import json

http_requests = ("GET", "HEAD", "POST", "PUT", "DELETE",
                 "TRACE", "OPTIONS", "CONNECT", "PATCH")
logging_levels = ("DEBUG", "INFO", "ERROR", "WARNING", "ERROR", "CRITICAL")
second_filters = ("Request_Length", "HTTP_CODE", "DATE")


def checkIfHTTPValid(http_requestC):
    return http_requestC in http_requests


def checkIfLevelValid(level):
    return level in logging_levels


def checkForASecondFilter(second):
    return second in second_filters


def configuration():
    log_file_name = input("The name of the log file is: ")
    check = False
    http_request = ""
    while not check:
        print(f"the available https requests are: {http_requests}")
        http_request = input("The http request is: ")
        check = checkIfHTTPValid(http_request)
        print(check)
        if check is False:
            print("choose a valid http request")
            continue
    check = False
    logging_level = ""
    while not check:
        print(f"the available logging levels are: {logging_levels}")
        logging_level = input("Choose the logging level: ")
        check = checkIfLevelValid(logging_level)
        if check is False:
            print("choose a valid logging level")
            continue
    number_lines = int(input("The number of lines: "))
    check = False
    second_filter = ""
    while not check:
        print(f"the available second filter are {second_filters}")
        second_filter = input("Choose a second filter: ")
        check = checkForASecondFilter(second_filter)
        if check is False:
            print("choose a valid second filter")
            continue
    Dict = {
        "log_file": log_file_name,
        "http_request": http_request,
        "logging level": logging_level,
        "number_lines": number_lines,
        "second_filter": second_filter
    }
    print(Dict)
    json.dumps(Dict)

