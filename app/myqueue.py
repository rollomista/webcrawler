import threading
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)

class MyQueue:
    def __init__(self) -> None:
        self.queue = []
        self.cv = threading.Condition()

    def _item_available(self):
        if len(self.queue) > 0:
            print('Almeno un oggetto')
            return True
        else:
            print('Lista vuota')
            return False


    def add_item(self, item):
        with self.cv:
            self.queue.append(item)
            print("Aggiunto item " + str(item))
            self.cv.notify()

    def consume_item(self):
        item = None

        with self.cv:
            self.cv.wait_for(self._item_available)
            item = self.queue.pop(0)
            print("Rimosso item " + str(item))

        return item