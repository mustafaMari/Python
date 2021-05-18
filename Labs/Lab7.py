import datetime
import re
import logging
timeStampRegex = r"([0-9]{2}\/[A-Za-z]{3}\/[0-9]{4}(:[0-9]{2}){3} \+[0-9]{4})"
httpRequestRegex = r"((GET|POST|HEAD|PUT|DELETE|TRACE|OPTIONS|CONNECT|PATCH)" \
                   r" ((\/.*HTTP\/[0-1].[0-1]).*([2-5][0-9]{2}) ([1-9][0-9]*)))"
ipRegex = r"\b(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"
#https://chrisjwarwick.wordpress.com/2012/09/16/more-regular-expressions-regex-for-ip-v4-addresses/#:~:text=More%20Regular%20Expressions%3A%20Regex%20for%20IP%20v4%20Addresses,Return%20%24Null%20if%20no%20valid%20address%20found.%20


class MalformedHTTPRequest(Exception):
  pass


def timeStamp(time):
  if re.match(timeStampRegex, time):
    return datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S %z')
  else:
    return "The time stamp format is invalid"


class storeHTTPRequest:
  def __init__(self, request):
    request = re.search(httpRequestRegex, request)
    if request:
      self.entireRequest = request.group(1)
      self.requestMethod = request.group(2)
      self.requestSource = request.group(3)
      self.requestPath = request.group(4)
      self.requestCode = request.group(5)
      self.requestSize = request.group(6)
    else:
      raise MalformedHTTPRequest(f"format of the request is incorrect")

  def __str__(self):
    return f"request type is: {self.requestMethod}\n" \
           f"request path is: {self.requestPath}\n" \
           f"request code is: {self.requestCode}\n" \
           f"request size is: {self.requestSize}\n"

  def request_method(self):
    return self.requestMethod

  def request_resource(self):
    return self.requestSource


class logEntry(storeHTTPRequest):
  def __init__(self, log):
    findingIp = re.search(ipRegex, log)
    findingTimeStamp = re.search(timeStampRegex, log)
    findingRequest = re.search(httpRequestRegex, log)
    if findingRequest and findingTimeStamp and findingIp:
      self.ip = findingIp.group(1)
      self.timeStamp = findingTimeStamp.group(1)
      storeHTTPRequest.__init__(self, findingRequest.group(1))
    else:
      raise MalformedHTTPRequest(f"format of the entry is incorrect")

  def __str__(self):
    return f"ip address is: {self.ip}\n" \
           f"timeStamp is {self.timeStamp}\n" \
           f"{storeHTTPRequest.__str__(self)}"


def readLine(line):
  line_obj = logEntry(line)
  return line_obj


def readFileContents(file="access_log-20201025"):
  log_lines = []
  errors = 0
  try:
    log_file = open(file)
    for line in log_file.readlines():
      try:
        log_lines.append(readLine(line))
      except MalformedHTTPRequest:
        errors += 1
    logging.error(f"number of malformed entries is: {errors}")
    return log_lines
  except FileNotFoundError:
    print("Error while opening the file")


validLogs = readFileContents()


def readBetweenTwoTimes(first, second):
  first = timeStamp(first)
  second = timeStamp(second)
  if first > second:
    print("The order is incorrect")
    return
  else:
    for obj in validLogs:
      if first <= timeStamp(obj.timeStamp) <= second:
        print(obj)


if __name__ == '__main__':
  x = storeHTTPRequest('77.242.220.94 - - [19/Oct/2020:13:23:40 +0200] "POST / HTTP/1.1" 301 231 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"')
  print(type(x))
  print(storeHTTPRequest)
  print(type(x) is storeHTTPRequest)

  # print(type(storeHTTPRequest('77.242.220.94 - - [19/Oct/2020:13:23:40 +0200] '
  #                             '"POST / HTTP/1.1" 301 231 "-" "Mozilla/5.0 '
  #                             '(Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"')))
  # readBetweenTwoTimes("18/Aug/2020:02:33:30 +0200", "19/Nov/2020:13:43:42 +0200")
