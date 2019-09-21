from lxml import etree
import re

root = etree.parse('LibEmplBio.xml')
researchers = root.iterfind(".//user")


def codify(org_code):

    org_code = re.sub("([.\/'-]|&(\w\S+)?|(\(.*\)))", "", org_code)
    if len(org_code.split()) > 1:
        org_code = ''.join(part[:3].upper() for part in org_code.split())
    return org_code


def codify_position(position):

    position_code = re.sub("([.\/'-]|&(\w\S+)?|(\(.*\)))", "", position)
    position_code = ''.join(part for part in position_code.split())
    position_field = position_code + " - " + position
    print("   Position: " + position_field)
    return position_code


for researcher in researchers:
    print(researcher.find(".//full_name").text)
    duplicates = []
    if researcher.find('.//position').text:
        researcher.find('.//position').text = codify_position(researcher.find('.//position').text)

    for affiliation in researcher.xpath('.//researcher_organization_affiliation'):

        if affiliation.find('.//organization_code').text:
            affiliation.find('.//organization_code').text = codify(affiliation.find('.//organization_code').text)
        if not affiliation.find('.//organization_code').text:
            print("   DELETE EMPTY")
            affiliation.getparent().remove(affiliation)
        else:
            if affiliation.find('.//organization_code').text not in duplicates:
                duplicates.append(affiliation.find('.//organization_code').text)
                print("   KEEP " + affiliation.find('.//organization_code').text)
            else:
                affiliation.getparent().remove(affiliation)
                print("   DUP " + affiliation.find('.//organization_code').text)
            
            
f = open('faculty_researchers.xml', 'wb')
f.write(etree.tostring(root, pretty_print=True))
f.close()
print("done")
