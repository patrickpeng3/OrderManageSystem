from django.http import HttpResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket


# @accept_websocket
# def echo(request):
#     if not request.is_websocket():
#         try:
#             message = request.GET['message']
#             return HttpResponse(message)
#         except Exception as e:
#             return render(request, 'index.html')
#     else:
#         for message in request.websocket:
#             message = message.decode('utf-8')
#             print(message)
#             for i in range(1, 10):
#                 request.websocket.send(i)
#         else:
#             request.websocket.send("websocket error!")
























