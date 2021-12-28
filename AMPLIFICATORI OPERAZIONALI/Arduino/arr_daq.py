#
# Description:
#    Arduino Due readout program, client side (PC)
#
#
# Read data from Arduino using pyserial
import argparse
import time
import serial
import re
import sys
import glob

class ARDconn:
    """
    Simple class to connect to the Arduino serial port
    """

    def __init__(self, port='/dev/ttyUSB0', time_out = 1):
        """
        Initialize the serial interface (for the time being)
        """
        self.cnx = ""
        self.status = ""
        self.command = ""
        self.reply_list = []
        self.bytes_written = 0
        self.bytes_read = 0
        try:
            self.cnx = serial.Serial(port, 115200, timeout = time_out)
        except (OSError, serial.SerialException):
            msg = "Cannot open serial connection " +\
                  self.cnx.name
            raise IOError(msg)

    def send_command(self, cmd, bytes_to_read = 512, debug = False):
        """
        Send a command through the serial port and read back
        a reply
        """

        if not self.cnx.is_open:
            self.cnx.open()

        if  len(cmd)>0 :
            self.command = cmd
            try:
                self.bytes_written = self.cnx.write(str.encode(cmd))
                if debug:
                    msg = "[W] Bytes written: " + str(self.bytes_written)
                    print(msg)

            except (serial.SerialTimeoutException):
                msg = "Error writing to serial port. Write operation timeout"
                raise IOError(msg)

        # Wait 200 ms before reading back the modem reply
        time.sleep(0.200)

        ok_tag   = re.compile(r'\r\nOK\r\n')
        command_tag = re.compile(r'\r\nCommand (\w) received\r\n')

        #
        # Read the reply
        self.read_attempts = 0
        buf_read = ""

        while True:

            if self.read_attempts > 10:
                msg = "Max number of read attempts achieved. " +\
                      "Read bytes: " + str(len(buf_read))
                msg += " " + repr(buf_read)
                print(msg)
                return False

            buf_bytes = self.cnx.read(bytes_to_read)
            buf_read += buf_bytes.decode()

            if buf_read != '':

                self.bytes_read = len(buf_read)

                if debug:
                    msg = "[R: " + str(self.read_attempts) +\
                          "] raw buffer: " + repr(buf_read)
                    print(msg)

                if ok_tag.search(buf_read):
                    if debug:
                        msg = "[-] OK tag found, message completed"
                        print(msg)
                    buf_read = buf_read.replace('OK\r\n','OK')
                    break

                elif command_tag.search(buf_read):
                    command_read = command_tag.group(1)
                    if debug:
                        msg = "[-] Command " + command_read +\
                              " received tag found, message completed"
                        print(msg)

                    buf_read = buf_read.replace('OK\r\n','OK')
                    break
                else:
                    #
                    #  wait some milliseconds and perform another read
                    time.sleep(0.500)
                    self.read_attempts += 1

        if debug:
            msg = "[-] Read cycles: " + str(self.read_attempts + 1) +\
                  " bytes read: "     + str(self.bytes_read)
            print(msg)

        # - Decode the message reply
        self.res = buf_read.split('\r\n')
        if command_tag.search(self.res[0]):
          self.command = command_tag.group(1)

        if debug:
            msg = "[-] Converted buffer list: " + str(self.res)
            print(msg)

        return True

    def data_extract(self, file_name="data_01.dat"):
        """
        Extract data received from the Arduino and save it in a dedicated file
        for further data analysis
        """
        if self.command == 'r':
            data = self.res[1].split(',')

            with open(file_name, 'w') as f:
                for item in data[:-1]:
                    f.write("%s " % item)

    def save_data_to_R(self, file_name="data_01.dat", vname="a"):
        """
        Extract data received from the Arduino and save it in a dedicated file
        for further data analysis
        """
        if self.command == 'r':
            data = self.res[1].split(',')

            with open(file_name, 'a') as f:
                f.write("%s <- c(" % vname)
                for item in data[:-2]:
                    f.write("%s, " % item)
                f.write("%s)\n" % data[-2])

    def save_data_to_ROOT(self, file_name="data_01.dat"):
        """
        Extract data received from the Arduino and save it in a dedicated file
        for further data analysis
        """
        if self.command == 'r':
            data = self.res[1].split(',')

            with open(file_name, 'a') as f:
                for index, item in enumerate(data[:-1], start=1):
                    f.write("{0} {1}\n".format(index, item))

    def __str__(self):
        return "Cmd: " + self.command +\
              " Status: " + self.status  +\
              " Reply:  " + self.reply_list +\
              " Bytes written: " + str(self.bytes_written) +\
              " Bytes read: " + str(self.bytes_read)


if __name__=='__main__' :

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file_name", default="data_osc",
                        dest='fname', help="output file name")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-R", "--R_output_file",
                        help="save retrieved data in R file format",
                        action="store_true")
    parser.add_argument("-ROOT", "--ROOT_output_file",
                        help="save retrieved data in simple format that can be easily imported in ROOT", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("verbosity turned on")

    # list serial devices for arduino;
    
    #dlp = glob.glob('COM*')
    #if len(dlp):
    #    msg = "Devices found: {}\n".format(dlp)
    #    print(msg)
    #else:
    #    msg = "No serial device found. Check Arduino USB connection."
    #    print(msg)
    #    sys.exit(1)

    td = ARDconn('COM6')
    time.sleep(3)

    # - Get the Board ID
    td.send_command('b')

    mdaq = ['sa0']
    for item in mdaq:
        td.send_command('s', 1024)
        time.sleep(1)
        td.send_command('r', 16000)
        # save data in a file for R processing
        if args.R_output_file:
            file_name = args.fname + "_R.R"
            td.save_data_to_R(item, file_name)
        if args.ROOT_output_file:
            file_name = args.fname + "_ROOT.dat"
            td.save_data_to_ROOT(file_name)
