from django.db import models
import socket

def getMyIP():
    tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tmp_socket.connect(('192.255.255.255', 1))
        myIP = tmp_socket.getsockname()[0]
    except:
        myIP = '127.0.0.1'
    finally:
        tmp_socket.close()
    return myIP

class Message(models.Model):

    # Default Values of the connection (changable at runtime)
    myPort = 6758
    destPort = 9769
    myIP = getMyIP()
    destIP = '127.0.0.1'
    socket = None

    position = models.CharField(max_length=10, default="left")
    type = models.CharField(max_length=5, default="text")
    title = models.CharField(max_length=5, default="You")
    text = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text
    class Meta:
        ordering = ('timestamp',)