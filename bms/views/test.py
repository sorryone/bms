# -*- coding: utf-8 -*-
import socket
from lib.djhelper.api_view import api_view, api_result, api_render
from django.http import HttpResponse

@api_view(['GET'])
@api_result
def test(request):
    print socket.gethostname()
    print request.META
    return 0, "hello django"


@api_render
def test_template(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return request, "test.html", {'TutorialList': TutorialList}


def test1(reqeust):
    return HttpResponse("helloword")
