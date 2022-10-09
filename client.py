from threading import Thread
from time import sleep

class Client(Thread):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
    
    def run(self):
        self.order()
    @staticmethod   
    def order():
        print("running")
        sleep(3)