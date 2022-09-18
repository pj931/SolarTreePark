import minimalmodbus
import serial



##There are many additional registers to check the data from day, month, year, etc. These can be added as needed since there are many different registers for this purpose##
def setup_modbus():
    serial_port = "/dev/ttyUSB0"
    #Setting up the controller communication
    controller = minimalmodbus.Instrument(serial_port, 1, debug=False)
    controller.serial.baudrate = 115200
    controller.serial.stopbits = 1
    controller.serial.bytesize = 8
    controller.serial.parity = serial.PARITY_NONE
    controller.serial.timeout = 0.2
    controller.mode = minimalmodbus.MODE_RTU
    controller.clear_buffer_before_each_transaction = True
    #print(controller)
    return controller
#funct_code = 3 for holding register, funct_code = 4 for input register
#ex: reading a single holding register: read_address(controller, 0x9000, False, 3) 
#IMPORTANT: If according to the datasheet you have a holding registers and NOT a read only register, you MUST use funct_code = 3 as an input. funct_code = 4 is only for read registers.
def read_address(controller, addr_low, addr_high=False, funct_code=4):
    while True:
        try:
            value = controller.read_register(addr_low, 2, funct_code, False)
        except:
            continue
        break
    if addr_high != False:
        while True:
            try:
                buffer = controller.read_register(addr_high, 2, funct_code, False)
            except:
                continue
            value = value | (buffer << 16)
            break
    return value 
    
    
if __name__ == '__main__':
    print("Usage: Import modulel and desired functions into script to read voltage, power, etc from Epever module")