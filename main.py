import xml.etree.ElementTree as ET  #

#openmsx_settings_path = "/home/Jul/.openMSX/share/settingsBU.xml"
openmsx_settings_path = "output.xml"

tree = ET.parse(openmsx_settings_path)
root = tree.getroot()

## the class ChangeASetting needs the attributevalue and the element name it should be changed to

class ChangeASetting:
    def __init__(self, settings, new_element):
        self.settings = settings
        self.new_element = new_element

    def get_settinglist(self):
        my_dict = {}
        for setting in root.iter('setting'):  # iterates through the settings list
            element = setting.text  # get the element name of the attribute
            attribute = setting.attrib['id']  # get the attribute values  associated with the attribute name 'id'
            my_dict.update({attribute: element})  # add the attribute to the dicts key and the element to the value
        return my_dict


    def check_setting(self):  # checks the list for a specific attribute Value
        return_value = (False, None)
        settinglist = self.get_settinglist()
        for i in settinglist.keys():
            if i == self.settings:
                return_value = (True, settinglist[i])
                print('found ', self.settings, settinglist[i])
        return return_value

    def change_setting(self):
        if self.check_setting()[0] == True:
           for settin in root.iter('setting'):
               if settin.attrib['id'] == self.settings:
                   settin.text = (self.new_element)
                   settin.set('id', self.settings)
                   tree.write('output.xml')
                   print('Element of the value ', self.settings, 'changed to ', self.new_element)
        else:
           print('setting not available ')



ChangeASetting('scale_factor', 'dicks').change_setting()
ChangeASetting('fullscreen', 'cocks').change_setting()

#print(bla.get_settinglist())
#print(bla.check_setting())
#print(bla.change_setting())
