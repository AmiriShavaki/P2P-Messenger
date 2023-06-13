from rest_framework import generics, serializers, status
from .models import Message
from rest_framework.views import APIView
from rest_framework.response import Response
import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

shared_secret_key_path = 'C:/Users/admin/Documents/semseter8/Security of Computer Systems/Projects/Final_Project/p2p_messenger/secret_key.txt'

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
    Message.socket.sendto(text, (Message.destIP, Message.destPort))

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
            data = decrypt_message(data, Message.shared_secret_key)
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
            encrpted_msg = encrypt_message(data['text'], Message.shared_secret_key)
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
        if Message.socket: # Prevent attribute error on None object
            Message.socket.close()
        Message.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Message.socket.bind((Message.myIP, Message.myPort))
        with open(shared_secret_key_path, "rb") as binary_file:
            Message.shared_secret_key = binary_file.read()
        return Response("", status=status.HTTP_200_OK)