#sms_cli.py

import argparse
import datetime

import smpplib.gsm
import smpplib.client
import smpplib.consts

parser = argparse.ArgumentParser(description='This is CLI based Python3 based script to Test SMPP SMS. You can find executable for popular OS and source code at https://github.com/gopalcnepal/Test-SMPP-SMS')

# Add an argument
parser.add_argument('--host', type=str, required=True, help='The IP address of SMSC')
parser.add_argument('--port', type=int, required=True, help='Port Number of the SMSC')
parser.add_argument('--user', type=str, required=True, help='SMPP Username')
parser.add_argument('--passwd', type=str, required=True, help='SMPP Password')
parser.add_argument('--type', type=str, required=True, help='User Type, transmitter or transceiver')
parser.add_argument('--mobile', type=str, required=True, help='Receiving Mobile Number')
parser.add_argument('--sender', type=str, help='Sender ID. If not mentioned default value "SMSCLI" will be used')
parser.add_argument('--message', type=str, help='SMS message. Default will be "Test from SMSCLI"')

args = parser.parse_args()

SMSC_HOST = str(args.host)
SMSC_PORT = str(args.port)
SYSTEM_ID = str(args.user)
SYSTEM_PASS = str(args.passwd)
USER_TYPE = str(args.type)
SENDER_ID = "SMSCLI" if args.sender is None else str(args.sender)
DESTINATION_NO = str(args.mobile)
MESSAGE = "Test from SMSCLI" if args.message is None else str(args.message)

try:
    # Two parts, UCS2, SMS with UDH
    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(MESSAGE)
    client = smpplib.client.Client(SMSC_HOST, int(SMSC_PORT))

    # Print when obtain message_id
    client.set_message_sent_handler(
        lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id))
        )
    client.set_message_received_handler(
        lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id))
        )
    client.connect()
    if USER_TYPE.lower() == "transceiver":
        client.bind_transceiver(system_id=SYSTEM_ID, password=SYSTEM_PASS)
    if USER_TYPE.lower() == "transmitter":
            client.bind_transmitter(system_id=SYSTEM_ID, password=SYSTEM_PASS)
    for part in parts:
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_INTL,
            #source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            # Make sure it is a byte string, not unicode:
            source_addr=SENDER_ID,
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            #dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            # Make sure thease two params are byte strings, not unicode:
            destination_addr=DESTINATION_NO,
            short_message=part,
            data_coding=encoding_flag,
            esm_class=msg_type_flag,
            registered_delivery=True,
        )
        print(pdu.get_status_desc(status=pdu.status))

    client.unbind()
    print('Unbind Done')
    client.disconnect()
    print('Disconnected')
    print('SMS sent on: ' + str(datetime.datetime.now()))

except ValueError:
    pass
