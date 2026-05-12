import smbus

class MCP4725:
    def __init__(self, dynamic_range = 5.2, address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number : int) -> None:
        if not isinstance(number, int):
            raise TypeError("MCP4752 can only receive int at the input")
            return

        if not(0 <= number <= 4095):
            raise ValueError("Number out of range MCP4752 (12 bit)")
            return

        first_byte = self.wm | self.pds | number >> 8

        second_byte = number & 0xFF

        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Number: {number} send to I2C, addres: 0x{(self.address << 1):02X},  data: [0x{first_byte:02X}, 0x{second_byte:02X}]\n")


    def set_voltage(self, voltage : float) -> None:
        if not (0.0 <= voltage <= self.dynamic_range):
            raise ValueError(f"Voltage out of range (0.00 - {self.dynamic_range:.2f} В)")
            return
        self.set_number(int(voltage/self.dynamic_range * 2**12))

dynamic_range = 5.2

def main():
    try:
        dac = MCP4725(dynamic_range, verbose=True)

        while True:
            try:
                voltage = float(input("Input voltage in Volts:  "))
                dac.set_voltage(voltage)
            
            except ValueError:
                print("Not a number. Try again.")
    finally:
        dac.deinit()

if __name__ == "__main__":
    main()