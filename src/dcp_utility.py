#! /usr/bin/env python
import pnio_dcp
import argparse
import ipaddress
import socket
import re

MAC_VALIDATE_PATTERN = "^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$"
DEFAULT_TIMEOUT = 10

timeout = DEFAULT_TIMEOUT
host = None

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def isMac(mac_address):
    if(not re.match(MAC_VALIDATE_PATTERN,mac_address)):
        raise argparse.ArgumentTypeError(f'mac address provided "{mac_address}" is invalid.\nUse format aa:bb:cc:dd:ee:ff or aa-bb-cc-dd-ee-ff')
    return mac_address.replace("-",":")

def isIP(ip_addr):
    try:
        ipaddress.ip_address(ip_addr)
    except(Exception, ValueError) as e:
        raise argparse.ArgumentTypeError("Address provided is invalid. Use format 0.0.0.0")
    return ip_addr

def add_mac_arg(parser):
    parser.add_argument(
    "mac",
    type=isMac,
    help="MAC address of the target."
    )

def add_idone_subparser(subparsers):
    parser = subparsers.add_parser("id_one", help="Send DCP Identify request to target with specified MAC address")
    add_mac_arg(parser)

def add_idall_subparser(subparsers):
    parser = subparsers.add_parser("id_all", help="Broadcast DCP Identify All request on subnet")

def add_getip_subparser(subparsers):
    parser = subparsers.add_parser("get_ip", help="Get IP address of target with specified MAC address")
    add_mac_arg(parser)

def add_setip_subparser(subparsers):
    parser = subparsers.add_parser("set_ip", help="Set IP address of target with specified MAC address")
    add_mac_arg(parser)
    parser.add_argument(
    "ipaddr",
    type=isIP,
    help="New ip address for target."
    )
    parser.add_argument(
    "subnet",
    type=isIP,
    help="New subnet mask for target."
    )
    parser.add_argument(
    "gateway",
    type=isIP,
    help="New gateway address for target."
    )

def add_getname_subparser(subparsers):
    parser = subparsers.add_parser("get_name", help="Get name of target with specified MAC address")
    add_mac_arg(parser)
    
def add_setname_subparser(subparsers):
    parser = subparsers.add_parser("set_name", help="Set name of target with specified MAC address")
    add_mac_arg(parser)
    parser.add_argument(
    "name",
    type=str,
    help="New name for target."
    )
    
def add_reset_subparser(subparsers):
    parser = subparsers.add_parser("reset", help="Reset communication parameters of target to factory defaults")
    add_mac_arg(parser)

def add_blink_subparser(subparsers):
    parser = subparsers.add_parser("blink", help="Request target device flash its LEDs to identify locally")
    add_mac_arg(parser)

parser = argparse.ArgumentParser(prog="Profinet DCP Utility", 
    description="A command line utility to interface with devices compatible with Profinet DCP.")

parser.add_argument(
    "--host",
    type=isIP, 
    help="IP address of host running utility"
    )

parser.add_argument(
    "--timeout", 
    type=int, 
    help=f'how long to wait for response messages in seconds (default {timeout}s)'
    )

subparsers = parser.add_subparsers(help="Action to be taken", required=True, dest="action")
add_idone_subparser(subparsers)
add_idall_subparser(subparsers)
add_getip_subparser(subparsers)
add_setip_subparser(subparsers)
add_getname_subparser(subparsers)
add_setname_subparser(subparsers)
add_reset_subparser(subparsers)
add_blink_subparser(subparsers)

cmd = parser.parse_args()


#Validate command line arguments
if(cmd.host == None):
    host = getIP()
else:
    host = cmd.host

if(cmd.timeout != None):
    if(cmd.timeout < 1):
        raise Exception("timeout must be >= 1")
    else:
        timeout = cmd.timeout

#instantiate utility and run command
dcp = pnio_dcp.DCP(host, timeout)
response = None

if(cmd.action.lower() == "id_all"):
    print("sending dcp identify all request")
    print("awaiting responses...")
    response = dcp.identify_all(timeout)
    if(response != None):
        for i in response:
            print(i)

elif(cmd.action.lower() == "id_one"):
    print(f'sending dcp identify request to {cmd.mac}')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.identify(cmd.mac)
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")

elif(cmd.action.lower() == "get_ip"):
    print(f'requesting ip address from {cmd.mac}')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.get_ip_address(cmd.mac)
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")

elif(cmd.action.lower() == "set_ip"):
    print(f'sending command to set ip config of device {cmd.mac} to IP:{cmd.ipaddr}, SUB:{cmd.subnet}, GW:{cmd.gateway}')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.set_ip_address(cmd.mac, [cmd.ipaddr,cmd.subnet,cmd.gateway])
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")

elif(cmd.action.lower() == "get_name"):
    print(f'sending command to get name of device {cmd.mac}')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.get_name_of_station(cmd.mac)
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")

elif(cmd.action.lower() == "set_name"):
    print(f'sending command to set name of device {cmd.mac} to {cmd.name}')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.set_name_of_station(cmd.mac, cmd.name)
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")

elif(cmd.action.lower() == "reset"):
    print(f'sending command to reset device {cmd.mac} to factory defaults')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.reset_to_factory(cmd.mac)
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")

elif(cmd.action.lower() == "blink"):
    print(f'sending command to {cmd.mac} to flash its LEDs')
    print(f'awaiting response from {cmd.mac}')
    try:
        response = dcp.blink(cmd.mac)
        print(response)
    except(Exception, pnio_dcp.error.DcpTimeoutError) as e:
        print("timeout occurred, no response received")
print("done")