from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import time

import server.app.src.nodes as nodes

async def roman_to_arabic(roman):
    roman_values = {
        'I': 1, 
        'II': 2, 
        'III': 3, 
        'IV': 4, 
        'V': 5, 
        'VI': 6, 
        'VII': 7,
        'VIII': 8, 
        'IX': 9, 
        'X': 10, 
        'XI': 11, 
        'XII': 12,
        'XIII': 13, 
        'XIV': 14, 
        'XV': 15, 
        'XVI': 16, 
        'XVII': 17,
        'XVIII': 18, 
        'XIX': 19, 
        'XX': 20, 
        'XXI': 21, 
        'XXII': 22,
        'XXIII': 23, 
        'XXIV': 24, 
    }
    arabic_num = roman_values[roman]
    return arabic_num

async def scraper_iliad_odyssey(divs, sent_tokenize):
    start = time.time()
    print("in iliad / odyssey -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global scriblerus_data
    scriblerus_data = {
        # 'iliad': {
            'iliad_preface': [],
            'iliad_bk1_argument': [],
            'iliad_bk1': [],
            'iliad_bk2_argument': [],
            'iliad_bk2': [],
            'iliad_bk3_argument': [],
            'iliad_bk3': [],
            'iliad_bk4_argument': [],
            'iliad_bk4': [],
            'iliad_bk5_argument': [],
            'iliad_bk5': [],
            'iliad_bk6_argument': [],
            'iliad_bk6': [],
            'iliad_bk7_argument': [],
            'iliad_bk7': [],
            'iliad_bk8_argument': [],
            'iliad_bk8': [],
            'iliad_bk9_argument': [],
            'iliad_bk9': [],
            'iliad_bk10_argument': [],
            'iliad_bk10': [],
            'iliad_bk11_argument': [],
            'iliad_bk11': [],
            'iliad_bk12_argument': [],
            'iliad_bk12': [],
            'iliad_bk13_argument': [],
            'iliad_bk13': [],
            'iliad_bk14_argument': [],
            'iliad_bk14': [],
            'iliad_bk15_argument': [],
            'iliad_bk15': [],
            'iliad_bk16_argument': [],
            'iliad_bk16': [],
            'iliad_bk17_argument': [],
            'iliad_bk17': [],
            'iliad_bk18_argument': [],
            'iliad_bk18': [],
            'iliad_bk19_argument': [],
            'iliad_bk19': [],
            'iliad_bk20_argument': [],
            'iliad_bk20': [],
            'iliad_bk21_argument': [],
            'iliad_bk21': [],
            'iliad_bk22_argument': [],
            'iliad_bk22': [],
            'iliad_bk23_argument': [],
            'iliad_bk23': [],
            'iliad_bk24_argument': [],
            'iliad_bk24': [],
            # 'odyssey_conclusion': [],
        # }
    }
    iliad_preface_pattern_start = r'Homer is universally allowed'
    bk1_argument_pattern_start = r'THE CONTENTION OF ACHILLES'
    bk1_pattern_start= r'direful spring'
    bk2_argument_pattern_start = r'CATALOGUE OF THE FORCES'
    bk2_pattern_start = r'Now pleasing sleep had'
    bk3_argument_pattern_start = r'THE DUEL OF MENELAUS AND PARIS.'
    bk3_pattern_start = r'care each martial band'
    bk4_argument_pattern_start = r'THE BREACH OF THE TRUCE'
    bk4_pattern_start = r'shining gates unfold'
    bk5_argument_pattern_start = r'THE ACTS OF DIOMED'
    bk5_pattern_start = r'But Pallas now Tydides'
    bk6_argument_pattern_start = r'THE EPISODES OF GLAUCUS AND DIOMED'
    bk6_pattern_start = r'Now heaven forsakes the fight'
    bk7_argument_pattern_start = r'THE SINGLE COMBAT OF HECTOR AND AJAX'
    bk7_pattern_start = r'So spoke the guardian of the Trojan state'
    bk8_argument_pattern_start = r'AND THE DISTRESS OF THE GREEKS'
    bk8_pattern_start = r'fair daughter of the dawn'
    bk9_argument_pattern_start = r'THE EMBASSY TO ACHILLES'
    bk9_pattern_start = r'Thus joyful Troy maintain'
    bk10_argument_pattern_start = r'THE NIGHT-ADVENTURE OF DIOMED AND ULYSSES'
    bk10_pattern_start = r'All night the chiefs before their vessels lay'
    bk11_argument_pattern_start = r'AND THE ACTS OF AGAMEMNON'
    bk11_pattern_start = r'The saffron morn'
    bk12_argument_pattern_start = r'THE BATTLE AT THE GRECIAN WALL'
    bk12_pattern_start = r'pious cares attend'
    bk13_argument_pattern_start = r'IN WHICH NEPTUNE ASSISTS THE GREEKS'
    bk13_pattern_start = r'When now the Thunderer on the'
    bk14_argument_pattern_start = r'JUNO DECEIVES JUPITER BY THE GIRDLE OF VENUS'
    bk14_pattern_start = r'But not the genial feast'
    bk15_argument_pattern_start = r'THE FIFTH BATTLE AT THE SHIPS'
    bk15_pattern_start = r'Now in swift flight they pass the trench profound'
    bk16_argument_pattern_start = r'THE ACTS AND DEATH OF PATROCLUS'
    bk16_pattern_start = r'both armies on the ensanguined shore'
    bk17_argument_pattern_start = r'FOR THE BODY OF PATROCLUS'
    bk17_pattern_start = r'On the cold earth divine Patroclus spread'
    bk18_argument_pattern_start = r'AND NEW ARMOUR MADE HIM BY VULCAN'
    bk18_pattern_start = r'Thus like the rage of fire the combat burns'
    bk19_argument_pattern_start = r'THE RECONCILIATION OF ACHILLES AND AGAMEMNON'
    bk19_pattern_start = r'Soon as Aurora heaved her Orient head'
    bk20_argument_pattern_start = r'THE BATTLE OF THE GODS'
    bk20_pattern_start = r'Thus round Pelides breathing war and blood'
    bk21_argument_pattern_start = r'THE BATTLE IN THE RIVER SCAMANDER'
    bk21_pattern_start = r'gliding stream they drove'
    bk22_argument_pattern_start = r'THE DEATH OF HECTOR'
    bk22_pattern_start = r'smit with panic fear'
    bk23_argument_pattern_start = r'FUNERAL GAMES IN HONOUR OF PATROCLUS'
    bk23_pattern_start = r'Thus humbled in the dust'
    bk24_argument_pattern_start = r'THE REDEMPTION OF THE BODY OF HECTOR'
    bk24_pattern_start=r'Now from the finish'
    iliad_end_pattern_start = r'We have now passed through'

    for div in divs:
        content_text = await div.inner_text()
        soup_popeworks_unparsed = BeautifulSoup(content_text, "html.parser")

        soup_popeworks = soup_popeworks_unparsed.get_text()
        
        all_sents = sent_tokenize(soup_popeworks, "english")
        for s in all_sents:
            sents.append(s)

    for sent in sents:
        lines = re.split(r'\n', sent)
        for line in lines:
            if len(line) < 1:
                continue
            in_iliad_preface = re.findall(iliad_preface_pattern_start, line)
            in_bk1_argument = re.findall(bk1_argument_pattern_start, line)
            in_bk1 = re.findall(bk1_pattern_start, line)
            in_bk2_argument = re.findall(bk2_argument_pattern_start, line)
            in_bk2 = re.findall(bk2_pattern_start, line)
            in_bk3_argument = re.findall(bk3_argument_pattern_start, line)
            in_bk3 = re.findall(bk3_pattern_start, line)
            in_bk4_argument = re.findall(bk4_argument_pattern_start, line)
            in_bk4 = re.findall(bk4_pattern_start, line)
            in_bk5_argument = re.findall(bk5_argument_pattern_start, line)
            in_bk5 = re.findall(bk5_pattern_start, line)
            in_bk6_argument = re.findall(bk6_argument_pattern_start, line)
            in_bk6 = re.findall(bk6_pattern_start, line)
            in_bk7_argument = re.findall(bk7_argument_pattern_start, line)
            in_bk7 = re.findall(bk7_pattern_start, line)
            in_bk8_argument = re.findall(bk8_argument_pattern_start, line)
            in_bk8 = re.findall(bk8_pattern_start, line)
            in_bk9_argument = re.findall(bk9_argument_pattern_start, line)
            in_bk9 = re.findall(bk9_pattern_start, line)
            in_bk10_argument = re.findall(bk10_argument_pattern_start, line)
            in_bk10 = re.findall(bk10_pattern_start, line)
            in_bk11_argument = re.findall(bk11_argument_pattern_start, line)
            in_bk11 = re.findall(bk11_pattern_start, line)
            in_bk12_argument = re.findall(bk12_argument_pattern_start, line)
            in_bk12 = re.findall(bk12_pattern_start, line)
            in_bk13_argument = re.findall(bk13_argument_pattern_start, line)
            in_bk13 = re.findall(bk13_pattern_start, line)
            in_bk14_argument = re.findall(bk14_argument_pattern_start, line)
            in_bk14 = re.findall(bk14_pattern_start, line)
            in_bk15_argument = re.findall(bk15_argument_pattern_start, line)
            in_bk15 = re.findall(bk15_pattern_start, line)
            in_bk16_argument = re.findall(bk16_argument_pattern_start, line)
            in_bk16 = re.findall(bk16_pattern_start, line)
            in_bk17_argument = re.findall(bk17_argument_pattern_start, line)
            in_bk17 = re.findall(bk17_pattern_start, line)
            in_bk18_argument = re.findall(bk18_argument_pattern_start, line)
            in_bk18 = re.findall(bk18_pattern_start, line)
            in_bk19_argument = re.findall(bk19_argument_pattern_start, line)
            in_bk19 = re.findall(bk19_pattern_start, line)
            in_bk20_argument = re.findall(bk20_argument_pattern_start, line)
            in_bk20 = re.findall(bk20_pattern_start, line)
            in_bk21_argument = re.findall(bk21_argument_pattern_start, line)
            in_bk21 = re.findall(bk21_pattern_start, line)
            in_bk22_argument = re.findall(bk22_argument_pattern_start, line)
            in_bk22 = re.findall(bk22_pattern_start, line)
            in_bk23_argument = re.findall(bk23_argument_pattern_start, line)
            in_bk23 = re.findall(bk23_pattern_start, line)
            in_bk24_argument = re.findall(bk24_argument_pattern_start, line)
            in_bk24 = re.findall(bk24_pattern_start, line)
            in_bk24_end = re.findall(iliad_end_pattern_start, line)

            if in_iliad_preface:
                current_state = "in_iliad_preface"
            elif in_bk1_argument:
                current_state = "in_bk1_argument"
            elif in_bk1:
                current_state = "in_bk1"
            elif in_bk2_argument:
                current_state = "in_bk2_argument"
            elif in_bk2:
                current_state = "in_bk2"
            elif in_bk3_argument:
                current_state = "in_bk3_argument"
            elif in_bk3:
                current_state = "in_bk3"
            elif in_bk4_argument:
                current_state = "in_bk4_argument"
            elif in_bk4:
                current_state = "in_bk4"
            elif in_bk5_argument:
                current_state = "in_bk5_argument"
            elif in_bk5:
                current_state = "in_bk5"
            elif in_bk6_argument:
                current_state = "in_bk6_argument"
            elif in_bk6:
                current_state = "in_bk6"
            elif in_bk7_argument:
                current_state = "in_bk7_argument"
            elif in_bk7:
                current_state = "in_bk7"
            elif in_bk8_argument:
                current_state = "in_bk8_argument"
            elif in_bk8:
                current_state = "in_bk8"
            elif in_bk9_argument:
                current_state = "in_bk9_argument"
            elif in_bk9:
                current_state = "in_bk9"
            elif in_bk10_argument:
                current_state = "in_bk10_argument"
            elif in_bk10:
                current_state = "in_bk10"
            elif in_bk11_argument:
                current_state = "in_bk11_argument"
            elif in_bk11:
                current_state = "in_bk11"
            elif in_bk12_argument:
                current_state = "in_bk12_argument"
            elif in_bk12:
                current_state = "in_bk12"
            elif in_bk13_argument:
                current_state = "in_bk13_argument"
            elif in_bk13:
                current_state = "in_bk13"
            elif in_bk14_argument:
                current_state = "in_bk14_argument"
            elif in_bk14:
                current_state = "in_bk14"
            elif in_bk15_argument:
                current_state = "in_bk15_argument"
            elif in_bk15:
                current_state = "in_bk15"
            elif in_bk16_argument:
                current_state = "in_bk16_argument"
            elif in_bk16:
                current_state = "in_bk16"
            elif in_bk17_argument:
                current_state = "in_bk17_argument"  
            elif in_bk17:
                current_state = "in_bk17"
            elif in_bk18_argument:
                current_state = "in_bk18_argument"
            elif in_bk18:
                current_state = "in_bk18"
            elif in_bk19_argument:
                current_state = "in_bk19_argument"
            elif in_bk19:
                current_state = "in_bk19"
            elif in_bk20_argument:
                current_state = "in_bk20_argument"
            elif in_bk20:
                current_state = "in_bk20"
            elif in_bk21_argument:
                current_state = "in_bk21_argument"
            elif in_bk21:
                current_state = "in_bk21"
            elif in_bk22_argument:
                current_state = "in_bk22_argument"
            elif in_bk22:
                current_state = "in_bk22"
            elif in_bk23_argument:
                current_state = "in_bk23_argument"
            elif in_bk23:
                current_state = "in_bk23"
            elif in_bk24_argument:
                current_state = "in_bk24_argument"
            elif in_bk24:
                current_state = "in_bk24"
            elif in_bk24_end:
                current_state = "in_iliad_end"
                break

            if current_state == "in_iliad_preface":
                scriblerus_data['iliad_preface'].append(nodes.ShortGeneralNode(
                    title='iliad_preface',
                    text=line
                ))
            elif current_state == "in_bk1_argument":
                scriblerus_data['iliad_bk1_argument'].append(nodes.ShortGeneralNode(
                    title="iliad_bk1_argument",
                    text=line
                ))
            elif current_state == "in_bk1":
                current_line_num +=1
                scriblerus_data['iliad_bk1'].append(nodes.PoemNode(
                    book_number=1,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_bk2_argument":
                scriblerus_data['iliad_bk2_argument'].append(nodes.PoemAnnotationNode(
                    book_number=2,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk2":
                current_line_num +=1
                scriblerus_data['iliad_bk2'].append(nodes.PoemNode(
                    book_number=2,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk3_argument":
                scriblerus_data['iliad_bk3_argument'].append(nodes.PoemAnnotationNode(
                    book_number=3,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk3":
                current_line_num +=1
                scriblerus_data['iliad_bk3'].append(nodes.PoemNode(
                    book_number=3,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk4_argument":
                scriblerus_data['iliad_bk4_argument'].append(nodes.PoemAnnotationNode(
                    book_number=4,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk4":
                current_line_num +=1
                scriblerus_data['iliad_bk4'].append(nodes.PoemNode(
                    book_number=4,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk5_argument":
                # scriblerus_data['iliad_bk5_argument'].append(nodes.PoemAnnotationNode(
                #     book_number=5,
                #     line_number=None,
                #     text=line
                # ))
                scriblerus_data['iliad_preface'].append(nodes.ShortGeneralNode(
                    title='bk5_argument',
                    text=line
                ))
            elif current_state == "in_bk5":
                current_line_num +=1
                scriblerus_data['iliad_bk5'].append(nodes.PoemNode(
                    book_number=5,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk6_argument":
                scriblerus_data['iliad_bk6_argument'].append(nodes.PoemAnnotationNode(
                    book_number=6,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk6":
                current_line_num +=1
                scriblerus_data['iliad_bk6'].append(nodes.PoemNode(
                    book_number=6,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk7_argument":
                scriblerus_data['iliad_bk7_argument'].append(nodes.PoemAnnotationNode(
                    book_number=7,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk7":
                current_line_num +=1
                scriblerus_data['iliad_bk7'].append(nodes.PoemNode(
                    book_number=7,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk8_argument":
                scriblerus_data['iliad_bk8_argument'].append(nodes.PoemAnnotationNode(
                    book_number=8,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk8":
                current_line_num +=1
                scriblerus_data['iliad_bk8'].append(nodes.PoemNode(
                    book_number=8,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk9_argument":
                scriblerus_data['iliad_bk9_argument'].append(nodes.PoemAnnotationNode(
                    book_number=9,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk9":
                current_line_num +=1
                scriblerus_data['iliad_bk9'].append(nodes.PoemNode(
                    book_number=9,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk10_argument":
                scriblerus_data['iliad_bk10_argument'].append(nodes.PoemAnnotationNode(
                    book_number=10,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk10":
                current_line_num +=1
                scriblerus_data['iliad_bk10'].append(nodes.PoemNode(
                    book_number=10,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk11_argument":
                scriblerus_data['iliad_bk11_argument'].append(nodes.PoemAnnotationNode(
                    book_number=11,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk11":
                current_line_num +=1
                scriblerus_data['iliad_bk11'].append(nodes.PoemNode(
                    book_number=11,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk12_argument":
                scriblerus_data['iliad_bk12_argument'].append(nodes.PoemAnnotationNode(
                    book_number=12,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk12":
                current_line_num +=1
                scriblerus_data['iliad_bk12'].append(nodes.PoemNode(
                    book_number=12,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk13_argument":
                scriblerus_data['iliad_bk13_argument'].append(nodes.PoemAnnotationNode(
                    book_number=13,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk13":
                current_line_num +=1
                scriblerus_data['iliad_bk13'].append(nodes.PoemNode(
                    book_number=13,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk14_argument":
                scriblerus_data['iliad_bk14_argument'].append(nodes.PoemAnnotationNode(
                    book_number=14,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk14":
                current_line_num +=1
                scriblerus_data['iliad_bk14'].append(nodes.PoemNode(
                    book_number=14,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk15_argument":
                scriblerus_data['iliad_bk15_argument'].append(nodes.PoemAnnotationNode(
                    book_number=15,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk15":
                current_line_num +=1
                scriblerus_data['iliad_bk15'].append(nodes.PoemNode(
                    book_number=15,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk16_argument":
                scriblerus_data['iliad_bk16_argument'].append(nodes.PoemAnnotationNode(
                    book_number=16,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk16":
                current_line_num +=1
                scriblerus_data['iliad_bk16'].append(nodes.PoemNode(
                    book_number=16,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk17_argument":
                scriblerus_data['iliad_bk17_argument'].append(nodes.PoemAnnotationNode(
                    book_number=17,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk17":
                current_line_num +=1
                scriblerus_data['iliad_bk17'].append(nodes.PoemNode(
                    book_number=17,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk18_argument":
                scriblerus_data['iliad_bk18_argument'].append(nodes.PoemAnnotationNode(
                    book_number=18,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk18":
                current_line_num +=1
                scriblerus_data['iliad_bk18'].append(nodes.PoemNode(
                    book_number=18,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk19_argument":
                scriblerus_data['iliad_bk19_argument'].append(nodes.PoemAnnotationNode(
                    book_number=19,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk19":
                current_line_num +=1
                scriblerus_data['iliad_bk19'].append(nodes.PoemNode(
                    book_number=19,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk20_argument":
                scriblerus_data['iliad_bk20_argument'].append(nodes.PoemAnnotationNode(
                    book_number=20,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk20":
                current_line_num +=1
                scriblerus_data['iliad_bk20'].append(nodes.PoemNode(
                    book_number=20,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk21_argument":
                scriblerus_data['iliad_bk21_argument'].append(nodes.PoemAnnotationNode(
                    book_number=21,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk21":
                current_line_num +=1
                scriblerus_data['iliad_bk21'].append(nodes.PoemNode(
                    book_number=21,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk22_argument":
                scriblerus_data['iliad_bk22_argument'].append(nodes.PoemAnnotationNode(
                    book_number=22,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk22":
                current_line_num +=1
                scriblerus_data['iliad_bk22'].append(nodes.PoemNode(
                    book_number=22,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk23_argument":
                scriblerus_data['iliad_bk23_argument'].append(nodes.PoemAnnotationNode(
                    book_number=23,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk23":
                current_line_num +=1
                scriblerus_data['iliad_bk23'].append(nodes.PoemNode(
                    book_number=23,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_bk24_argument":
                scriblerus_data['iliad_bk24_argument'].append(nodes.PoemAnnotationNode(
                    book_number=24,
                    line_number=None,
                    text=line
                ))
            elif current_state == "in_bk24":
                current_line_num +=1
                scriblerus_data['iliad_bk24'].append(nodes.PoemNode(
                    book_number=24,
                    line_number=None,
                    line=line
                ))
            elif current_state == "in_iliad_end":
                # print("HERE! ", scriblerus_data)
                # return scriblerus_data
                break
            else:
                continue
                # return scriblerus_data

    results = {
        'iliad': {
            'preface': scriblerus_data['iliad_preface'],
            'iliad_bk1_argument': scriblerus_data['iliad_bk1_argument'],
            'iliad_bk1': scriblerus_data['iliad_bk1'],
            'iliad_bk2_argument': scriblerus_data['iliad_bk2_argument'],
            'iliad_bk2': scriblerus_data['iliad_bk2'],
            'iliad_bk3_argument': scriblerus_data['iliad_bk3_argument'],
            'iliad_bk3': scriblerus_data['iliad_bk3'],
            'iliad_bk4_argument': scriblerus_data['iliad_bk4_argument'],
            'iliad_bk4': scriblerus_data['iliad_bk4'],
            'iliad_bk5_argument': scriblerus_data['iliad_bk5_argument'],
            'iliad_bk5': scriblerus_data['iliad_bk5'],
            'iliad_bk6_argument': scriblerus_data['iliad_bk6_argument'],
            'iliad_bk6': scriblerus_data['iliad_bk6'],
            'iliad_bk7_argument': scriblerus_data['iliad_bk7_argument'],
            'iliad_bk7': scriblerus_data['iliad_bk7'],
            'iliad_bk8_argument': scriblerus_data['iliad_bk8_argument'],
            'iliad_bk8': scriblerus_data['iliad_bk8'],
            'iliad_bk9_argument': scriblerus_data['iliad_bk9_argument'],
            'iliad_bk9': scriblerus_data['iliad_bk9'],
            'iliad_bk10_argument': scriblerus_data['iliad_bk10_argument'],
            'iliad_bk10': scriblerus_data['iliad_bk10'],
            'iliad_bk11_argument': scriblerus_data['iliad_bk11_argument'],
            'iliad_bk11': scriblerus_data['iliad_bk11'],
            'iliad_bk12_argument': scriblerus_data['iliad_bk12_argument'],
            'iliad_bk12': scriblerus_data['iliad_bk12'],
            'iliad_bk13_argument': scriblerus_data['iliad_bk13_argument'],
            'iliad_bk13': scriblerus_data['iliad_bk13'],
            'iliad_bk14_argument': scriblerus_data['iliad_bk14_argument'],
            'iliad_bk14': scriblerus_data['iliad_bk14'],
            'iliad_bk15_argument': scriblerus_data['iliad_bk15_argument'],
            'iliad_bk15': scriblerus_data['iliad_bk15'],
            'iliad_bk16_argument': scriblerus_data['iliad_bk16_argument'],
            'iliad_bk16': scriblerus_data['iliad_bk16'],
            'iliad_bk17_argument': scriblerus_data['iliad_bk17_argument'],
            'iliad_bk17': scriblerus_data['iliad_bk17'],
            'iliad_bk18_argument': scriblerus_data['iliad_bk18_argument'],
            'iliad_bk18': scriblerus_data['iliad_bk18'],
            'iliad_bk19_argument': scriblerus_data['iliad_bk19_argument'],
            'iliad_bk19': scriblerus_data['iliad_bk19'],
            'iliad_bk20_argument': scriblerus_data['iliad_bk20_argument'],
            'iliad_bk20': scriblerus_data['iliad_bk20'],
            'iliad_bk21_argument': scriblerus_data['iliad_bk21_argument'],
            'iliad_bk21': scriblerus_data['iliad_bk21'],
            'iliad_bk22_argument': scriblerus_data['iliad_bk22_argument'],
            'iliad_bk22': scriblerus_data['iliad_bk22'],
            'iliad_bk23_argument': scriblerus_data['iliad_bk23_argument'],
            'iliad_bk23': scriblerus_data['iliad_bk23'],
            'iliad_bk24_argument': scriblerus_data['iliad_bk24_argument'],
            'iliad_bk24': scriblerus_data['iliad_bk24']
        }
    }           
    return results
            
