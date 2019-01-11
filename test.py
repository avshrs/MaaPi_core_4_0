
from lib.lib_maapi_pcf8591_i2c  import class_get_values as bh

a=((2191, "PCF8591_I2C_0X48_1W", 0,1),(2191, "PCF8591_I2C_0X48_1W", 0,1))

for i in a:
  print a[1]

bh(a)
