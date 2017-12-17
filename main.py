import subprocess
import xml.etree.ElementTree as ET
import controller_input as ci


class Xml_io:
    def __init__(self, path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.path = path

    def read_setting(self):
        my_dict = {}
        # iterates through the settings list
        for setting in self.root.iter('setting'):
            element = setting.text  # get the element name of the attribute
            # get the attribute values  associated with the attribute name 'id'
            attribute = setting.attrib['id']
            # add the attribute to the dicts key and the element to the value
            my_dict.update({attribute: element})
        return my_dict

    def check_setting(self, settings=None):
        """checks the list for a specific attribute Value"""
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
        # TODO refactor using guard clause
        # https://testing.googleblog.com/2017/06/code-health-reduce-nesting-reduce.html

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
        self.process = subprocess.Popen(
            ['openmsx', '-control', 'stdio'],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)

    def run_omsx(self, xml_settings_path=None):
        """reads the openmsx xml setting and runs openmsx
           using these settings + somemore like"""

        # TODO make rom path configurable
        rom = '/home/Jul/Downloads/MSX_Roms/MetalGear1(J).mx2'
        self.process.stdin.write('<command>set renderer SDL</command>')
        self.process.stdin.write('<command>set power true</command>')
        self.process.stdin.write('<command>carta {}</command>'.format(rom))
        self.process.stdin.write('<command>reset</command>')
        self.process.stdin.flush()

        if xml_settings_path is not None:
            malist = Xml_io(xml_settings_path).read_setting()
            for key in malist:
                self.process.stdin.write(
                    '<command>set {key} {element}</command>'.format(
                        key=key, element=malist[key]))
                self.process.stdin.flush()

    def get_output(self):
        update_types = [
            'led', 'media', 'plug', 'unplug', 'setting', 'setting-info',
            'status'
        ]

        for ut in update_types:
            self.process.stdin.write('<command>openmsx_update enable ' + ut +
                                     ' </command>')
            self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            print(line)
            self.process.stdout.flush()
            if not line: break

    def set_on_runtime(self, setting=None, new_element=None,
                       use_only_set=True):
        if use_only_set == True:
            mystring = str('<command>set ' + setting + ' ' + new_element +
                           '</command>')
            print(mystring)
            self.process.stdin.write(mystring)
            self.process.stdin.flush()
        if use_only_set == False:
            mystring = str('<command>' + setting + ' ' + new_element +
                           '</command>')
            print(mystring)
            self.process.stdin.write(mystring)
            self.process.stdin.flush()

    def change_control(self, msx_input, joystick='joystick1'):
        hats = {
            (-1, 0): 'L_hat0',
            (1, 0): 'R_hat0',
            (0, -1): 'D_hat0',
            (0, 1): 'U_hat0'
        }
        inp = ci.get_controller_input()

        if type(inp) == int:
            setting = str('dict set ' + joystick + '_config ' + msx_input)
            new_element = ('button' + str(inp))
            self.set_on_runtime(setting, new_element, use_only_set=False)

        if type(inp) == tuple:
            if inp in hats:
                setting = str('dict set ' + joystick + '_config ' + msx_input)
                new_element = str(hats.get(inp))
                self.set_on_runtime(setting, new_element, use_only_set=False)

        if type(inp) == list:
            setting = setting = str('dict set ' + joystick + '_config ' +
                                    msx_input)
            new_element = None
            axis = inp[0]
            if (inp[1]) > 0:
                new_element = ('+axis' + str(axis))
            elif (inp[1]) < 0:
                new_element = ('-axis' + str(axis))
            self.set_on_runtime(setting, new_element, use_only_set=False)

    def change_keyboard(self, key_press, layer, joystick="joy1"):
        ############### missing joystick selection ###############
        matrix = {
            '7': '0 0x80',
            ':': '1 0x80',
            'b': '2 0x80',
            'j': '3 0x80',
            'r': '4 0x80',
            'z': '5 0x80',
            'F3': '6 0x80',
            'RETURN': '7 0x80',
            '6': '0 0x40',
            ']': '1 0x40',
            'a': '2 0x40',
            'i': '3 0x40',
            'q': '4 0x40',
            'y': '5 0x40',
            'F2': '6 0x40',
            'SELECT': '7 0x40',
            '5': '0 0x20',
            '[': '1 0x20',
            'dead': '2 0x20',
            'h': '3 0x20',
            'p': '4 0x20',
            'x': '5 0x20',
            'F1': '6 0x20',
            'BS': '7 0x20',
            '4': '0 0x10',
            '\\': '1 0x10',
            '/': '2 0x10',
            'g': '3 0x10',
            'o': '4 0x10',
            'w': '5 0x10',
            'CODE': '6 0x10',
            'STOP': '7 0x10',
            '3': '0 0x08',
            '=': '1 0x08',
            '.': '2 0x08',
            'f': '3 0x08',
            'n': '4 0x08',
            'v': '5 0x08',
            'CAP': '6 0x08',
            'TAB': '7 0x08',
            'DEL': '8 0x08',
            '2': '0 0x04',
            '-': '1 0x04',
            ',': '2 0x04',
            'e': '3 0x04',
            'm': '4 0x04',
            'u': '5 0x04',
            'GRAPH': '6 0x04',
            'ESC': '7 0x04',
            'INS': '8 0x04',
            '1': '0 0x02',
            '9': '1 0x02',
            '~': '2 0x02',
            'd': '3 0x02',
            'l': '4 0x02',
            't': '5 0x02',
            'CTRL': '6 0x02',
            'F5': '7 0x02',
            'HOME': '8 0x02',
            '0': '0 0x01',
            '8': '1 0x01',
            '"': '2 0x01',
            'c': '3 0x01',
            'k': '4 0x01',
            's': '5 0x01',
            'SHIFT': '6 0x01',
            'F4': '7 0x01',
            'SPACE': '8 0x01'
        }

        controller_input = (ci.get_controller_input())

        if type(controller_input) != list:
            controller_input = str(controller_input)
            settingup = str('bind "joy1 button' + controller_input +
                            ' up" -layer ' + layer)
            new_elementup = str('"keymatrixup ' + matrix[key_press] + '"')
            settingdown = str('bind "joy1 button' + controller_input +
                              ' down" -layer ' + layer)
            new_elementdown = str('"keymatrixdown ' + matrix[key_press] + '"')
            self.set_on_runtime(settingup, new_elementup, use_only_set=False)
            self.set_on_runtime(
                settingdown, new_elementdown, use_only_set=False)

        else:
            setting = str('dict set ' + joystick + '_config ' + matrix[
                key_press])
            new_elementup = str('"keymatrixup ' + matrix[key_press] + '"')
            new_elementdown = str('"keymatrixup ' + matrix[key_press] + '"')

            axis = str(controller_input[0])
            value = str(int(controller_input[1]))
            settingup = str('bind "joy1 axis' + axis + ' ' + value +
                            '" -layer ' + layer)
            settingdown = str('bind "joy1 axis' + axis + ' ' + value +
                              '" -layer ' + layer)
            self.set_on_runtime(
                settingdown, new_elementdown, use_only_set=False)
            self.set_on_runtime(settingup, new_elementup, use_only_set=False)
        self.set_on_runtime('activate_input_layer', layer, use_only_set=False)

    def put_something_in(self, inp):
        self.process.stdin.write(inp)
        self.process.stdin.flush()


if __name__ == '__main__':
    Runtime_io().run_omsx()
