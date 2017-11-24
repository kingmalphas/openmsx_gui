import subprocess
from main import ChangeASetting

proc = subprocess.Popen(["openmsx -control stdio"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)


# reads the openmsx xml setting and runs openmsx using these settings

def run_omsx(xml_settings_path, process):
    malist = ChangeASetting(xml_settings_path).get_settinglist()
    process.stdin.write('<command>set renderer SDL</command>')
    process.stdin.write('<command>set power true</command>')

    process.stdout.readline('<command>openmsx_update enable led</command>')

    #for key in malist:
    #    #print ((key, malist[key]))
    #    process.stdin.write('<command>set {key} {element}</command>'.format(key=key, element=malist[key]))
    #    process.stdin.flush()

def change_scalingplus(process):
    process.stdin.write('<command>set scale_factor 2</command>')
    process.stdin.flush()
def change_scalingminus(process):
    process.stdin.write('<command>set scale_factor 1</command>')
    process.stdin.flush()

run_omsx('/home/Jul/.openMSX/share/settings.xml', proc)



while True:
    print('input please')
    iput = input()
    if iput == 'more':
        change_scalingplus(proc)
    elif iput == 'less':
        change_scalingminus(proc)

#<command > setscale_factor1 < / command >

#<command> openmsx_update enable led </command>







        #process.stdin.write('<command>save</command>')

        #'<command>set renderer SDL</command>'
        #'<command>set fullscreen TRUE</command>'
        #'<command>set scale_factor 1</command>'