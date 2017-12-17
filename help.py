import subprocess
import xml.etree.ElementTree as ET
import ControllerInput as ci

proc = subprocess.Popen(["openmsx -control stdio"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)

class Runtime_io:

    def __init__(self):
        self.process = proc


    def run_omsx(self, xml_settings_path = None):  # reads the openmsx xml setting and runs openmsx using these settings + somemore like

        self.process.stdin.write('<command>set renderer SDL</command>')
        self.process.stdin.write('<command>set power true</command>')
        self.process.stdin.write('<command>carta /home/Jul/Downloads/MSX_Roms/MetalGear1(J).mx2 </command>')
        self.process.stdin.write('<command>reset</command>')
        self.process.stdin.flush()

        if xml_settings_path is not None:
            malist = Xml_io(xml_settings_path).read_setting()
            for key in malist:
                #print ((key,    malist[key]))
                self.process.stdin.write('<command>set {key} {element}</command>'.format(key=key, element=malist[key]))
                self.process.stdin.flush()


    def get_output(self):
        update_types = ['led', 'media', 'plug', 'unplug', 'setting', 'setting-info', 'status',]

        for ut in update_types:
            print (type)
            self.process.stdin.write('<command>openmsx_update enable '+ut+' </command>')
            self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            print(line)
            self.process.stdout.flush()
            if not line:
                break


Runtime_io().run_omsx()
Runtime_io().get_output()
