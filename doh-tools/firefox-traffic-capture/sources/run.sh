#!/usr/bin/env bash

OUTPUT_PCAP_FILE=$NAME".pcap"
OUTPUT_HAR_FILE=$NAME".json"

sudo tcpdump -U -i any port 443 -w $OUTPUT_PCAP_FILE &
sleep 5

sudo -H -u seluser bash -c "/sources/firefox-run-selenium.py $REQUEST_DOMAIN_NAME single"

TCPDUMP_PID=$(ps -e | pgrep tcpdump)

ping 8.8.8.8 -i 0.1 -c 20

kill -2 $TCPDUMP_PID

sudo -H -u seluser bash -c "/sources/firefox-run-selenium.py $REQUEST_DOMAIN_NAME proxy $OUTPUT_HAR_FILE"
