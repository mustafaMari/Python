import re

import pytest

httpRequestRegex = r"((?P<ProperType>GET|POST|HEAD|PUT|DELETE|TRACE|OPTIONS|CONNECT|PATCH)|(?P<BadType>[A-Z]+)) " \
                   r"((?P<ProperPath>\/.*)|(?P<BadPath>[A-Za-z]+)) " \
                   r"((?P<ProperVersion>((HTTP\/)(1\.1|1\.0|2\.0)))|" \
                   r"(?P<BadVersion>(HTTP\/)((1\.[2-9]+)|(2\.[1-9])|([3-9]+\.[0-9]+))))"


class MalformedHTTPRequest(Exception):
    pass


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


def reqstr2obj(request_string):
    # task 2-3 had only 'pass' in this function
    # task 4
    if type(request_string) is not str:
        raise TypeError
    try:
        return storeHTTPRequest(request_string)
    except MalformedHTTPRequest:
        return None


class TestReqStr2Obj:
    def test_reqstr2obj1(self):
        with pytest.raises(TypeError):
            reqstr2obj(8768)

    def setup(self):
        self.request = storeHTTPRequest("GET / HTTP/1.1")

    def test_reqstr2obj2(self):
        assert type(self.request) == storeHTTPRequest

    def test_reqstr2obj3(self):
        assert \
            self.request.requestType == 'GET' \
            and self.request.requestPath == '/' \
            and self.request.requestHTTPProtocol == 'HTTP/1.1'

    def test_reqstr2obj4(self):
        req = 'POST /something HTTP/1.1'
        self.task7 = reqstr2obj(req)
        lis = req.split(' ')
        assert \
            self.task7.requestType == lis[0] \
            and self.task7.requestPath == lis[1] \
            and self.task7.requestHTTPProtocol == lis[2]

    def test_reqstr2obj5(self):
        assert reqstr2obj('GET  / HTTP/1.1"') is None

    def test_reqstr2obj6(self):
        with pytest.raises(BadRequestTypeError):
            reqstr2obj("DOWNLOAD /movie.mp4 HTTP/1.1")

    def test_reqstr2obj7(self):
        with pytest.raises(BadHTTPVersion):
            reqstr2obj('POST /something HTTP/3.1')

    def test_reqstr2obj8(self):
        with pytest.raises(ValueError):
            reqstr2obj('POST something HTTP/3.1')


class storeHTTPRequest:
    def __init__(self, request):
        attr = request.split(' ')
        if len(attr) != 3:
            raise MalformedHTTPRequest
        request = re.search(httpRequestRegex, request)

        if request:
            if request.group('ProperType') is not None:
                self.requestType = request.group('ProperType')
            else:
                raise BadRequestTypeError(f"The Type Of request is invalid")
            if request.group('ProperPath') is not None:
                self.requestPath = request.group('ProperPath')
            else:
                raise ValueError(f"The Path of the request is invalid")
            if request.group('ProperVersion') is not None:
                self.requestHTTPProtocol = request.group('ProperVersion')
            else:
                raise BadHTTPVersion(f"The HTTP version is invalid")
        else:
            raise MalformedHTTPRequest(f"format of the request is incorrect")

    def __str__(self):
        return f"request type is: {self.requestType}\n" \
               f"request path is: {self.requestPath}\n" \
               f"request code is: {self.requestHTTPProtocol}\n"

    def request_type(self):
        return self.requestType

    def request_path(self):
        return self.requestPath

    def request_HTTP_protocol(self):
        return self.requestHTTPProtocol
