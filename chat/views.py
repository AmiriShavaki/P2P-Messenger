from rest_framework import generics, serializers, status
from .models import Message
from rest_framework.views import APIView
from rest_framework.response import Response
import socket

def send2sock(text):
    Message.socket.bind((Message.myIP, Message.myPort))
    Message.socket.sendto(text.encode('utf-8'), (Message.destIP, Message.destPort))

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'sent_by_me']

class GetMessages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    def get_queryset(self):

        Message.socket.settimeout(0.2)
        try:
            data, addr = Message.socket.recvfrom(1024)
        except socket.timeout:
            data = None
        if data:
            data = data.decode('utf-8')
            serializer = MessageSerializer(data={'text':data})
            if serializer.is_valid():
                serializer.save()

        return Message.objects.all()

class SendMessage(APIView): 
    def post(self, request, format=None):
        data = request.data
        data['sent_by_me'] = True
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            send2sock(data['text'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            

class SetAttributes(APIView):
    def post(self, request, format=None):
        Message.myPort = request.data['my_port']
        Message.destPort = request.data['dest_port']
        Message.destIP = request.data['dest_ip']
        return Response("", status=status.HTTP_200_OK)