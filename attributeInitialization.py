import json
import zipfile
import sys, os, traceback


class AttributeInitialization():
    """
    Plugin that checks if modified attributes are properly initialized.
    """

    BLOCKMAPPING = {
        'costume': frozenset([('looks_switchbackdropto', 'absolute'),
                              ('looks_nextbackdrop', 'relative'),
                              ('looks_switchcostumeto', 'absolute'),
                              ('looks_nextcostume', 'relative')]),
        'orientation': frozenset([('motion_turnright', 'relative'),
                                  ('motion_turnleft', 'relative'),
                                  ('motion_pointindirection', 'absolute'),
                                  ('motion_pointtowards_menu', 'relative')]),
        'position': frozenset([('motion_movesteps', 'relative'),
                               ('motion_gotoxy', 'absolute'),
                               ('motion_goto', 'relative'),
                               ('motion_glidesecstoxy', 'relative'),
                               ('motion_glideto', 'relative'),
                               ('motion_changexby', 'relative'),
                               ('motion_setx', 'absolute'),
                               ('motion_changeyby', 'relative'),
                               ('motion_sety', 'absolute')]),
        'size': frozenset([('looks_changesizeby', 'relative'),
                           ('looks_setsizeto', 'absolute')]),
        'visibility': frozenset([('looks_hide', 'absolute'),
                                 ('looks_show', 'absolute')])
    }


    def __init__(self):

        self.total_default = 0
        self.list_default = []
        self.attributes = ['costume', 'orientation', 'position', 'size', 'visibility']


    def finalize(self, filename):
        """Output the default attributes initialization found in the project."""
        result = ""
        result += ("%d default attributes initialization found:\n" % self.total_default)
        #for name in self.list_default:
        #    result += name
        #    result += "\n"
        result +='\n'.join(map(str, self.list_default))
        #print(result)
        result2 = self.total_default
        return result2


    def analyze(self, filename):
        """Run and return the results from the SpriteNaming module."""
        zip_file = zipfile.ZipFile(filename, "r")
        json_project = json.loads(zip_file.open("project.json").read())
        #list_attrib, list_abs, list_relative = [], [], []
        list_aux = []
        for key, value in json_project.items():
            if key == "targets":
                for dicc in value:
                    blocks_set = dicc["blocks"]
                    block_list = self.iter_blocks(blocks_set)
                    for name in block_list:
                        for attribute in self.attributes:
                            if (name, 'absolute') in self.BLOCKMAPPING[attribute]:
                                #print(name, 'absolute')
                                list_aux.append((name, 'absolute'))
                            elif (name, 'relative') in self.BLOCKMAPPING[attribute]:
                                #print(name, 'relative')
                                list_aux.append((name, 'relative'))
                            else:
                                list_aux.append(name)
                                #print(name)
        self.list_default = list_aux
        #self.list_default = list_abs + list_relative + list_attrib
        #self.total_default = len(list_abs) + len(list_relative) + len(list_attrib)
        self.total_default = len(list_aux)


    def iter_blocks(self, blocks_set):
        block_list = []
        for _, block_value in blocks_set.items():
            if block_value['opcode'] == 'event_whenflagclicked':
                next_block = block_value["next"]
                for block_id, block in blocks_set.items():
                    if block_id == next_block:
                        block_list.append(str(block['opcode']))
                        next_block = block['next']
        return block_list


def main(filename):
    """The entrypoint for the 'attributeInitialization' extension"""
    attinit = AttributeInitialization()
    attinit.analyze(filename)
    return attinit.finalize(filename)
