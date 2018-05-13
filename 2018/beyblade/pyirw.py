#!/usr/bin/env python

# Read lirc output, in order to sense key presses on an IR remote.
# There are various Python packages that claim to do this but
# they tend to require elaborate setup and I couldn't get any to work.
# This approach requires a lircd.conf but does not require a lircrc.
# If irw works, then in theory, this should too.
# Based on irw.c, https://github.com/aldebaran/lirc/blob/master/tools/irw.c

# Source: https://github.com/akkana/scripts/blob/master/rpi/pyirw.py

import socket

SOCKPATH = "/var/run/lirc/lircd"

sock = None

def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(1)
    print ('starting up on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

def next_key():
    '''Get the next key pressed. Return keyname, updown.
    '''
    #while True:
    #    data = sock.recv(128)
    #    # print("Data: " + data)
    #    data = data.strip()
    #    if data:
    #        break
    data = b''
    try:
        data = sock.recv(128)
    except socket.timeout:
        print("timed out, moving on")
    data = data.strip()
    if not data:
        print("no data, returning")
        return b'yay', b'yay'

    print("found data, returning")
    words = data.split()
    return words[2], words[1]

if __name__ == '__main__':
    init_irw()

    while True:
        keyname, updown = next_key()
        print('%s (%s)' % (keyname, updown))

