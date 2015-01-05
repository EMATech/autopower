#!/bin/env python2

"""
Automate powerered loudspeakers power with EATON UPS from Denon DN-500AV pre-amplifier state
"""

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, TelnetProtocol  # Unavailable in Python3, yet


class TelnetPrinter(TelnetProtocol):
    def connectionMade(self):
        self.transport.write("PW?\n")

    def dataReceived(self, bytes):
        print('Received:', repr(bytes))
        if bytes == 'PWON':
            print('Power is ON')
            # TODO: Enable UPS sockets
        if bytes == 'PWSTANDBY':
            print('Power is STANDBY')
            # TODO: Disable UPS sockets


class TelnetFactory(ClientFactory):
    def buildProtocol(self, addr):
        return TelnetTransport(TelnetPrinter)


if __name__ == '__main__':
    """
    The amplifier uses a Telnet interface (port 23) to send and receive serial commands

    We can subscribe to the power state using PW?\r

    The reply can be either PWON or PWSTANDBY

    The UPS is an EATON powerstation

    It exposes an interface through NUT to control 2 power sockets

    We want them to follow the amp's state
    """
    host = '192.168.1.10'  # TODO: store in a configuration file
    port = 23
    reactor.connectTCP(host, port, TelnetFactory())
    reactor.run()
