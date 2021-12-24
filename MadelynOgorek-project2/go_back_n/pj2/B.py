from pj2.simulator import to_layer_five
from pj2.packet import send_ack


class B:
    def __init__(self):
        # The state only need to maintain the information of expected sequence number of packet
        self.nextseq = 0
        return

    def B_output(self, m):
        return

    def B_input(self, pkt):
        #if correct expected packet wasn't received
        if((pkt.checksum != pkt.get_checksum()) or (pkt.seqnum != self.nextseq)):
            send_ack("B", self.nextseq -1)
            return
        #send correct data to layer 5
        to_layer_five("B", pkt.payload.data)
        send_ack("B", self.nextseq)
        #update next expected sequence number
        self.nextseq += 1
        return

    def B_handle_timer(self):
        return


b = B()

