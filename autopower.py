#!/bin/env python

"""
Automate powerered loudspeakers power with EATON UPS from Denon DN-500AV pre-amplifier state
"""


def reactor():
    """
    The amplifier uses a Telnet interface (port 23) to send and receive serial commands

    We can subscribe to the power state using PW?\r

    The reply can be either PWON or PWSTANDBY

    The UPS is an EATON powerstation

    It exposes an interface through NUT to control 2 power sockets

    We want them to follow the amp's state
    """
