import machine
from octoliner import Octoliner

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

octoliner.set_sensitivity(230)

print(f"Sensor 3 : {octoliner.analog_read(3)}")
print(f"Sensor 4 : {octoliner.analog_read(4)}")
