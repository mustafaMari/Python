import json
import logging
import random
import sys
from itertools import chain

logger = logging.getLogger("Lab 4")
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_streamer = logging.StreamHandler()
file_streamer.setFormatter(formatter)
logger.addHandler(file_streamer)


def read_log():
    Dict = {}
    f_name = 'file.json'
    parameters = ("log_file", "http_request_method", "logging level", "number_lines", "number_of_ips_has_request_method")
    try:
        with open(f_name) as f:
            try:
                data = json.load(f)
                method_http = data["http_request_method"]
                lines_number_from_file = data["number_lines"]
                number_request = data["number_of_ips_has_request_method"]
                print(number_request)
                if lines_number_from_file <= 0:
                    lines_number_from_file = 5
                logger.setLevel(data["logging level"])

                try:
                    for parameter in parameters:
                        if parameter not in data:
                            raise ValueError
                except ValueError:
                    print(f"this parameter {parameter} does not exist in the json file")
                try:
                    log_file = open(data["log_file"])
                    for line in log_file.readlines():
                        list_of_content = []
                        http_request_header = []
                        request = ""
                        content_of_a_request = line.split(' ')
                        ip_address = content_of_a_request[0]
                        for v in content_of_a_request[5:8]:
                            http_request_header.append(v)
                        http_request_header.append(content_of_a_request[5:8])
                        for s in content_of_a_request[5:8]:
                            request += s
                        request_response = content_of_a_request[8]
                        list_of_content.append(request)
                        list_of_content.append(request_response)
                        if ip_address not in Dict:
                            Dict[ip_address] = {
                                "contents": list_of_content,
                                "request_header": http_request_header
                            }
                        else:
                            Dict[ip_address]["contents"] = list(
                                chain(*zip(Dict[ip_address].get("contents")), list_of_content))
                            Dict[ip_address]["request_header"] = list(
                                chain(*zip(Dict[ip_address].get("request_header")), http_request_header)
                            )
                    return Dict, method_http, lines_number_from_file, number_request
                except FileNotFoundError:
                    print("The log file does not exists")
            except ValueError:
                print("decoding the JSON file had failed")
    except FileNotFoundError:
        logger.error("The Json file does not exists")


original_dictionary, http_method, lines_number, number_ip_request = read_log()


def assign_in_list(lis):
    http_requests = ("GET", "HEAD", "POST", "PUT", "DELETE",
                     "TRACE", "OPTIONS", "CONNECT", "PATCH")
    methods_l = []
    resource_l = []
    protocols_l = []
    index = 0
    for item in lis:
        if index == 3:
            index = 0
        if index == 0:
            if item[1:] not in http_requests:
                # for requests that do not have a method we are skipping
                continue
            else:
                methods_l.append(item[1:])
        elif index == 1:
            resource_l.append(item)
        elif index == 2:
            protocols_l.append(item)
        index += 1
    return methods_l, resource_l, protocols_l


def requests_index_html(dictionary=None):
    if dictionary is None:
        dictionary = original_dictionary
    requests = {}
    for ip in dictionary:

        content = original_dictionary[ip]["request_header"]

        def all_in_one_list(attributes=content):
            return_list = []
            for x in attributes:
                if type(x) is list:
                    for s in x:
                        return_list.append(s)
                    attributes.remove(x)
                else:
                    return_list.append(x)
            return return_list

        list_con = all_in_one_list(content)

        # logger.info(f"the list is: {list_con}")

        methods, resources, protocols = assign_in_list(list_con)

        # logger.info(f"for {ip}: \n methods are {methods} \n resources are {resources} \n protocols are {protocols}")
        requests[ip] = {
            "methods": methods,
            "resources": resources,
            "protocols": protocols
        }
    return requests
    # logger.info(f"The dictionary is {requests}")


requests_original = requests_index_html()


def print_requests():
    br_line = 1
    logger.info(f"{lines_number}")
    for ip in requests_original:
        methods = requests_original[ip]["methods"]
        resources = requests_original[ip]["resources"]
        index = 0
        for method in methods:
            if method == http_method:
                logger.info(f"The ip {ip} has the method {method} and its resource is {resources[index]}")
                if br_line == lines_number:
                    logger.info("input any key to continue: ")
                    try:
                        input()
                        br_line = 1
                        continue
                    except EOFError:
                        logger.exception("an error had occurred the program will execute"
                                         " to the end now without asking for an input")
                br_line += 1
            index += 1


def number_of_ips_has_a_given_request():
    ip_set = set()
    for ip in requests_original:
        methods = requests_original[ip]["methods"]
        if number_ip_request in methods:
            ip_set.add(ip)
    logger.info(f"The number of ips that has the http method {number_ip_request} is {len(ip_set)}")
    return ip_set


def longest_request():
    returnString = ""
    prev = ""
    for ip in original_dictionary:
        content = original_dictionary[ip]["contents"]
        for request_string in content[0:-1:2]:
            if len(request_string) == len(prev):
                returnString += f", {request_string} and it belongs to: {ip}"
            if len(request_string) > len(prev):
                returnString = f"{request_string} and it belongs to: {ip}"
                prev = request_string
    li = returnString.split(',')
    return random.choice(li)


def ip_requests_number(ip, dictionary=None):
    if dictionary is None:
        dictionary = original_dictionary
    Dict = {}
    ip = str(ip)
    if ip in dictionary:
        Dict = {
            "IP": ip,
            "theNumberOfRequests": len(dictionary[ip]["contents"]) / 2
        }
    else:
        logger.error("The ip address does not exists")

    return Dict


def ip_find(most_active=True, dictionary=None):
    if dictionary is None:
        dictionary = original_dictionary
    returnIp = ""
    minimum = 0
    size = 0
    maximum = sys.maxsize
    for ip in dictionary:
        length = ip_requests_number(ip)["theNumberOfRequests"]
        if length == {}:
            break
        if not most_active:
            if length == maximum:
                returnIp += f" {ip}"
            if length < maximum:
                maximum = length
                returnIp = ip
                size = length
        else:
            if length == minimum:
                returnIp += ip
            if length > minimum:
                minimum = length
                returnIp = ip
                size = length
    return returnIp, size


def non_existent():
    returnSet = set()
    for ip in original_dictionary:
        content = original_dictionary[ip]["contents"]
        index = 0
        for httpCode in content[1::2]:
            if httpCode == "404":
                returnSet.add(content[index])
            index += 2
    return returnSet


def run():
    # number_of_requests = ip_requests_number("38.18.38.6")
    # logger.info(f"the ip : {number_of_requests} ")
    # ip_most, size_most = ip_find()
    # logger.info(f"the most used ip is: {ip_most} and the number of the requests is: {size_most}")
    # ip_least, size_least = ip_find(False)
    # logger.info(f"the least used ip is: {ip_least} and the number of the requests is: {size_least}")
    # stringRequest = longest_request()
    # logger.info(f"the string of the longest request is {stringRequest}")
    # my_set = non_existent()
    # logger.info(f"the following paths do not exists: {my_set}")
    number_of_ips_has_a_given_request()
    print_requests()


if __name__ == "__main__":
    try:
        if original_dictionary is None:
            raise ValueError
        else:
            run()

    except ValueError:
        logger.error("The read logger is an empty dictionary")
