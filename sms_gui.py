
import logging
import sys
import datetime

import smpplib.gsm
import smpplib.client
import smpplib.consts

from tkinter import *
from tkinter import ttk

def send_sms(*args):
    try:
        # if you want to know what's happening

        logging.basicConfig(filename='sms_smpp.log', filemode='w', level='DEBUG')

        # Two parts, UCS2, SMS with UDH
        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(MESSAGE.get())
        client = smpplib.client.Client(SMSC_HOST.get(), int(SMSC_PORT.get()))

        # Print when obtain message_id
        client.set_message_sent_handler(
            lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id))
            )
        client.set_message_received_handler(
            lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id))
            )

        client.connect()
        if USER_TYPE.get() == "bind_transceiver":
            client.bind_transceiver(system_id=SYSTEM_ID.get(), password=SYSTEM_PASS.get())
        if USER_TYPE.get() == "bind_transmitter":
                client.bind_transmitter(system_id=SYSTEM_ID.get(), password=SYSTEM_PASS.get())

        for part in parts:
            pdu = client.send_message(
                source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                #source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                # Make sure it is a byte string, not unicode:
                source_addr=SENDER_ID.get(),

                dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                #dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                # Make sure thease two params are byte strings, not unicode:
                destination_addr=DESTINATION_NO.get(),
                short_message=part,

                data_coding=encoding_flag,
                esm_class=msg_type_flag,
                registered_delivery=True,
            )
            print(pdu.sequence)
	
        client.unbind()
        print('Unbind Done')
        client.disconnect()
        print('Disconnected')
        print('Sms sent on: ' + str(datetime.datetime.now()))

    except ValueError:
        pass


root = Tk()
root.title("SMS Tester using SMPP")

mainframe = ttk.Frame(root, padding="3 6 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

SMSC_HOST = StringVar()
SMSC_PORT = StringVar()
SYSTEM_ID = StringVar()
SYSTEM_PASS = StringVar()
USER_TYPE = StringVar()
SENDER_ID = StringVar()
DESTINATION_NO = StringVar()
MESSAGE = StringVar()
LOG_MSG = StringVar()

ttk.Label(mainframe, text="Host IP : ").grid(column=1, row=1, sticky=E)
smsc_host_entry = ttk.Entry(mainframe, width=15, textvariable=SMSC_HOST)
smsc_host_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, text="Host Port : ").grid(column=3, row=1, sticky=E)
smsc_port_entry = ttk.Entry(mainframe, width=15, textvariable=SMSC_PORT)
smsc_port_entry.grid(column=4, row=1, sticky=(W, E))

ttk.Label(mainframe, text="Username : ").grid(column=1, row=2, sticky=E)
smsc_user_entry = ttk.Entry(mainframe, width=15, textvariable=SYSTEM_ID)
smsc_user_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text="Password : ").grid(column=3, row=2, sticky=E)
smsc_pass_entry = ttk.Entry(mainframe, width=15, textvariable=SYSTEM_PASS)
smsc_pass_entry.grid(column=4, row=2, sticky=(W, E))

ttk.Label(mainframe, text="User Type : ").grid(column=1, row=3, sticky=E)
smsc_user_type_entry = ttk.Entry(mainframe, width=15, textvariable=USER_TYPE)
smsc_user_type_entry.grid(column=2, row=3, sticky=(W, E))

ttk.Label(mainframe, text="Sender ID : ").grid(column=3, row=3, sticky=E)
smsc_sender_id_entry = ttk.Entry(mainframe, width=15, textvariable=SENDER_ID)
smsc_sender_id_entry.grid(column=4, row=3, sticky=(W, E))

ttk.Label(mainframe, text="Mobile Number : ").grid(column=1, row=4, sticky=E)
smsc_destination_no_entry = ttk.Entry(mainframe, width=15, textvariable=DESTINATION_NO)
smsc_destination_no_entry.grid(column=2, row=4, sticky=(W, E))

ttk.Label(mainframe, text="Message : ").grid(column=3, row=4, sticky=E)
smsc_message_entry = ttk.Entry(mainframe, width=15, textvariable=MESSAGE)
smsc_message_entry.grid(column=4, row=4, sticky=(W, E))

ttk.Button(mainframe, text="Send SMS", command=send_sms).grid(column=4, row=5, sticky=W)


for child in mainframe.winfo_children(): child.grid_configure(padx=4, pady=7)

root.mainloop()
