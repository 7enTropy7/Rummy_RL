#!/bin/bash
python client.py --client_name A &
python client.py --client_name B &
python client.py --client_name C &
exit 0