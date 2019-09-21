from lxml import etree
from copy import deepcopy
import pandas as pd
import re

# load in excel file. returns DataFrame object.
org_file = pd.read_excel("EmployeeGrouping.xlsx", sheet_name="one")
# org_file = pd.read_excel("AcademicUnits.xlsx")

# create root object
units_root = etree.Element('organization_units')

# define unitData
# unit = etree.fromstring('<unit><unitData><organizationCode></organizationCode><organizationName></organizationName><organizationCategory></organizationCategory><organizationType></organizationType><unitType></unitType><description></description><status>ACTIVE</status><data><addressDataList><city></city><country></country><line1></line1><line2></line2><line3></line3><line4></line4><line5></line5><note></note><postalCode></postalCode><stateProvince></stateProvince></addressDataList><alternativeNameList><value></value></alternativeNameList><alternativeNameList><value></value></alternativeNameList><emailDataList><email></email></emailDataList><emailDataList><email></email></emailDataList><emailSuffixList><value></value></emailSuffixList><keywordList><value></value></keywordList><organizationExternalDataList><id></id><type></type></organizationExternalDataList><organizationExternalDataList><id></id><type></type></organizationExternalDataList><phoneDataList><phone></phone><phoneTypeList></phoneTypeList></phoneDataList><webPagesDataList><url></url></webPagesDataList></data></unitData></unit>')

unit = etree.fromstring('<unit><unitData><organizationCode></organizationCode><organizationName></organizationName><organizationCategory></organizationCategory><organizationType></organizationType><unitType>esploro.organization.unit.types.department</unitType><description></description><status>ACTIVE</status></unitData></unit>')
sub_unit = etree.fromstring('<subUnits></subUnits>')

unit_list = []


def codify(org_code):

    org_code = re.sub("([.\/'-]|&(\w\S+)?|(\(.*\)))", "", org_code)
    if len(org_code.split()) > 1:
        org_code = ''.join(part[:3].upper() for part in org_code.split())
    return org_code


def create_unit(unit_value):

    new_org = unit

    organization_code = new_org.find(".//organizationCode")
    organization_code.text = codify(unit_value)

    organization_name = new_org.find(".//organizationName")
    organization_name.text = unit_value

    organization_category = new_org.find(".//organizationCategory")
    organization_category.text = "INTERNAL"

    organization_type = new_org.find(".//organizationType")
    organization_type.text = "EDUCATION"
    
    return new_org


def convert_tiered():

    # iterate through each dataFrame row TWO
    for i, row in org_file.iterrows():
        level_two = str(row['two'])
        level_three = str(row['three'])
        level_four = str(row['four'])

        level_two_code = codify(level_two)
        level_three_code = codify(level_three)
        level_four_code = codify(level_four)

        # two
        if level_two_code not in unit_list:
            unit_list.append(level_two_code)
            # create new unit Object and insert data

            level_two_org = create_unit(level_two)
            units_root.append(deepcopy(level_two_org))

        # three
        if level_three_code not in unit_list:
            codes = units_root.xpath(".//organizationCode")
            for code in codes:
                if code.text == codify(level_two):
                    current_parent_unit = code.getparent().getparent()
                    if current_parent_unit.find('.//subUnits') is None:
                        current_parent_unit.append(deepcopy(sub_unit))

                    level_three_org = create_unit(level_three)

                    current_parent_unit.find(".//subUnits").append(deepcopy(level_three_org))
                    unit_list.append(level_three_code)

        # four
        if level_four_code not in unit_list:
            codes = units_root.findall(".//organizationCode")
            for code in codes:
                if code.text == codify(level_three):
                    current_parent_unit = code.getparent().getparent()
                    if current_parent_unit.find('.//subUnits') is None:
                        current_parent_unit.append(deepcopy(sub_unit))

                    level_four_org = create_unit(level_four)

                    current_parent_unit.find(".//subUnits").append(deepcopy(level_four_org))
                    unit_list.append(level_four_code)


def convert_simple():
    # iterate through each dataFrame row for flat org charts
    for i, row in org_file.iterrows():
        # create new unit Object and insert data
        new_org = unit

        organization_code = new_org.find(".//organizationCode")
        organization_code.text = str(row['CODE'])

        organization_name = new_org.find(".//organizationName")
        organization_name.text = str(row['DESCRIPTION']).title()

        organization_category = new_org.find(".//organizationCategory")
        organization_category.text = "INTERNAL"

        organization_type = new_org.find(".//organizationType")
        organization_type.text = "EDUCATION"

        # description = new_org.find(".//description")
        # description.text = str(row['DESCRIPTION']).title()

        # unit_type = new_org.find(".//unitType")
        # unit_type.text = "DEPARTMENT"

        units_root.append(deepcopy(new_org))


# convert_simple()
convert_tiered()

# create final object and write output
um_organizations = etree.ElementTree(units_root)
um_organizations.write('org_units.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')
print('done')
