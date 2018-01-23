
from lib.lib_maapi_check import Check

cond, force  = Check().condition(135)

print ("condition \t= {0}".format(cond))
print ("force \t\t= {0}".format(force))
