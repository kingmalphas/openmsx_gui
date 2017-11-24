import xml.etree.ElementTree as ET  #

## the class ChangeASetting needs the attributevalue and the element name it should be changed to

class ChangeASetting:
    def __init__(self, path, settings=None, new_element=None ):
        self.settings = settings
        self.new_element = new_element
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()


    def get_settinglist(self):
        my_dict = {}
        for setting in self.root.iter('setting'):  # iterates through the settings list
            element = setting.text  # get the element name of the attribute
            attribute = setting.attrib['id']  # get the attribute values  associated with the attribute name 'id'
            my_dict.update({attribute: element})  # add the attribute to the dicts key and the element to the value
        #print(my_dict)
        return my_dict


    def check_setting(self):  # checks the list for a specific attribute Value
        return_value = (False, None)
        settinglist = self.get_settinglist()
        for i in settinglist.keys():
            if i == self.settings:
                return_value = (True, settinglist[i])
                print('setting:', self.settings, ('| element:'),settinglist[i])
        if return_value == (False, None):
            print('setting not found')
        return return_value


    def change_setting(self):
        if self.new_element is not None:
            if self.check_setting()[0] == True:
               for settin in self.root.iter('setting'):
                   if settin.attrib['id'] == self.settings:
                       settin.text = (self.new_element)
                       settin.set('id', self.settings)
                       self.tree.write('output.xml')
                       print(self.settings, 'has been changed to', self.new_element)
            elif self.settings==None:
                print('missing the setting you want to change')
            elif self.new_element==None:
                print('missing a new element')
            else:
                print('irgendwas anderes stimmt nicht')
        else:
            print('missing argument')

#my_path = '/home/Jul/.openMSX/share/settingsBU.xml'
#ChangeASetting(my_path).get_settinglist()

