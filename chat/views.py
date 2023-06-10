from rest_framework import generics, serializers, status
from .models import Message
from rest_framework.views import APIView
from rest_framework.response import Response
import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
# TODO: Read shared secret key from a file
shared_secret_key = b'\x13\x02\x82\xa3\xcd\xb8\x946\xa6\x90vS\xf3\x1cI\x84\xc0\xa5\x14\xab\xcfc\r\x89\xbd\xe3\x17\x97\x03\xe0\xe4\x9e'

def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = message + (16 - len(message) % 16) * chr(16 - len(message) % 16)
    ciphertext = encryptor.update(padded_message.encode()) + encryptor.finalize()
    return iv + ciphertext

def decrypt_message(ciphertext, key):
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]
    return plaintext.decode()

def send2sock(text):
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
            data, addr = Message.socket.recvfrom(1024) # Getting a byte str or timeout
        except socket.timeout:
            data = None
        if data:
            data = decrypt_message(data, shared_secret_key)
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
            encrpted_msg = encrypt_message(data['text'], shared_secret_key)
            send2sock(encrpted_msg) # Sending a byte str
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            

class SetAttributes(APIView):
    def post(self, request, format=None):
        Message.objects.all().delete() # Delete previous message history from DB

        Message.myPort = request.data['my_port']
        Message.destPort = request.data['dest_port']
        Message.destIP = request.data['dest_ip']
        Message.socket.close()
        Message.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Message.socket.bind((Message.myIP, Message.myPort))
        return Response("", status=status.HTTP_200_OK)