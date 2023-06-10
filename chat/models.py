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

def dirty_code(myIP, myPort):
    ret = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ret.bind((myIP, myPort))
    return ret

class Message(models.Model):

    # Default Values of the connection (changable at runtime)
    myPort = 4000 
    destPort = 4000 
    myIP = getMyIP()
    destIP = '127.0.0.1'
    socket = dirty_code(myIP, myPort)

    sent_by_me = models.BooleanField(default=False)
    text = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text
    class Meta:
        ordering = ('timestamp',)