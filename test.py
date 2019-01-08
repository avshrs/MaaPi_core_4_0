
from lib.lib_maapi_pcf8591_i2c  import class_get_values as bh

a=[[2191, "L1_PCF8591_W0", 0,1],[2191, "L1_PCF8591_W0", 0,1]]

for i in a:
  print a[1]

bh(a)
