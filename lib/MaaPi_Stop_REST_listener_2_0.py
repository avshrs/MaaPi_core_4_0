
import commands
from MaaPi_Settings import Maapi_rest_server_port

command_port="lsof -t -i:{0}".format(Maapi_rest_server_port)
command_kill="kill"


value=commands.getstatusoutput('{}'.format(command_port))
kill=commands.getstatusoutput('{}'.format("{0} {1}".format(command_kill,value[1])))
print kill[1]
1
