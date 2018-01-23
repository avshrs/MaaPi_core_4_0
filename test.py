
from lib.lib_maapi_check import Check

condition, condition_min_max, force  = Check().condition(135)

print ("condition \t\t= {0}".format(condition))
print ("condition_min_max \t= {0}".format(condition_min_max))
print ("force \t\t\t= {0}".format(force))
