from PyQt5 import QtCore, QtSerialPort, QtWidgets # pyqt imports used
import matplotlib.pyplot as plt
import numpy as np

# set by user
value = 100
arraySize = 500

#app = QtCore.QCoreApplication([]) 
app = QtWidgets.QApplication([]) # use with automatic plotting
[print('port:', i.portName()) for i in QtSerialPort.QSerialPortInfo().availablePorts()] # shows available ports
serial_port = QtSerialPort.QSerialPort('COM4') # set to same as arduino uses
# Use if baud rate not 9600, 9600 is the default
#serial_port.setBaudRate(QtSerialPort.QSerialPort.Baud9600)
serial_port.open(QtCore.QIODevice.ReadWrite) # open port to reading and writing

print('serial port:' , serial_port) # shows serial port instance
print('description:',QtSerialPort.QSerialPortInfo(serial_port).description()) # description of serial port
print('baud rate:' , serial_port.baudRate()) # shows baud rate
print('data bits:', serial_port.dataBits()) # shows data bits
print('parity:' , serial_port.parity()) # shows parity
print('stop bits:', serial_port.StopBits()) # shows stop bits
print('DTR signal:', serial_port.DataTerminalReadySignal) # shows dtr signal, dtr is used to reset arduino
print('flow controls:', serial_port.flowControl()) # shows flow control

dataOut = [] # list to fill with data

def handle_ready_read(): # slot function connected to readyread signal, called when something is there to be read
    while serial_port.bytesAvailable(): # while bytes are available to read from serial port, readline doesn't work with serial.write from arduino since realine expects a '\n', so just bytes are checked to be read
        dataByte = serial_port.readLineData(1) # reads a byte from the line from serial port
        dataOut.append(ord(dataByte)) # appends the number representing the read unicode character 
        if len(dataOut) == arraySize: # if the length of the dataout array is the set arraysize
            serial_port.close() # close the port
            app.quit() # quit the pyqt eventloop


serial_port.readyRead.connect(handle_ready_read) 

serial_port.write(bytes([value])) # returns bytes object of value then writes to serial port
#app.setQuitOnLastWindowClosed(True) # could be needed 
app.exec_() # possibly could use sys.exit(app.exec_()) like in last pyqt code, if not closing properly, but then would need to put the plotting done next before app.quit() in handl ready read

plt.figure() # creating a figure may not be needed with automatic plotting
plt.plot(dataOut, 'o') # plots dataout, index is automatic, starts from 0, length of dataout, plots scatter points with 'o'
plt.xlabel("array index") # x label set
plt.ylabel("8-bit rounded voltage reading") # y label set   
plt.show() # showing the plot may be automatic
print('mean:', np.mean(dataOut)) # prints mean of data out

