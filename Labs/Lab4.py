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
    parameters = ("log_file", "http_request", "logging level", "number_lines", "second_filter")
    try:
        with open(f_name) as f:
            try:
                data = json.load(f)
                print(data)
                print(data["logging level"])
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
                        list_http_headers = []
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
                    return Dict
                except FileNotFoundError:
                    print("The log file does not exists")
            except ValueError:
                print("decoding the JSON file had failed")
    except FileNotFoundError:
        logger.error("The Json file does not exists")


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

        def assign_in_list(lis=None):
            if lis is None:
                lis = list_con
            methods_l = []
            resource_l = []
            protocols_l = []
            index = 0
            for item in lis:
                if index == 3:
                    index = 0
                if index == 0:
                    if '/' in item:
                        # for requests that do not have a method we are skipping
                        continue
                    else:
                        methods_l.append(item)
                elif index == 1:
                    resource_l.append(item)
                elif index == 2:
                    protocols_l.append(item)
                index += 1
            return methods_l, resource_l, protocols_l

        methods, resources, protocols = assign_in_list()
        index = 0
        for source in resources:
            if "index.html" in source:
                logger.info(f"the ip {ip} has a resource containing index.html. \nthe source is {source} and the "
                            f"method for it is {methods[index][1:]}")
            index += 1
        # logger.info(f"for {ip}: \n methods are {methods} \n resources are {resources} \n protocols are {protocols}")
        requests[ip] = {
            "methods": methods,
            "resources": resources,
            "protocols": protocols
        }
    # logger.info(f"The dictionary is {requests}")


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
    min = 0
    size = 0
    max = sys.maxsize
    for ip in dictionary:
        length = ip_requests_number(ip)["theNumberOfRequests"]
        if length == {}:
            break
        if not most_active:
            if length == max:
                returnIp += f" {ip}"
            if length < max:
                max = length
                returnIp = ip
                size = length
        else:
            if length == min:
                returnIp += ip
            if length > min:
                min = length
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
    # myset = non_existent()
    # logger.info(f"the following paths do not exists: {myset}")
    requests_index_html()


original_dictionary = read_log()

if __name__ == "__main__":
    try:
        if original_dictionary is None:
            raise ValueError
        else:
            run()

    except ValueError:
        logger.error("The read logger is an empty dictionary")
