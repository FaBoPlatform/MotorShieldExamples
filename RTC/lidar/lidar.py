#coding: utf-8
import smbus
import time

bus = smbus.SMBus(1)  # use SMBus
SLAVE_ADDRESS = 0x62 # Slave address of Lider

# Resgiter Address
ADDR_ACQ_COMMAND = 0x00 # DevieConnand
ADDR_STATUS = 0x01 # SystemStatus
ADDR_FULL_DELAY_HIGH = 0x0f # Diatance measurement high byte
ADDR_FULL_DELAY_LOW = 0x10 # Diatance measurement low byte
ADDR_UNIT_ID_HIGH = 0x16 # Serial number low byte
ADDR_UNIT_ID_LOW = 0x17 # Serial number high byte
ADDR_I2C_ID_HIGH = 0x18 # Write serial number high byte for I2C address unlock
ADDR_I2C_ID_LOW = 0x19 # Write serial number low byte for I2C address unlock
ADDR_I2C_SEC_ADDR = 0x1a # Write new I2C address after unlock
ADDR_I2C_CONFIG = 0x1e # Default address response control

class LidarLite():

    def __init__(self, address=SLAVE_ADDRESS):
        print "LidarLite__init__"
        self.address = address

    def getDistance(self):
        # 0x00に0x04の内容を書き込む
        bus.write_block_data(self.address, ADDR_ACQ_COMMAND, [0x04])

        # 0x01を読み込んで、最下位bitが0になるまで読み込む
        value = bus.read_byte_data(self.address, ADDR_STATUS)
        while value & 0x01 == 1:
            value = bus.read_byte_data(self.address, ADDR_STATUS)

        # 0x8fから2バイト読み込んで16bitの測定距離をcm単位で取得する
        high = bus.read_byte_data(self.address, ADDR_FULL_DELAY_HIGH)
        low = bus.read_byte_data(self.address, ADDR_FULL_DELAY_LOW)
        val = ( high << 8 ) + low
        dist = val
        #print "Dist = {0} cm , {1} m".format( dist, dist / 100.0 )
        return dist

    def chageSlaveAddress(self, new_address):
        print "LidarLite.chageSlaveAddress"
        if new_address == None:
            return
        elif new_address == self.address:
            return
        else:
            high = bus.read_byte_data(self.address, ADDR_UNIT_ID_HIGH)
            low = bus.read_byte_data(self.address, ADDR_UNIT_ID_LOW)

            bus.write_byte_data(self.address, ADDR_I2C_ID_HIGH, high)
            bus.write_byte_data(self.address, ADDR_I2C_ID_LOW, low)

            bus.write_block_data(self.address, ADDR_I2C_SEC_ADDR, [new_address])
            bus.write_block_data(self.address, ADDR_I2C_CONFIG, [0x08])

            self.address = new_address

