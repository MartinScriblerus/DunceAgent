import json
import pprint
from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import time

import server.app.src.nodes as nodes

def roman_to_arabic(roman):
    roman_values = {
        'I': 1, 
        'II': 2, 
        'III': 3, 
        'IV': 4, 
        'V': 5, 
        'VI': 6, 
        'VII': 7,
    }
    arabic_num = roman_values[roman]
    return arabic_num

async def scraper_moral_essays(divs, sent_tokenize):
    start = time.time()
    print("in moral essays -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global scriblerus_data
    scriblerus_data = {
        # 'epistles_satires': {
        'epistle_to_cobham_intro': [],
        'epistle_to_cobham': [],
        'epistle_to_a_lady': [],
        'epistle_to_bathurst_intro': [],
        'epistle_to_bathurst': [],
        'epistle_to_burlington_intro': [],
        'epistle_to_burlington': [],
        'epistle_to_addison': [],
        'epistle_to_arbuthnot_intro': [],
        'epistle_to_arbuthnot': [],
        'horatian_satires_advertisement': [],
        'epistle_to_fortescue': [],
        'epistle_to_bethel': [],
        'epistle_to_bolingbroke': [],
        'epistle_to_murray': [],
        'epistle_to_augustus_advertisement': [],
        'epistle_to_augustus': [],
        'second_horatian_epistle': [],
        'donne_satire_two': [],
        'donne_satire_four': [],
        'epilogue_dialogue_one': [],
        'epilogue_dialogue_two': [],
        # }
    }
    cobham_intro_pattern_start = r'IN FOUR EPISTLES TO SEVERAL PERSONS.'
    cobham_poem_pattern_start = r'Yes, you despise the man'
    to_a_lady_pattern_start = r'Of the Characters of Women.'
    bathurst_intro_pattern_start = r'TO ALLEN LORD BATHURST'
    bathurst_poem_pattern_start = r'Who shall decide'
    burlington_intro_pattern_start = r'TO RICHARD BOYLE'
    burlington_poem_pattern_start = r'Tis strange, the miser'
    addison_medals_pattern_start = r'Occasioned by his Dialogues on Medals.'
    arbuthnot_epistle_intro_pattern_start = r'EPISTLE TO DR. ARBUTHNOT.'
    arbuthnot_epistle_poem_pattern_start = r'Shut, shut the door'
    horatian_satires_advertisement_pattern_start = r'SATIRES AND EPISTLES OF HORACE IMITATED.'
    to_fortescue_satire_pattern_start = r'TO MR. FORTESCUE.'
    to_bethel_satire_pattern_start = r'TO MR. BETHEL.'
    to_bolingbroke_pattern_start = r'TO LORD BOLINGBROKE.'
    to_murray_pattern_start = r'TO MR. MURRAY.'
    to_augustus_advertisement_start = r'The Reflections of Horace'
    to_augustus_poem_start = r'TO AUGUSTUS.'
    second_horatian_epistle_pattern_start = r'Ludentis'
    donne_satire_two_pattern_start = r'Yes; thank my stars'
    donne_satire_four_pattern_start = r'if it be my time'
    epilogue_dialogue_one_pattern_start = r'EPILOGUE'
    epilogue_dialogue_two_pattern_start = r'Tis all a libel'
    volume_end_pattern = r'END OF THE PROJECT GUTENBERG EBOOK'

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
            in_cobham = re.findall(cobham_intro_pattern_start, line)
            in_cobham_poem = re.findall(cobham_poem_pattern_start, line)
            in_to_a_lady = re.findall(to_a_lady_pattern_start, line)
            in_bathurst = re.findall(bathurst_intro_pattern_start, line, re.IGNORECASE)
            in_bathurst_poem = re.findall(bathurst_poem_pattern_start, line)
            in_burlington = re.findall(burlington_intro_pattern_start, line)
            in_burlington_poem = re.findall(burlington_poem_pattern_start, line)
            in_addison_medals = re.findall(addison_medals_pattern_start, line)
            in_arbuthnot_epistle_intro = re.findall(arbuthnot_epistle_intro_pattern_start, line)
            in_arbuthnot_epistle_poem = re.findall(arbuthnot_epistle_poem_pattern_start, line)
            in_horatian_satires_advertisement = re.findall(horatian_satires_advertisement_pattern_start, line)
            in_to_fortescue_satire = re.findall(to_fortescue_satire_pattern_start, line)
            in_to_bethel_satire = re.findall(to_bethel_satire_pattern_start, line)
            in_to_bolingbroke = re.findall(to_bolingbroke_pattern_start, line)
            in_to_murray = re.findall(to_murray_pattern_start, line)
            in_to_augustus_advertisement = re.findall(to_augustus_advertisement_start, line)
            in_to_augustus_poem = re.findall(to_augustus_poem_start, line)
            in_second_horatian_epistle = re.findall(second_horatian_epistle_pattern_start, line)
            in_donne_satire_two = re.findall(donne_satire_two_pattern_start, line)
            in_donne_satire_four = re.findall(donne_satire_four_pattern_start, line)
            in_epilogue_dialogue_one = re.findall(epilogue_dialogue_one_pattern_start, line, re.IGNORECASE)
            in_epilogue_dialogue_two = re.findall(epilogue_dialogue_two_pattern_start, line)
            in_volume_end = re.findall(volume_end_pattern, line)
    
            if in_cobham:
                current_state = "in_cobham"
            elif in_cobham_poem:
                current_state = "in_cobham_poem"
                current_line_num = 0
            elif in_to_a_lady:
                current_state = "in_to_a_lady"
                current_line_num = 0
            elif in_bathurst:
                current_state = "in_bathurst"
                current_line_num = 0
            elif in_bathurst_poem:
                current_state = "in_bathurst_poem"
                current_line_num = 0
            elif in_burlington:
                current_state = "in_burlington"
                current_line_num = 0
            elif in_burlington_poem:
                current_state = "in_burlington_poem"
                current_line_num = 0
            elif in_addison_medals:
                current_state = "in_addison_medals"
                current_line_num = 0
            elif in_arbuthnot_epistle_intro:
                current_state = "in_arbuthnot_epistle_intro"
                current_line_num = 0
            elif in_arbuthnot_epistle_poem:
                current_line_num = 0
                current_state = "in_arbuthnot_epistle_poem"
            elif in_horatian_satires_advertisement:
                current_state = "in_horatian_satires_advertisement"
            elif in_to_fortescue_satire:
                current_line_num = 0
                current_state = "in_to_fortescue_satire"
            elif in_to_bethel_satire:
                current_line_num = 0
                current_state = "in_to_bethel_satire"
            elif in_to_bolingbroke:
                current_line_num = 0
                current_state = "in_to_bolingbroke"
            elif in_to_murray:
                current_line_num = 0
                current_state = "in_to_murray"
            elif in_to_augustus_advertisement:
                current_state = "in_to_augustus_advertisement"
            elif in_to_augustus_poem:
                current_line_num = 0
                current_state = "in_to_augustus_poem"
            elif in_second_horatian_epistle:
                current_line_num = 0
                current_state = "in_second_horatian_epistle"
            elif in_donne_satire_two:
                current_line_num = 0
                current_state = "in_donne_satire_two"
            elif in_donne_satire_four:
                current_line_num = 0
                current_state = "in_donne_satire_four"
            elif in_epilogue_dialogue_one:
                current_line_num = 0
                current_state = "in_epilogue_dialogue_one"
            elif in_epilogue_dialogue_two:
                current_line_num = 0
                current_state = "in_epilogue_dialogue_two"
            elif in_volume_end:
                current_state = "in_volume_end"



            if current_state == "in_cobham":
                scriblerus_data['epistle_to_cobham_intro'].append(nodes.ShortGeneralNode(
                    title='epistle_to_cobham_intro',
                    text=line
                ))
            elif current_state == "in_cobham_poem":
                current_line_num += 1
                scriblerus_data['epistle_to_cobham'].append(nodes.PoemNode(
                    book_number=1,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_to_a_lady":
                current_line_num += 1
                scriblerus_data['epistle_to_a_lady'].append(nodes.PoemNode(
                    book_number=2,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_bathurst":
                scriblerus_data['epistle_to_bathurst_intro'].append(nodes.ShortGeneralNode(
                    title='epistle_to_bathurst_intro',
                    text=line
                ))
            elif current_state == "in_bathurst_poem":
                current_line_num += 1
                scriblerus_data['epistle_to_bathurst'].append(nodes.PoemNode(
                    book_number=3,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_burlington":
                current_line_num += 1
                scriblerus_data['epistle_to_burlington_intro'].append(nodes.ShortGeneralNode(
                    title='epistle_to_burlington_intro',
                    text=line
                ))
            elif current_state == "in_burlington_poem":
                current_line_num += 1
                scriblerus_data['epistle_to_burlington'].append(nodes.PoemNode(
                    book_number=4,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_addison_medals":
                current_line_num += 1
                scriblerus_data['epistle_to_addison'].append(nodes.PoemNode(
                    book_number=5,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_arbuthnot_epistle_intro":
                scriblerus_data['epistle_to_arbuthnot_intro'].append(nodes.ShortGeneralNode(
                    title='epistle_to_arbuthnot_intro',
                    text=line
                ))
            elif current_state == "in_arbuthnot_epistle_poem":
                current_line_num += 1
                scriblerus_data['epistle_to_arbuthnot'].append(nodes.PoemNode(
                    book_number=1,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_horatian_satires_advertisement":
                scriblerus_data['horatian_satires_advertisement'].append(nodes.ShortGeneralNode(
                    title='in_horatian_satires_advertisement',
                    text=line
                ))
            elif current_state == "in_to_fortescue_satire":
                current_line_num +=1
                scriblerus_data['epistle_to_fortescue'].append(nodes.PoemNode(
                    book_number=2,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_to_bethel_satire":
                current_line_num += 1
                scriblerus_data['epistle_to_bethel'].append(nodes.PoemNode(
                    book_number=3,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_to_bolingbroke":
                current_line_num += 1
                scriblerus_data['epistle_to_bolingbroke'].append(nodes.PoemNode(
                    book_number=4,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_to_murray":
                current_line_num += 1
                scriblerus_data['epistle_to_murray'].append(nodes.PoemNode(
                    book_number=5,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_to_augustus_advertisement":
                scriblerus_data['epistle_to_augustus_advertisement'].append(nodes.ShortGeneralNode(
                    title='epistle_to_augustus_advertisement',
                    text=line
                ))
            elif current_state == "in_to_augustus_poem":
                current_line_num += 1
                scriblerus_data['epistle_to_augustus'].append(nodes.PoemNode(
                    book_number=6,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_second_horatian_epistle":
                current_line_num += 1
                scriblerus_data['second_horatian_epistle'].append(nodes.PoemNode(
                    book_number=7,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_donne_satire_two":
                current_line_num += 1
                scriblerus_data['donne_satire_two'].append(nodes.PoemNode(
                    book_number=8,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_donne_satire_four":
                current_line_num += 1
                scriblerus_data['donne_satire_four'].append(nodes.PoemNode(
                    book_number=9,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_epilogue_dialogue_one":
                # if len(line) < 1 or current_line_num < 2: # this line num check is based on text / convenience of scrape gates
                #     continue
                current_line_num += 1
                scriblerus_data['epilogue_dialogue_one'].append(nodes.PoemNode(
                    book_number=10,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_epilogue_dialogue_two":
                current_line_num += 1
                scriblerus_data['epilogue_dialogue_two'].append(nodes.PoemNode(
                    book_number=11,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_volune_end":
                return scriblerus_data

    # results =  {
    #     'epistles_satires': {
    #         'epistle_to_cobham_intro': scriblerus_data['epistle_to_cobham_intro'],
    #         'epistle_to_cobham': scriblerus_data['epistle_to_cobham'],
    #         'epistle_to_a_lady': scriblerus_data['epistle_to_a_lady'],
    #         'epistle_to_bathurst_intro': scriblerus_data['epistle_to_bathurst_intro'],
    #         'epistle_to_bathurst': scriblerus_data['epistle_to_bathurst'],
    #         'epistle_to_burlington_intro': scriblerus_data['epistle_to_burlington_intro'],
    #         'epistle_to_burlington': scriblerus_data['epistle_to_burlington'],
    #         'epistle_to_addison': scriblerus_data['epistle_to_addison'],
    #         'epistle_to_arbuthnot_intro': scriblerus_data['epistle_to_arbuthnot_intro'],
    #         'epistle_to_arbuthnot': scriblerus_data['epistle_to_arbuthnot'],
    #         'horatian_satires_advertisement': scriblerus_data['horatian_satires_advertisement'],
    #         'epistle_to_fortescue': scriblerus_data['epistle_to_fortescue'],
    #         'epistle_to_bethel': scriblerus_data['epistle_to_bethel'],
    #         'epistle_to_bolingbroke': scriblerus_data['epistle_to_bolingbroke'],
    #         'epistle_to_murray': scriblerus_data['epistle_to_murray'],
    #         'epistle_to_augustus_advertisement': scriblerus_data['epistle_to_augustus_advertisement'],
    #         'epistle_to_augustus': scriblerus_data['epistle_to_augustus'],
    #         'second_horatian_epistle': scriblerus_data['second_horatian_epistle'],
    #         'donne_satire_two': scriblerus_data['donne_satire_two'],
    #         'donne_satire_four': scriblerus_data['donne_satire_four'],
    #         'epilogue_dialogue_one': scriblerus_data['epilogue_dialogue_one'],
    #         'epilogue_dialogue_two': scriblerus_data['epilogue_dialogue_two'],
    #     }
    # }
    # return results['epistles_satires']
    return scriblerus_data
    








