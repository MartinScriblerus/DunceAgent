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

async def scraper_tale_of_a_tub(divs, sent_tokenize):
    start = time.time()
    print("in tale of a tub -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global section_num 
    section_num = 0
    global scrape_ready
    scrape_ready = False
    global section_title
    global do_get_section_title
    section_title = ''
    do_get_section_title = False
    global scriblerus_data
    scriblerus_data = {
        'section_1': [],
        'section_2': [],
        'section_3': [],
        'section_4': [],
        'section_5': [],
        'section_6': [],
        'section_7': [],
        'section_8': [],
        'section_9': [],
        'section_10': [],
        'section_11': [],
        'conclusion': [],
        'the_history_of_martin': [],
        'universal_benefit': [],
    }

    in_conclusion_pattern = r'THE CONCLUSION.'
    in_history_of_martin_pattern = r'THE HISTORY OF MARTIN.'
    start_pattern = r'ORIGINAL ADVERTISEMENT.'


    for div in divs:
        content_text = await div.inner_text()
        soup_swiftworks_unparsed = BeautifulSoup(content_text, "html.parser")

        soup_swiftworks = soup_swiftworks_unparsed.get_text()
        
        all_sents = sent_tokenize(soup_swiftworks, "english")
        for s in all_sents:
            sents.append(s)

    for sent in sents:
        lines = re.split(r'\n', sent)
        for line in lines:
            if scrape_ready is False and re.findall(start_pattern, line):
                scrape_ready = True
            line = re.sub(r'p\. \d+|\d+|[\[\](){}]|[\t]', '', line).strip()
            if len(line) < 1 or line == "." or scrape_ready is False:
                continue

            match = re.findall(r'Section (\w+)', line, re.IGNORECASE)

            if do_get_section_title:
                do_get_section_title = False
                section_title = line
                # continue

            if match:
                # section_num_unconverted = match.group(1)
                # section_num = roman_to_arabic(section_num_unconverted)
                do_get_section_title = True
                section_num += 1
                # continue

            in_conclusion_matcher = re.findall(in_conclusion_pattern, line)

            if in_conclusion_matcher:
                current_state = "in_conclusion"

            in_universal_benefit_pattern = re.findall(r'PROJECT FOR THE UNIVERSAL BENEFIT OF MANKIND.', str(line))
            if in_universal_benefit_pattern:
                current_state = "in_universal_benefit"

            in_history_of_martin_matcher = re.findall(in_history_of_martin_pattern, line)
            if in_history_of_martin_matcher:
                current_state = "in_history_of_martin"
               
                           
            if current_state == "":
                if section_num == 1:
                    scriblerus_data['section_1'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 2:
                    scriblerus_data['section_2'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 3:
                    scriblerus_data['section_3'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 4:
                    scriblerus_data['section_4'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 5:
                    scriblerus_data['section_5'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 6:
                    scriblerus_data['section_6'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 7:
                    scriblerus_data['section_7'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 8:
                    scriblerus_data['section_8'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 9:
                    scriblerus_data['section_9'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 10:
                    scriblerus_data['section_10'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))
                elif section_num == 11:
                    scriblerus_data['section_11'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier=f"section_{section_num}",
                        text=line
                    ))


            elif current_state == "in_conclusion":
                scriblerus_data['conclusion'].append(nodes.GeneralNode(
                        title=f"tale_of_a_tub",
                        identifier="conclusion",
                        text=line
                    ))
            elif current_state == "in_history_of_martin":
                scriblerus_data['the_history_of_martin'].append(nodes.GeneralNode(
                        title="tale_of_a_tub",
                        identifier="history of martin",
                        text=line
                    ))
            elif current_state == "in_universal_benefit":
                if re.findall(r'FOOTNOTES.', line):
                    current_state = "end"
                    continue
                scriblerus_data['universal_benefit'].append(nodes.GeneralNode(
                        title="tale_of_a_tub",
                        identifier="a project for the universal benefit of mankind",
                        text=line
                    ))
            
    # results = {
    #     'tale_of_a_tub_data': scriblerus_data
    # }
    return scriblerus_data