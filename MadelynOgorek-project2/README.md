# Header
Madelyn Ogorek,Zhang CSCI4211,13/11/2021

Python3,main.py,,main.py
## How to Run Program:

1. choose either the stop_and_wait or the go_back_n directory.
2. run `python3 main.py` command.

## Description of Program

### stop_and_wait

#### Fields that were added
`.totalseq` was added to A to keep track of the total number of packets that A needs to deliver to B.
`.nexttobeacked` was added to A to keep track of the packet that is next in line to be acked.
`.buf` was a list added to A to hold all the packets A receives that can't yet be sent to B.

#### A_output()
This function is called whenever A receives a new packet that needs to eventually be sent to B. If A is still waiting for an ack for a previous packet, it will buffer the packet. Otherwise, it will send the packet to B and start the timer.

#### A_input()
This function is used when A receives an ack from B. If the packet has been corrupted or the acknum is not the one it is waiting for, it resends the old packet and restarts the timer. Otherwise, it updates A's state and checks the buffer to see if there is another packet to be sent. If so, it sends the next packet and restarts the timer.

#### A_handle_timer()
This function is called when a timer has expired. It resends the last sent packet and starts the timer again.

#### B_input()
This function is called whenever B receives a packet from A. If the packet wasn't what was expected, it sends an ack for the last correctly acked packet. Otherwise it acks the received packet and updates B's state.

### go_back_n

#### Fields that were added
`.totalpackets` was added to A to keep track of the total number of packets that A needs to deliver to B.
`.base` was added to A to keep track of the packet that is next in line to be acked.
`.buf` was a list added to A to hold all the packets A receives that can't yet be sent to B.

#### A_output()
This function is called whenever A receives a new packet that needs to eventually be sent to B. If the window isn't full, it will put the new packet in the window and send it to B. Otherwise, it will buffer the new packet as long as the buffer isn't full. The timer will be started if there isn't already one (there are no other packets in the window).

#### A_input()
This function is used when A receives an ack from B. If the packet was corrupted or wasn't the ack number it was expected, the function does nothing. Otherwise, the acked packet is removed from the window, the timer is removed, and, if a packet is waiting in the buffer, the next packet is sent.

#### A_handle_timer()
This function is called when a timer has expired. It resends all of the packets in the window and restarts the timer.

#### B_input()
This function is called whenever B receives a packet from A. If the correct packet wasn't received, it sends an ack for the last correctly received packet. Otherwise it acks the correct packet and updates B's state.

## Evaluation

### stop_and_wait
In an average test case with a .3 probability of losing packets and a .2 probability of corruption, the program did well and correctly output all 20 of the expected 20 messages. This program recovers from packet loss and corruption by resending the old packet whenever an error has been detected (like in A_input()). In addition, in the case of a timeout, the old packet is also sent again.

### go_back_n
In an average test case with a .3 probability of losing packets and a .2 probability of corruption, this program also did well and correctly output all 20 of the expected 20 messages. This program recovers from packet loss and corruption by resending the old packet whenever an error has been detected (like in A_input()). In addition, in the case of a timeout, all of the packets that are in the window are re-sent.
