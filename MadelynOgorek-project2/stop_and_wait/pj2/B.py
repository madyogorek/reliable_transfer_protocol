from pj2.simulator import to_layer_five
from pj2.packet import send_ack


class B:
    def __init__(self):

        self.nextseq = 0
        return


    def B_input(self, pkt):
        #if expected packet wasn't received, send ack for last received
        if(pkt.checksum != pkt.get_checksum() or (pkt.seqnum != self.nextseq)):
            send_ack("B", self.nextseq -1)
            return
        #otherwise send expected ack and update state
        to_layer_five("B",pkt.payload.data)
        send_ack("B", self.nextseq)
        self.nextseq += 1
        return

    def B_output(self, m):
        return

    def B_handle_timer(self):
        return

b = B()
