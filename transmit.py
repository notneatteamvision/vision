import threading

from nt_io import NetworkTableIO


def connection_listener(connected, info):
    print(info, '; connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()


def get_nt():
    return nt_io


def send(vals):
    nt_io.output_consumer(vals)


cond = threading.Condition()
notified = [False]

nt_io = NetworkTableIO('10.19.43.2', 'Vision')
nt_io.add_connection_listener(connection_listener)

with cond:
    print('Waiting for Connection...')
    if not notified[0]:
        cond.wait()
print('Connected')
