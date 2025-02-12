from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import time

import server.app.src.nodes as nodes

# def roman_to_arabic(roman):
#     roman_values = {
#         'I': 1, 
#         'II': 2, 
#         'III': 3, 
#         'IV': 4, 
#         'V': 5, 
#         'VI': 6, 
#         'VII': 7,
#         'VIII': 8, 
#         'IX': 9, 
#         'X': 10, 
#         'XI': 11, 
#         'XII': 12,
#         'XIII': 13, 
#         'XIV': 14, 
#         'XV': 15, 
#         'XVI': 16, 
#         'XVII': 17,
#         'XVIII': 18, 
#         'XIX': 19, 
#         'XX': 20, 
#         'XXI': 21, 
#         'XXII': 22,
#         'XXIII': 23, 
#         'XXIV': 24, 
#     }
#     arabic_num = roman_values[roman]
#     return arabic_num

async def scraper_volume_one(divs, sent_tokenize):
    start = time.time()
    print("in volume one -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global scriblerus_data
    scriblerus_data = {
        "temple_of_fame_intro": [],
        "temple_of_fame_poem": [],
        "pastorals_intro": [],
        "discourse_on_pastorals": [],
        "pastorals_poems_spring": [],
        "pastorals_poems_summer": [],
        "pastorals_poems_autumn": [],
        "pastorals_poems_winter": [],
        "messiah_intro": [],
        "messiah_poem": [],
        "windsor_forest_intro": [],
        "windsor_forest_poem": [],
    }

    #PATTERN MATCHERS HERE
    temple_of_fame_intro_pattern = r'The hint of the following'
    temple_of_fame_poem_pattern = r'In that soft season'
    temple_of_fame_end_pattern = r'or grant me none'
    pastorals_intro_pattern = r'WRITTEN IN THE YEAR 1704'
    pastorals_intro_end_pattern = r'he showed his face in the'
    discourse_on_pastorals_pattern = r'a greater number of any sort of verses than'
    discourse_on_pastorals_end_pattern = r'have not wanted care to imitate'
    pastorals_spring_pattern = r'First in these fields I try'
    pastorals_spring_end_pattern = r'And from the Pleiads'
    pastorals_summer_pattern = r'he seeks no better name'
    pastorals_summer_end_pattern = r'By night he scorches'
    pastorals_autumn_pattern = r'Beneath the shade a spreading'
    pastorals_autumn_end_pattern = r'And the low sun had lengthened'
    pastorals_winter_pattern = r'THE FOURTH PASTORAL'
    pastorals_winter_end_pattern = r'And from the Pleiads'
    messiah_intro_pattern = r'Ye Nymphs of Solyma'
    messiah_poem_pattern = r'thy own Messiah reigns'
    messiah_poem_end_pattern = r'classed by Pope among his Pastorals'
    windsor_forest_intro_pattern = r'To the Right Honourable George'
    windsor_forest_intro_end_pattern = r'numerous verse was extinct'
    windsor_forest_poem_pattern = r'GEORGE LORD LANSDOWN'
    windsor_forest_poem_end_pattern=r'fields I sung the sylvan strains'

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
            line = line.strip()
            if len(line) < 1:
                continue
            # print("what the fuck / line: ", line)
            in_tof_intro_match = re.findall(temple_of_fame_intro_pattern, line)
            in_tof_poem_match = re.findall(temple_of_fame_poem_pattern, line)
            in_tof_end_poem_match = re.findall(temple_of_fame_end_pattern, line)
            in_pastorals_intro_match = re.findall(pastorals_intro_pattern, line)
            in_pastorals_intro_end_match = re.findall(pastorals_intro_end_pattern, line)
            in_discourse_on_pastorals_match = re.findall(discourse_on_pastorals_pattern, line)
            in_discourse_on_pastorals_end_match = re.findall(discourse_on_pastorals_end_pattern, line)
            in_pastorals_spring_match = re.findall(pastorals_spring_pattern, line)
            in_pastorals_spring_end_match = re.findall(pastorals_spring_end_pattern, line)
            in_pastorals_summer_match = re.findall(pastorals_summer_pattern, line)
            in_pastorals_summer_end_match = re.findall(pastorals_summer_end_pattern, line)
            in_pastorals_autumn_match = re.findall(pastorals_autumn_pattern, line)
            in_pastorals_autumn_end_match = re.findall(pastorals_autumn_end_pattern, line)
            in_pastorals_winter_match = re.findall(pastorals_winter_pattern, line, re.IGNORECASE)
            in_pastorals_winter_end_match = re.findall(pastorals_winter_end_pattern, line)
            in_messiah_intro_match = re.findall(messiah_intro_pattern, line)
            in_messiah_poem_match = re.findall(messiah_poem_pattern, line)
            in_messiah_poem_end_match = re.findall(messiah_poem_end_pattern, line)
            in_winsor_forest_intro_match = re.findall(windsor_forest_intro_pattern, line, re.IGNORECASE)
            in_windsor_forest_intro_end_match = re.findall(windsor_forest_intro_end_pattern, line)
            in_windsor_forest_poem_match = re.findall(windsor_forest_poem_pattern, line)
            in_windsor_forest_poem_end_match = re.findall(windsor_forest_poem_end_pattern, line)


            if in_tof_intro_match:
                current_state = "in_tof_intro_match"
            elif in_tof_poem_match:
                current_state = "in_tof_poem_match"
            elif in_tof_end_poem_match:
                current_state = "in_tof_end_poem_match"
            elif in_pastorals_intro_match:
                current_state = "in_pastorals_intro_match"
            elif in_pastorals_intro_end_match:
                current_state = "in_pastorals_intro_end_match"
            elif in_discourse_on_pastorals_match:
                current_state = "in_discourse_on_pastorals_match"
            elif in_discourse_on_pastorals_end_match:
                current_state = "in_discourse_on_pastorals_end_match"
            elif in_pastorals_spring_match:
                current_state = "in_pastorals_spring_match"
            elif in_pastorals_spring_end_match:
                current_state = "in_pastorals_spring_end_match"
            elif in_pastorals_summer_match:
                current_state = "in_pastorals_summer_match"
            elif in_pastorals_summer_end_match:
                current_state = "in_pastorals_summer_end_match"
            elif in_pastorals_autumn_match:
                current_state = "in_pastorals_autumn_match"
            elif in_pastorals_autumn_end_match:
                current_state = "in_pastorals_autumn_end_match"
            elif in_pastorals_winter_match:
                current_state = "in_pastorals_winter_match"
            elif in_pastorals_winter_end_match:
                current_state = "in_pastorals_winter_end_match"
            elif in_messiah_intro_match:
                current_state = "in_messiah_intro_match"
            elif in_messiah_poem_match:
                current_state = "in_messiah_poem_match"
            elif in_messiah_poem_end_match:
                current_state = "in_messiah_poem_end_match"
            elif in_winsor_forest_intro_match:
                current_state = "in_winsor_forest_intro_match"
            elif in_windsor_forest_intro_end_match:
                current_state = "in_windsor_forest_intro_end_match"
            elif in_windsor_forest_poem_match:
                current_state = "in_windsor_forest_poem_match"
            elif in_windsor_forest_poem_end_match:
                current_state = 'in_windsor_forest_poem_end_match'
                # break
            else: 
                continue
       
            if current_state == "in_tof_intro_match":
                scriblerus_data["temple_of_fame_intro"].append(nodes.ShortGeneralNode(
                    title='temple_of_fame_intro',
                    text=line
                ))
            elif current_state == "in_tof_poem_match":
                current_line_num +=1
                scriblerus_data['temple_of_fame_poem'].append(nodes.PoemNode(
                    book_number=1,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_pastorals_intro_match":
                current_line_num +=1
                scriblerus_data['pastorals_intro'].append(nodes.ShortGeneralNode(
                    title='pastorals_intro',
                    text=line
                ))
            elif current_state == "in_discourse_on_pastorals_match":
                scriblerus_data['discourse_on_pastorals'].append(nodes.ShortGeneralNode(
                    title='discourse_on_pastorals',
                    text=line
                ))
            elif current_state == "in_pastorals_spring_match":
                current_line_num +=1
                scriblerus_data['pastorals_poems_spring'].append(nodes.PoemNode(
                    book_number=1,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_pastorals_summer_match":
                scriblerus_data['pastorals_poems_summer'].append(nodes.PoemNode(
                    book_number=2,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_pastorals_autumn_match":
                scriblerus_data['pastorals_poems_autumn'].append(nodes.PoemNode(
                    book_number=3,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_pastorals_winter_match":
                current_line_num +=1
                scriblerus_data['pastorals_poems_winter'].append(nodes.PoemNode(
                    book_number=4,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_messiah_intro_match":
                scriblerus_data['messiah_intro'].append(nodes.ShortGeneralNode(
                    title="messiah_intro",
                    text=line
                ))
            elif current_state == "in_messiah_poem_match":
                current_line_num +=1
                scriblerus_data['messiah_poem'].append(nodes.PoemNode(
                    book_number=5,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_windsor_forest_intro_match":
                scriblerus_data['windsor_forest_"intro'].append(nodes.ShortGeneralNode(
                    title='windsor_forest_intro_match',
                    text=line
                ))
            elif current_state == "in_windsor_forest_poem_match":
                current_line_num +=1
                scriblerus_data['windsor_forest_poem'].append(nodes.PoemNode(
                    book_number=1,
                    line_number=current_line_num,
                    line=line
                ))
            elif current_state == "in_windsor_forest_poem_end_match":
                return scriblerus_data
            else:
                continue  
    
    # results = {
    #     "volume_one": {
    #         "temple_of_fame_intro": scriblerus_data["temple_of_fame_intro"],
    #         # "temple_of_fame_poem": scriblerus_data["temple_of_fame_poem"],
    #         # "pastorals_intro": scriblerus_data["pastorals_intro"],
    #         # "discourse_on_pastorals": scriblerus_data["discourse_on_pastorals"],
    #         # "pastorals_poems_spring": scriblerus_data["pastorals_poems_spring"],
    #         # "pastorals_poems_summer": scriblerus_data["pastorals_poems_summer"],
    #         # "pastorals_poems_autumn": scriblerus_data["pastorals_poems_autumn"],
    #         # "pastorals_poems_winter": scriblerus_data["pastorals_poems_winter"],
    #         # "messiah_intro": scriblerus_data["messiah_intro"],
    #         # "messiah_poem": scriblerus_data["messiah_poem"],
    #         # "windsor_forest_intro": scriblerus_data["windsor_forest_intro"],
    #         # "windsor_forest_poem": scriblerus_data["windsor_forest_poem"],
    #     }
    # }           
    return scriblerus_data