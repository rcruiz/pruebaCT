#Analyzer of projects sb3, the new version Scratch 3.0

import json
from collections import Counter
import zipfile
import sys, traceback
import os


class Mastery:

    """Analyzer of projects sb3, the new version Scratch 3.0"""

    def __init__(self):

        self.mastery_dicc = {}		#New dict to save punctuation
        self.total_blocks = [] #List with blocks
        self.blocks_dicc = Counter()		#Dict with blocks


    def process(self, filename):
        """Start the analysis."""
        zip_file = zipfile.ZipFile(filename, "r")
        json_project = json.loads(zip_file.open("project.json").read())
        for key, value in json_project.items():
            if key == "targets":
                for dicc in value:
                    for dicc_key, dicc_value in dicc.items():
                        if dicc_key == "blocks":
                            for blocks, blocks_value in dicc_value.items():
                                if type(blocks_value) is dict:
                                    self.total_blocks.append(blocks_value)

        for block in self.total_blocks:
            for key, value in block.items():
                if key == "opcode":
                    self.blocks_dicc[value] += 1


    def analyze(self):
        """Run and return the results of Mastery. """
        self.logic()
        self.flow_control()
        self.synchronization()
        self.abstraction()
        self.data_representation()
        self.user_interactivity()
        self.parallelization()


    def finalize(self, filename):
        """Output the overall programming competence"""
        result = "" + filename + '\n' + json.dumps(self.mastery_dicc) + '\n'
        total = 0
        for i in self.mastery_dicc.items():
            total += i[1]
        result += ("Total mastery points: %d/21\n" % total)
        average =  float(total)/7
        result += ("Average mastery points: %.2f/3\n" % average)
        if average > 2:
            result += "Overall programming competence: Proficiency"
        elif average > 1:
            result += "Overall programming competence: Developing"
        else:
            result += "Overall programming competence: Basic"
        result2 = list((filename, total, average, result.split(':')[-1][1:]))
        result2.extend(self.mastery_dicc.values()) # To list of values
        #print(item, sep=',', end='', flush=False) # with python3
        # write a row to csv
        print(*[item for item in result2], sep=',')


    def logic(self):
        """Assign the Logic skill result"""
        operations = {'operator_and', 'operator_or', 'operator_not'}
        score = 0
        for operation in operations:
            if self.blocks_dicc[operation]:
                score = 3
                self.mastery_dicc['Logic'] = score
                return

        if self.blocks_dicc['control_if_else']:
            score = 2
        elif self.blocks_dicc['control_if']:
            score = 1

        self.mastery_dicc['Logic'] = score


    def flow_control(self):
        """Assign the Flow Control skill result"""
        score = 0
        if self.blocks_dicc['control_repeat_until']:
            score = 3
        elif (self.blocks_dicc['control_repeat'] or self.blocks_dicc['control_forever']):
            score = 2
        else:
            for block in self.total_blocks:
                for key, value in block.items():
                    if key == "next" and value != None:
                        score = 1
                        break
        self.mastery_dicc['FlowControl'] = score


    def synchronization(self):
        """Assign the Syncronization skill result"""
        score = 0
        if (self.blocks_dicc['control_wait_until'] or
            self.blocks_dicc['event_whenbackdropswitchesto'] or
            self.blocks_dicc['event_broadcastandwait']):
                score = 3
        elif (self.blocks_dicc['event_broadcast'] or
              self.blocks_dicc['event_whenbroadcastreceived'] or
              self.blocks_dicc['control_stop']):
                score = 2
        elif self.blocks_dicc['control_wait']:
                score = 1

        self.mastery_dicc['Synchronization'] = score


    def abstraction(self):
        """Assign the Abstraction skill result"""
        score = 0
        if self.blocks_dicc['control_start_as_clone']:
            score = 3
        elif self.blocks_dicc['procedures_definition']:
            score = 2
        else:
            count = 0
            for block in self.total_blocks:
                for key, value in block.items():
                    if key == "parent" and value == None:
                        count += 1
            if count > 1 :
                score = 1

        self.mastery_dicc['Abstraction'] = score


    def data_representation(self):
        """Assign the Data representation skill result"""
        score = 0
        modifiers = {'motion_movesteps', 'motion_gotoxy', 'motion_glidesecstoxy', 'motion_setx', 'motion_sety',
                     'motion_changexby', 'motion_changeyby', 'motion_pointindirection', 'motion_pointtowards',
                     'motion_turnright', 'motion_turnleft', 'motion_goto',
                     'looks_changesizeby', 'looks_setsizeto', 'looks_switchcostumeto', 'looks_nextcostume',
                     'looks_changeeffectby', 'looks_seteffectto', 'looks_show', 'looks_hide', 'looks_switchbackdropto',
                     'looks_nextbackdrop'}
        lists = {'data_lengthoflist', 'data_showlist', 'data_insertatlist', 'data_deleteoflist', 'data_addtolist',
                 'data_replaceitemoflist', 'data_listcontainsitem', 'data_hidelist', 'data_itemoflist'}
        for item in lists:
            if self.blocks_dicc[item]:
                score = 3
                self.mastery_dicc['DataRepresentation'] = score
                return
        if self.blocks_dicc['data_changevariableby'] or self.blocks_dicc['data_setvariableto']:
            score = 2
        else:
            for modifier in modifiers:
                if self.blocks_dicc[modifier]:
                    score = 1
        self.mastery_dicc['DataRepresentation'] = score


    def user_interactivity(self):
        """Assign the User Interactivity skill result"""
        score = 0
        proficiency = {'videoSensing_videoToggle', 'videoSensing_videoOn', 'videoSensing_whenMotionGreaterThan',
                       'videoSensing_setVideoTransparency', 'sensing_loudness'}

        developing = {'event_whenkeypressed', 'event_whenthisspriteclicked', 'sensing_mousedown', 'sensing_keypressed',
                      'sensing_askandwait', 'sensing_answer'}

        for item in proficiency:
            if self.blocks_dicc[item]:
                self.mastery_dicc['UserInteractivity'] = 3
                return
        for item in developing:
            if self.blocks_dicc[item]:
                self.mastery_dicc['UserInteractivity'] = 2
                return
        if self.blocks_dicc['motion_goto_menu']:
            if self.check_mouse() == 1:
                self.mastery_dicc['UserInteractivity'] = 2
                return
        if self.blocks_dicc['sensing_touchingobjectmenu']:
            if self.check_mouse() == 1:
                self.mastery_dicc['UserInteractivity'] = 2
                return
        if self.blocks_dicc['event_whenflagclicked']:
            score = 1
        self.mastery_dicc['UserInteractivity'] = score


    def check_mouse(self):
        """Check whether there is a block 'go to mouse' or
        'touching mouse-pointer?'
        """
        for block in self.total_blocks:
            for key, value in block.items():
                if key == 'fields':
                    for mouse_key, mouse_val in value.items():
                        if (mouse_key == 'TO' or mouse_key =='TOUCHINGOBJECTMENU') and mouse_val[0] == '_mouse_':
                            return 1
        return 0



    def parallelization (self):
        """Assign the Parallelization skill result"""
        score = 0
        keys = []
        messages = []
        backdrops = []
        multimedia = []
        dict_parall = {}

        dict_parall = self.parallelization_dict()

        if self.blocks_dicc['event_whenbroadcastreceived'] > 1:            # 2 Scripts start on the same received message
            if dict_parall['BROADCAST_OPTION']:
                var_list = set(dict_parall['BROADCAST_OPTION'])
                for var in var_list:
                    if dict_parall['BROADCAST_OPTION'].count(var) > 1:
                        score = 3
                        self.mastery_dicc['Parallelization'] = score
                        return

        if self.blocks_dicc['event_whenbackdropswitchesto'] > 1:           # 2 Scripts start on the same backdrop change
            if dict_parall['BACKDROP']:
                backdrop_list = set(dict_parall['BACKDROP'])
                for var in backdrop_list:
                    if dict_parall['BACKDROP'].count(var) > 1:
                        score = 3
                        self.mastery_dicc['Parallelization'] = score
                        return

        if self.blocks_dicc['event_whengreaterthan'] > 1:                  # 2 Scripts start on the same multimedia (audio, timer) event
            if dict_parall['WHENGREATERTHANMENU']:
                var_list = set(dict_parall['WHENGREATERTHANMENU'])
                for var in var_list:
                    if dict_parall['WHENGREATERTHANMENU'].count(var) > 1:
                        score = 3
                        self.mastery_dicc['Parallelization'] = score
                        return

        if self.blocks_dicc['videoSensing_whenMotionGreaterThan'] > 1:     # 2 Scripts start on the same multimedia (video) event
            score = 3
            self.mastery_dicc['Parallelization'] = score
            return

        if self.blocks_dicc['event_whenkeypressed'] > 1:                   # 2 Scripts start on the same key pressed
            if dict_parall['KEY_OPTION']:
                var_list = set(dict_parall['KEY_OPTION'])
                for var in var_list:
                    if dict_parall['KEY_OPTION'].count(var) > 1:
                        score = 2

        if self.blocks_dicc['event_whenthisspriteclicked'] > 1:           # Sprite with 2 scripts on clicked
            score = 2

        if self.blocks_dicc['event_whenflagclicked'] > 1 and score == 0:  # 2 scripts on green flag
            score = 1

        self.mastery_dicc['Parallelization'] = score


    def parallelization_dict(self):
        dicc = {}

        for block in self.total_blocks:
            for key, value in block.items():
                if key == 'fields':
                    for key_pressed, val_pressed in value.items():
                        if key_pressed in dicc:
                            dicc[key_pressed].append(val_pressed[0])
                        else:
                            dicc[key_pressed] = val_pressed

        return dicc


def main(filename):
    """The entrypoint for the `Mastery` extension"""
    mastery = Mastery()
    mastery.process(filename)
    mastery.analyze()
    return mastery.finalize(filename)


if __name__ == "__main__":

    try:
        filename = sys.argv[1]
        main(filename)
    except IndexError:
        print("You must enter the name of the project.")
    except IOError:
        print(sys.argv[1], " does not exist.")
    except (AttributeError, zipfile.BadZipFile, json.decoder.JSONDecodeError):
        _, _, exc_tb = sys.exc_info()
        formatted_lines = traceback.format_exc().splitlines()
        exception = formatted_lines[-1].split(':')[0]
        print(filename, exception, exc_tb.tb_lineno, sep=',', file=sys.stderr)
