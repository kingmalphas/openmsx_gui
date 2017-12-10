import subprocess
from main import xml_io

proc = subprocess.Popen(["openmsx -control stdio"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)


class runtime_io:

    def __init__(self):
        self.process = proc

    def run_omsx(self, xml_settings_path = None):                   # reads the openmsx xml setting and runs openmsx using these settings + somemore like

        self.process.stdin.write('<command>set renderer SDL</command>')
        self.process.stdin.write('<command>set power true</command>')
        self.process.stdin.flush()

        if xml_settings_path is not None:
            malist = xml_io(xml_settings_path).read_setting()
            for key in malist:
                #print ((key,    malist[key]))
                self.process.stdin.write('<command>set {key} {element}</command>'.format(key=key, element=malist[key]))
                self.process.stdin.flush()


    def get_output(self):

        self.process.stdin.write('<command>openmsx_update enable led</command>')
        self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            self.process.stdout.flush()
            if line == '' and self.process.poll() != None:
                print('break')
                break

    def set_on_runtime(self, setting=None, new_element=None):
        mystring = ('<command>set '+ setting + ' ' +  new_element + '</command>')
        self.process.stdin.write(mystring)
        self.process.stdin.flush()


#print(proc())
runtime_io().run_omsx()
#runtime_io().get_output()
runtime_io().set_on_runtime('scale_factor', '1')
runtime_io().set_on_runtime('fullscreen', 'true')

#<command> openmsx_update enable led </command>
#'<command>save</command>'
#'<command>set renderer SDL</command>'
#'<command>set fullscreen TRUE</command>'
#'<command>set scale_factor 1</command>'