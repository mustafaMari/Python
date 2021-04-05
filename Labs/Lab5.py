# import logging
# import random
# import json
# import sys
# from itertools import chain
# import configFile
# logger = logging.getLogger("Lab 4")
# f_name = 'file.json'
# parameters = ("log_file", "http_request", "logging level", "number_lines", "second_filter")
# try:
#     with open(f_name) as f:
#         try:
#             data = json.load(f)
#             print(data)
#             print(data["logging level"])
#             logger.setLevel(data["logging level"])
#             formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
#             file_streamer = logging.StreamHandler()
#             file_streamer.setFormatter(formatter)
#             logger.addHandler(file_streamer)
#             try:
#                 for parameter in parameters:
#                     if parameter not in data:
#                         raise ValueError
#             except ValueError:
#                 print(f"this parameter {parameter} does not exist in the json file")
#             try:
#                 log_file = open(data["log_file"])
#             except FileNotFoundError:
#                 print("The log file does not exists")
#         except ValueError:
#             print("decoding the JSON file had failed")
# except FileNotFoundError:
#     logger.error("The Json file does not exists")
#
#
# #
# # def read_logger():
# #     Dict = {}
# #     try:
# #         logs = open(data["log_file"])
# #         for line in logs.readlines():
# #             list_of_content = []
# #             request = ""
# #             content_of_a_request = line.split(' ')
# #             ip_address = content_of_a_request[0]
# #             for s in content_of_a_request[5:8]:
# #                 request += s
# #             request_response = content_of_a_request[8]
# #             list_of_content.append(request)
# #             list_of_content.append(request_response)
# #             if ip_address not in Dict:
# #                 Dict[ip_address] = {
# #                     "contents": list_of_content
# #                 }
# #             else:
# #                 Dict[ip_address]["contents"] = list(chain(*zip(Dict[ip_address].get("contents")), list_of_content))
# #         return Dict