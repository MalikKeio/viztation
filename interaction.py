import matplotlib.pyplot as plt

class InteractiveNode:
    NODE_RADIUS = 10
    def __init__(self, value, position):
        self._value = value
        self._position = position
        self._cid = None

    def getX(self):
        return self._position[0]
    def getY(self):
        return self._position[1]

    def onclick(self, event):
        if self.getX() - InteractiveNode.NODE_RADIUS < event.xdata < self.getX() + InteractiveNode.NODE_RADIUS and self.getY() - InteractiveNode.NODE_RADIUS < event.ydata < self.getY() + InteractiveNode.NODE_RADIUS:
            print('node=%s, button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(self._value, event.button, event.x, event.y, event.xdata, event.ydata))
    def connect(self):
        if self._cid is None:
            self._cid = plt.gcf().canvas.mpl_connect('button_press_event', self.onclick)
    def disconnect(self):
        if self._cid is not None:
            plt.gcf().canvas.mpl_disconnect(self._cid)
            self._cid = None

class InteractiveNodes:
    def __init__(self, pos):
        self.nodes = []
        for value, position in pos.items():
            self.nodes.append(InteractiveNode(value, position))
        self.connect()

    def connect(self):
        for node in self.nodes:
            node.connect()
    def disconnect(self):
        for node in self.nodes:
            node.disconnect()
