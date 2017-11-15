import xml.etree.ElementTree as ET

openmsx_settings_path = "/home/Jul/.openMSX/share/settingsBU.xml"

tree = ET.parse(openmsx_settings_path)
root = tree.getroot()


def get_settings():

    my_dict = {}
    for setting in root.iter('setting'):    # iterates through the settings list
        element = setting.text              # get the element name of the attribute
        attribute = setting.attrib['id']    # get the attribute values  associated with the attribute name 'id'
        my_dict.update({attribute: element})
    return my_dict

print(get_settings())









#def read_file():
#   try:
#       f = open(p, "r")
#       print("reading")
#       for line in f:
#           #print(line, end='')
#           lines.append(line)
#       f.close()
#   except Exception:
#       print ("Could not read file")
#       f = open("students.txt", "w+")
#   print(*lines,sep='\n')

#read_file()