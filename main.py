import subprocess
import xml.etree.ElementTree as ET
import ControllerInput as ci

proc = subprocess.Popen(["openmsx -control stdio"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)

class Xml_io:

    def __init__(self, path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.path = path

    def read_setting(self):
        my_dict = {}
        for setting in self.root.iter('setting'):  # iterates through the settings list
            element = setting.text      # get the element name of the attribute
            attribute = setting.attrib['id']  # get the attribute values  associated with the attribute name 'id'
            my_dict.update({attribute: element})  # add the attribute to the dicts key and the element to the value
        # print(my_dict)
        return my_dict

    def check_setting(self, settings=None):  # checks the list for a specific attribute Value
        return_value = (False, None)
        settinglist = self.read_setting()
        for i in settinglist.keys():
            if i == settings:
                return_value = (True, settinglist[i])
                print('setting:', settings, ('| element:'), settinglist[i])
        if return_value == (False, None):
            print('setting not found')
        return return_value

    def change_setting(self, setting=None, new_element=None):
        if new_element is not None and setting is not None:
            print(self.check_setting(setting)[0])
            if self.check_setting(setting)[0] == True:
                for settin in self.root.iter('setting'):
                    if settin.attrib['id'] == setting:
                        settin.text = (new_element)
                        settin.set('id', setting)
                        self.tree.write(self.path)
                        print(setting, 'has been changed to', new_element)
            elif setting == None:
                print('missing the setting you want to change')
            elif new_element == None:
                print('missing a new element')
            else:
                print('irgendwas anderes stimmt nicht')
        else:
            print('missing argument')

class Runtime_io:

    def __init__(self):
        self.process = proc


    def run_omsx(self, xml_settings_path = None):                   # reads the openmsx xml setting and runs openmsx using these settings + somemore like

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

        self.process.stdin.write('<command>openmsx_update enable led</command>')
        self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            print(line)
            self.process.stdout.flush()
            if line == '' and self.process.poll() != None:
                print('break')
                break

    def set_on_runtime(self, setting=None, new_element=None, use_only_set=True):
        if use_only_set == True:
            mystring = str('<command>set '+ setting + ' ' +  new_element + '</command>')
            print(mystring)
            self.process.stdin.write(mystring)
            self.process.stdin.flush()
        if use_only_set == False:
            mystring = str('<command>' + setting + ' ' + new_element + '</command>')
            print(mystring)
            self.process.stdin.write(mystring)
            self.process.stdin.flush()

    def change_control(self, msx_input, joystick='joystick1'):
        hats = {(-1, 0): 'L_hat0', (1, 0): 'R_hat0', (0, -1): 'D_hat0', (0, 1): 'U_hat0'}
        inp = ci.get_controller_input()

        # if remove_old_assaigns:
        #self.set_on_runtime('dict unset joystick1_config', msx_input, use_only_set=False)

        if type(inp) == int:
            setting = str('dict set ' + joystick + '_config ' + msx_input)
            new_element = ('button' + str(inp))
            self.set_on_runtime(setting, new_element, use_only_set=False)

        if type(inp) == tuple:
            if inp in hats:
                setting = str('dict set ' + joystick + '_config ' + msx_input)
                new_element = str(hats.get(inp))
                self.set_on_runtime(setting, new_element, use_only_set=False)

    def put_something_in(self, inp):
        self.process.stdin.write(inp)
        self.process.stdin.flush()


#print(proc())
Runtime_io().run_omsx()
#Runtime_io().get_output()
#Runtime_io().set_on_runtime('scale_factor', '2')
#Runtime_io().set_on_runtime('fullscreen', 'false')

#<command> openmsx_update enable led </command>
#'<command>save</command>'
#'<command>set renderer SDL</command>'
#'  '
#'<command>set scale_factor 1</command>'



#my_path = '/home/Jul/.openMSX/share/settingsBU.xml'

#xml_io(my_path).change_setting(setting = 'fullscreen',new_element='cocks')
#xml_io(my_path).check_setting('fullscreen')
#<command> dict lappend joystick1_config LEFT L_hat0 </command>
#<command> dict lappend joystick1_config RIGHT R_hat0 </command>
#<command> dict lappend joystick1_config UP U_hat0 </command>
#<command> dict lappend joystick1_config DOWN D_hat0 </command>
