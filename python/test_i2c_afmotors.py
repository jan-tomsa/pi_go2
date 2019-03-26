from smbus import SMBus

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
bus.write_i2c_block_data(addr,0,[250,0,0,0,0,0,0])
#bus.write_byte(addr,   0) # M1 mode ... FWD
#bus.write_byte(addr, 250) # M1 speed
#bus.write_byte(addr,   0) # M2 mode ... FWD
#bus.write_byte(addr,   0) # M2 speed ... stop
#bus.write_byte(addr,   0) # M3 mode ... FWD
#bus.write_byte(addr,   0) # M3 speed ... stop
#bus.write_byte(addr,   0) # M4 mode ... FWD
#bus.write_byte(addr,   0) # M4 speed ... stop
i = input("Press return to exit")
bus.write_i2c_block_data(addr,1,[250,0,0,0,0,0,180])
#bus.write_byte(addr, 0x1) # M1 mode  ... BACK
#bus.write_byte(addr, 250) # M1 speed
#bus.write_byte(addr,   0) # M2 mode
#bus.write_byte(addr,   0) # M2 speed ... stop
#bus.write_byte(addr,   0) # M3 mode
#bus.write_byte(addr,   0) # M3 speed ... stop
#bus.write_byte(addr,   0) # M4 mode
#bus.write_byte(addr, 180) # M4 speed  
i = input("Press return to exit")
bus.write_i2c_block_data(addr,0,[0,0,0,0,0,0,0])
#bus.write_byte(addr,   0) # M1 mode ... FWD
#bus.write_byte(addr,   0) # M1 speed ... stop
#bus.write_byte(addr,   0) # M2 mode ... FWD
#bus.write_byte(addr,   0) # M2 speed ... stop
#bus.write_byte(addr,   0) # M3 mode ... FWD
#bus.write_byte(addr,   0) # M3 speed ... stop
#bus.write_byte(addr,   0) # M4 mode ... FWD
#bus.write_byte(addr,   0) # M4 speed ... stop
