from smbus import SMBus

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
bus.write_i2c_block_data(addr,0,[250,0,0,0,0,0,0])
i = input("Press return to exit")
bus.write_i2c_block_data(addr,1,[250,0,0,0,0,0,180])
i = input("Press return to exit")
bus.write_i2c_block_data(addr,0,[0,0,0,0,0,0,0])
