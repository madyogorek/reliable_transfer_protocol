from pj2.simulator import sim
from pj2.simulator import to_layer_three
from pj2.event_list import evl
from pj2.packet import *
from pj2.circular_buffer import circular_buffer

class A:
    def __init__(self):

        self.totalpackets = 0
        self.estimated_rtt = 30
        self.window = circular_buffer(8)
        #for when the window is full
        self.buf = []
        # the sequence of the first packet in the window
        self.base = 0

    def A_output(self, m):

        newpacket = packet(seqnum=self.totalpackets, payload=m)
        #if the window isn't full
        if(self.window.isfull() == False):
            #put new packet in the window
            self.window.push(newpacket)
            #send new packet to B
            to_layer_three("A", newpacket)
            #if there are no other packets in the window start the timer
            if(self.window.count == 1):
                evl.start_timer("A", self.estimated_rtt)

            self.totalpackets += 1
        elif(len(self.buf) < 50):
            #if window is full but buffer isn't, buffer the packet
            self.buf.append(newpacket)
            self.totalpackets += 1



    def A_input(self, pkt):

        #if correct ack wasn't received, do not update the state
        if((pkt.checksum != pkt.get_checksum()) or (pkt.acknum != self.base)):
            return
        #if correct ack was received, update the window
        wasFull = self.window.isfull()
        self.window.pop()
        self.base += 1
        evl.remove_timer()
        #if the window was full that means we now have space to send the next packet
        if(wasFull):
            #take next in line packet from the buffer and send
            next = self.buf.pop(0)
            self.window.push(next)
            to_layer_three("A", next)
            if(self.window.count == 1):
                evl.start_timer("A", self.estimated_rtt)
        return

    def A_handle_timer(self):

        #if window is empty don't do anything
        if(self.window.count == 0):
            return
        #else resend all packets in window and restart the timer
        lst = self.window.read_all()
        for i in range(len(lst)):
            to_layer_three("A", lst[i])

        evl.start_timer("A", self.estimated_rtt)


        return


a = A()
