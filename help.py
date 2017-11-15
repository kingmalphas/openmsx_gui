from xml.etree.ElementTree import XML, SubElement, Element, tostring

text = """
<root>
    <phoneNumbers>
        <number topic="sys/phoneNumber/1" update="none" />
        <number topic="sys/phoneNumber/2" update="none" />
        <number topic="sys/phoneNumber/3" update="none" />
    </phoneNumbers>

    <gfenSMSnumbers>
        <number topic="sys2/SMSnumber/1" update="none" />
        <number topic="sys2/SMSnumber/2" update="none" />
    </gfenSMSnumbers>
</root>
"""

elem = XML(text)
for node in elem.find('phoneNumbers'):
    print (node.attrib['topic'])
    # Create sub elements
    if node.attrib['topic']=="sys/phoneNumber/1":
        tag = SubElement(node,'TagName')
        tag.attrib['attr'] = 'AttribValue'

#print (tostring(elem))