#!/bin/env python2

"""
Automate powered loudspeakers power with EATON UPS from Denon DN-500AV pre-amplifier state
"""

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, TelnetProtocol  # Unavailable in Python3, yet
from PyNUT import PyNUTClient


class DenonProtocol(TelnetProtocol):
    ups_name = 'nutdev1'  # TODO: store in a configuration file
    ups_var = "outlet.2.switchable"  # on means power down or off power up
    ups_username = 'admin'  # TODO: store in a configuration file
    ups_userpass = 'ups'  # TODO: store securely? in a configuration file

    def connectionMade(self):
        # Subscribe to the power state
        self.transport.write("PW?\n")

    def dataReceived(self, bytes):
        ups = PyNUTClient(login=self.ups_username, password=self.ups_userpass)
        if 'PWON' in bytes:
            # Enable UPS sockets
            ups.SetRWVar(ups=self.ups_name, var=self.ups_var, value='no')
        if 'PWSTANDBY' in bytes:
            # Disable UPS sockets
            ups.SetRWVar(ups=self.ups_name, var=self.ups_var, value='yes')


class TelnetFactory(ClientFactory):
    def buildProtocol(self, addr):
        return TelnetTransport(DenonProtocol)


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
