from pj2.simulator import sim
from pj2.simulator import to_layer_three
from pj2.event_list import evl
from pj2.packet import *



class A:
    def __init__(self):
        #total number of packets A needs to send
        self.totalseq=0
        #next packet seq # that needs to be acked
        self.nexttobeacked = 0
        self.estimated_rtt = 30
        self.state = "WAIT_LAYER5"
        self.lastpacket = None
        #packets that are waiting to be sent
        self.buf = []
        return

    def A_output(self, m):

        newpacket = packet(seqnum=self.totalseq, payload=m)
        if(self.state == "WAIT_ACK"):
            #still waiting on another packet so buffer this one
            self.buf.append(newpacket)
            return
        #else treat this packet with priority
        self.lastpacket = newpacket
        to_layer_three("A", self.lastpacket)
        evl.start_timer("A", self.estimated_rtt)
        self.state = "WAIT_ACK"
        self.totalseq += 1
        return

    def A_input(self, pkt):
        #if its not the correct packet resend the old packet
        if((pkt.checksum != pkt.get_checksum()) or (pkt.acknum != self.nexttobeacked)):
            to_layer_three("A", self.lastpacket)
            evl.remove_timer()
            evl.start_timer("A", self.estimated_rtt)
            return
        #else update state and send next packet if there is one to be sent
        self.state = "WAIT_LAYER5"
        self.nexttobeacked += 1
        if(len(self.buf) > 0):
            self.lastpacket = self.buf.pop(0)
            to_layer_three("A", self.lastpacket)
            evl.remove_timer()
            evl.start_timer("A", self.estimated_rtt)
            return
        evl.remove_timer()
        return

    def A_handle_timer(self):

        to_layer_three("A", self.lastpacket)
        evl.start_timer("A", self.estimated_rtt)
        return



a = A()
