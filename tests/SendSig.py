# This script is used to simulate order notification emails coming from TradeStation
from smtplib import SMTP
from email.mime.text import MIMEText
import sys
import time
import socket


if __name__ == '__main__':
    server = 'localhost'
    port = 25

    if len(sys.argv) >= 2:
        [server, port] = sys.argv[1].split(":")
        
    try:
        server = SMTP(server, port, timeout=6)
    except socket.timeout:
        print "Error: server connection timed out."
        sys.exit()
    except socket.gaierror:
        print "Error: unknown server name:", server
        sys.exit()
    except socket.error:
        print "Error: Connection refused for", server
        sys.exit()

    fromaddr = 'from@tester.net'
    for i in xrange(1):
        i += 1
        toaddr = 'test@receiver.com'
        # 4 types of order message?
        # body = ('TradeStation - New order has been placed for VXX\n'
        """
        body = ('TradeStation - Order has been filled for VXX\n'
                #'        Order: Sell 225 VXX @ Market\n'
                #'        Order: Buy 225 VXX @ Market\n'
                #'        Order: Sell 1000 VXX @ Market\n'
                #'        Order: Sell Short 560 VXX @ Market\n'
                '        Order: Buy to Cover 100 VXX @ Market\n'
                '        Qty Filled: 50\n'
                #'        Entered: 1/6/2017 12:59:01 PM\n'
                '        Duration: Day\n'
                '        Route: Intelligent\n'
                '        Account: SIM524807M\n'
                '        Order#: 4-4060-7888')
        """
        body = ('TradeStation - Order has been filled for TQQQ\n'
                 '   Order: Buy 300 TQQQ @ Market\n'
                 '   Qty Filled: 300\n'
                 '   Filled Price: 65.2000\n'
                 '   Duration: Day\n'
                 '   Route: Intelligent\n'
                 '   Account: SIMXXXX\n'
                 '   Order#: 5-5733-7770')

        msg = MIMEText(body)
        # msg['Subject'] = 'TradeStation - New order has been placed for VXX'
        msg['Subject'] = 'TradeStation - Order has been filled for VXX'
        msg['From'] = 'samhalim@roadrunner.com'
        msg['To'] = ','.join([toaddr])

        try:
            server.sendmail(fromaddr, [toaddr], msg.as_string())
            print "sent", i, "email"
            # time.sleep(1)
        except:
            print "toaddr", toaddr, " has unexpected error:", sys.exc_info()[0]
            print sys.exc_info()[1]

        time.sleep(2)

    server.quit()
