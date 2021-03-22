import logging
import sys

logger = logging.getLogger("lab2")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler("lab2.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.info("START")
totalBytes = 0
numberOfLines = 0
mean = 0
processingTime = 0
failedRequests = 0
currentSize = 0
PreviousSize = 0
largestSizePath = 0
listsOfPaths = []
for line in sys.stdin:
    PreviousSize = currentSize
    content = line.split(' ')
    logger.debug(f"Line is: {content}")
    currentSize = int(content[2])
    totalBytes += int(content[2])
    processingTime += int(content[3])
    logger.debug(f"HTTP result code: {content[1]}")
    if content[1] == "404":
        logger.debug(f"Path before editing: {content[0]}")
        content[0] = f"!{content[0]}"
        logger.debug(f"Path after editing: {content[0]}")
        failedRequests += 1
    listsOfPaths.append(content[0])
    if currentSize > PreviousSize:
        largestSizePath = content[0] + " " + content[3].strip('\n')
    numberOfLines += 1
logger.info(f"All paths in log: {listsOfPaths}")
logger.info(f"the path and processing time of the largest resource: {largestSizePath}")
logger.info(f"the number of failed requests: {failedRequests}")
logger.info(f"total number of bytes sent to a user: {totalBytes}")
logger.info(f"total number of kilobytes sent to a user: {totalBytes / 1000}")
try:
    mean = processingTime / numberOfLines
    logger.info(f"mean processing time ofa request: {mean}")
except ZeroDivisionError:
    logger.exception("DIVISION BY ZERO OCCURRED")
logger.info("END")
# https://docs.python.org/3/library/logging.html
# https://www.tutorialspoint.com/logging-in-python
# https://docs.python.org/3/howto/logging-cookbook.html
