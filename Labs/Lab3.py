import logging

logger = logging.getLogger("Lab3")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler("lab3.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
file_streamer = logging.StreamHandler()
file_streamer.setFormatter(formatter)
logger.addHandler(file_streamer)


def run():
    logger.info("START")
    try:
        userInput = input("File location: ")
        logFile = open(userInput)
        read_log(logFile)
        logFile.close()
    except FileExistsError as e:
        logger.exception(f"FILE DOES NOT EXIST: {e}")
    logger.info("END")


def read_log(logFile):
    returnList = []
    linesCounter = 0
    for line in logFile.readlines():
        if len(line.split()) == 0:
            linesCounter += 1
            continue
        content = line.split(' ')
        del content[4:-1]
        if len(content) != 4 and len(content) != 5:
            logger.error("The number of attributes are different from assumption")
            continue
        linesCounter += 1
        path = str(content[0])
        HTMLResultCode = int(content[1])
        dataSize = int(content[2])
        requestTime = int(content[3])
        attributes = (path, HTMLResultCode, dataSize, requestTime)

        logger.debug(f"The attributes of line {linesCounter} are: {attributes}")
        returnList.append(attributes)

    logger.debug(f"The number of lines which are read (including empty lines) is: {linesCounter}")
    logger.debug(f"The number of entries in the list are: {len(returnList)}")
    successful_reads(returnList)
    failed_reads(returnList)
    print_html_entries(html_entries(returnList))
    return returnList


def successful_reads(logList):
    list2 = find_for_HTTP("2", logList)
    logger.info(f"The number of entries where HTTP result is 2xx are: {len(list2)}")
    return list2


def failed_reads(logList):
    list4 = find_for_HTTP("4", logList)
    list5 = find_for_HTTP("5", logList)
    logger.info(f"The number of entries where HTTP result is 4xx are: {len(list4)}")
    logger.info(f"The number of entries where HTTP result is 5xx are: {len(list5)}")
    return list4 + list5


def find_for_HTTP(x, logList):
    returnList = []
    for attributes in logList:
        HTTPResult = str(attributes[1])
        if HTTPResult[0] == x:
            returnList.append(attributes)
    return returnList


def html_entries(logList):
    returnList = []
    for attributes in logList:
        path = attributes[0]
        if ".html" in path:
            returnList.append(attributes)
    return returnList


def print_html_entries(entries):
    for entry in entries:
        logger.info(f"The following entry's path is an html extension: {entry}")


if __name__ == "__main__":
    run()
