
from lib.lib_maapi_check import Check


d = Check().run(20)
print d
if d == True:
    print "true"

if d == False:
    print "False"
