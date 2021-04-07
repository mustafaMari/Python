import json

http_requests_methods = ("GET", "HEAD", "POST", "PUT", "DELETE",
                         "TRACE", "OPTIONS", "CONNECT", "PATCH")
logging_levels = ("DEBUG", "INFO", "ERROR", "WARNING", "ERROR", "CRITICAL")


def configuration():
    log_file_name = input("The name of the log file is: ")
    check = False
    http_request_method = ""
    while not check:
        print(f"the available https request methods are: {http_requests_methods}")
        http_request_method = input("The http request is: ")
        check = http_request_method.upper() in http_requests_methods
        if check is False:
            print("choose a valid http request method")
            continue
    check = False
    logging_level = ""
    while not check:
        print(f"the available logging levels are: {logging_levels}")
        logging_level = input("Choose the logging level: ")
        check = logging_level.upper() in logging_levels
        if check is False:
            print("choose a valid logging level")
            continue
    number_lines = int(input("The number of lines: "))
    check = False
    number_of_ips_has_request_method = ""
    while not check:
        print(f"the available https requests methods are: {http_requests_methods}")
        number_of_ips_has_request_method = input("choose a method: ")
        check = number_of_ips_has_request_method.upper() in http_requests_methods
        if check is False:
            print("choose a valid http method")
            continue
    Dict = {
        "log_file": log_file_name,
        "http_request_method": http_request_method.upper(),
        "logging level": logging_level.upper(),
        "number_lines": number_lines,
        "number_of_ips_has_request_method": number_of_ips_has_request_method.upper()
    }
    print(Dict)
    file_name = 'file.txt'
    with open(file_name, 'w') as fi:
        json.dump(Dict, fi)


if __name__ == "__main__":
    configuration()
