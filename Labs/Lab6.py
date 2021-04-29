import logging
import re
import sys

logger = logging.getLogger("Lab 6")
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_streamer = logging.StreamHandler()
file_streamer.setFormatter(formatter)
logger.addHandler(file_streamer)


def read_config():
    f_name = 'lab6.config'
    t = ""
    contents = []
    default_content = ['name', 'access_log-20201025', 'debug',
                       'DEBUG', 'lines', '9', 'separator',
                                              ';', 'filter', 'POST']
    try:
        with open(f_name) as f:
            for line in f:
                t += line
            y = re.findall(r"\[(.*)\]|(name=.*)|(debug=.*)|"
                           r"(lines=.*)|(separator=.*)|(filter=.*)", t)
            for i in y:
                for r in i:
                    if '=' in r:
                        d = r.split('=')
                        contents.append(d[0])
                        contents.append(d[1])
            counter = 1
            for x, t in zip(default_content[0::2], default_content[1::2]):
                if x not in contents:
                    contents.insert(counter - 1, x)
                    contents.insert(counter, t)
                counter += 2
            name = contents[contents.index("name")+1]
            logger.setLevel(contents[contents.index("debug")+1])
            print(contents)
            display = {
              "lines": int(contents[contents.index("lines")+1]),
              "separator": contents[contents.index("separator")+1],
              "filter": contents[contents.index("filter")+1]
            }
            return name, display
    except FileNotFoundError:
        sys.exit(0)


name_file, display_attributes = read_config()


def read_log():
    log_lines = []
    try:
        log_file = open(name_file)
        for line in log_file.readlines():
            log_lines.append(line)
        return log_lines
    except FileNotFoundError:
        print("the file does not exist")
        sys.exit(0)


log_contents = read_log()


def handling_log_lines():
    tuples = []
    for line in log_contents:
        ip_address = re.search(r"^(.*) - -", line)
        time_stamp = re.search(r"([0-9]{2}\/[A-Za-z]{3}\/[0-9]{4}(:[0-9]{2}){3} \+[0-9]{4})", line)
        logLines = re.search(r"\"(GET|POST|HEAD|PUT|DELETE|TRACE|OPTIONS|CONNECT|PATCH) ((\/.*HTTP\/[0-1].[0-1])\" ([2-5][0-9]{2}) ([1-9][0-9]*)) ", line)
        if ip_address and time_stamp and logLines:
            ip_address = ip_address.group(1)
            time_stamp = time_stamp.group(1)
            http_request_header = logLines.group(1)
            http_status_code = int(logLines.group(4))
            size = int(logLines.group(5))
            data = (ip_address, time_stamp,
                    http_request_header, http_status_code, size)
            tuples.append(data)
    return tuples


all_tuples = handling_log_lines()

global_subnet = ""


def print_all_requests(subnet="185.191.0.1"):
    mask_length = (252407 % 16) + 8
    counter = 0
    for ip in all_tuples:
        if check_ip_belong(ip[0], subnet, mask_length):
            print(f"The ip {ip[0]} belongs to the subnet {subnet}")
            counter += 1
            if counter == display_attributes['lines']:
                print("Enter to continue")
                input()
                counter = 0
    return subnet


def check_ip_belong(ip, subnet, maskLength):
    def mask(maskLength2):
        mask_list = []
        while maskLength2 > 0:
            mask_list.append(1)
            maskLength2 -= 1
        while len(mask_list) < 32:
            mask_list.append(0)
        return mask_list

    x = mask(maskLength)
    y = convert_to_binary(subnet)
    firstIp = []
    lastIp = []
    for a, b in zip(x, y):
        t = a & b
        firstIp.append(t)
        k = int(not a)
        d = k | b
        lastIp.append(d)
    ip_binary = convert_to_binary(ip)
    return ip_binary[0:maskLength - 1] == lastIp[0:maskLength - 1] and (
      lastIp[maskLength - 1:] >= ip_binary[maskLength - 1:]
      >= firstIp[maskLength - 1:])


def convert_to_binary(addr):
    parts = addr.split('.')
    binaryFirst = convert(int(parts[0]))
    binarySecond = convert(int(parts[1]))
    binaryThird = convert(int(parts[2]))
    binaryForth = convert(int(parts[3]))
    return binaryFirst + binarySecond + binaryThird + binaryForth


def convert(num):
    return_list = []
    while num > 0:
        reminder = int(num % 2)
        return_list.append(reminder)
        num = int(num / 2)
    while len(return_list) < 8:
        return_list.append(0)
        return_list.reverse()
    return return_list


def print_total_number_bytes():
    total_bytes = 0
    for x in all_tuples:
        if display_attributes['filter'] == re.search(r"[\w]*", x[2]).group():
            total_bytes += x[4]
    print(f"{display_attributes['filter']}"
          f"{display_attributes['separator']} {total_bytes}")


if __name__ == "__main__":
    print(all_tuples)

# Before:
# (venv)
# C:\Users\Mustafa\OneDrive\Documents\GitHub\Python\Labs > pycodestyle
# lab6.py
# lab6.py: 13:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 14:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 15:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 16:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 16:80: E501
# line
# too
# long(119 > 79
# characters)
# lab6.py: 17:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 19:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 21:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 21:80: E501
# line
# too
# long(95 > 79
# characters)
# lab6.py: 22:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 24:11: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 28:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 29:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 31:11: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 32:11: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 34:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 35:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 36:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 41:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 42:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 50:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 51:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 54:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 56:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 65:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 66:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 72:80: E501
# line
# too
# long(87 > 79
# characters)
# lab6.py: 73:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 74:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 75:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 76:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 77:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 78:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 78:80: E501
# line
# too
# long(82 > 79
# characters)
# lab6.py: 79:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 80:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 89:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 90:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 91:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 93:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 94:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 95:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 99:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 103:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 106:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 107:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 109:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 112:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 113:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 114:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 115:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 116:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 122:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 123:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 124:80: E501
# line
# too
# long(86 > 79
# characters)
# lab6.py: 128:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 129:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 130:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 131:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 132:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 133:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 137:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 138:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 142:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 144:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 145:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 149:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 150:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 152:7: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 153:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 153:80: E501
# line
# too
# long(89 > 79
# characters)
# lab6.py: 157:3: E111
# indentation is not a
# multiple
# of
# four
# lab6.py: 158:3: E111
# indentation is not a
# multiple
# of
# four
#
# After:
# Labs > pycodestyle
# lab6.py

