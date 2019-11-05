import threading
import time
from networktables import NetworkTables
import numpy as np

# Create listener, for later use
cond = threading.Condition()
notified = [False]
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

# Start server
NetworkTables.initialize()
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# Wait until connected
with cond:
    print("Waiting...")
    if not notified[0]:
        cond.wait()
print("Connected!")

# Create entry listener
def valueChanged(table, key, value, isNew):
    print("%s changed %s to %s" % (table, key, value))
NetworkTables.getTable("left").addEntryListener(valueChanged)
NetworkTables.getTable("right").addEntryListener(valueChanged)
NetworkTables.getTable("target").addEntryListener(valueChanged)

while True:
    time.sleep(1)
