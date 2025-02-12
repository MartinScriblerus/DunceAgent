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

async def scraper_gulliver(divs, sent_tokenize):
    start = time.time()
    print("in gulliver -> scrape")
    global sents
    sents = []
    global current_state
    current_state = 'in_publisher_to_reader'
    global current_line_num
    current_line_num = 0
    global chapter_num 
    chapter_num = 1
    global part_num
    part_num = 1
    global part_title
    part_title = ''
    global do_get_part_title
    do_get_part_title = False
    global scrape_ready
    scrape_ready = False
    global chapter_title
    global do_get_chapter_title
    chapter_title = ''
    do_get_chapter_title = False
    global scriblerus_data
    scriblerus_data = {
        'publisher_to_reader': [],
        'gulliver_to_sympson': [],
        'part_1': [],
        'part_2': [],
        'part_3': [],
        'part_4': [],
    }

    in_publisher_to_reader_pattern = r'As given in the original edition'
    letter_to_sympson_pattern = r'A LETTER FROM CAPTAIN GULLIVER TO HIS COUSIN SYMPSON.'
    global start_pattern
    start_pattern = r'THE PUBLISHER TO THE READER.'
    global end_pattern
    end_pattern = r'that they will not presume to come in my sight.'

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
            if do_get_chapter_title:
                do_get_chapter_title = False
                chapter_title = line
            if scrape_ready is False and re.findall(start_pattern, line):
                scrape_ready = True
            if scrape_ready is False:
                continue
            # line = re.sub(r'p\. \d+|\d+|[\[\](){}]|[\t]', '', line).strip()
            if len(line) < 1 or line == "." or scrape_ready is False:
                continue

            match = re.findall(r'PART I\.|PART II\.|PART III\.|PART IV\.', line)
            match_part1 = re.findall(r'A VOYAGE TO LILLIPUT.', line)
            match_part2 = re.findall(r'A VOYAGE TO BROBDINGNAG.', line)
            match_part3 = re.findall(r'A VOYAGE TO LAPUTA, BALNIBARBI, GLUBBDUBDRIB, LUGGNAGG AND JAPAN.', line)
            match_part4 = re.findall(r'A VOYAGE TO THE COUNTRY OF THE HOUYHNHNMS.', line)
            match_chapter = re.findall(r'CHAPTER (X{1,2}|IX|V?I{1,3}|IV|I{1,3})\.', line)
            


            if match_part1:
                do_get_part_title = True
                part_num = 1
                chapter_num=1
            if match_part2:
                do_get_part_title = True
                part_num = 2
                chapter_num=1
            if match_part3:
                do_get_part_title = True
                part_num = 3
                chapter_num=1
            if match_part4:
                do_get_part_title = True
                part_num = 4
                chapter_num=1
            
            if match:
                do_get_part_title = True
                part_num += 1
            if match_chapter:
                # chapter_num_unconverted = match.group(1)
                # chapter_num = roman_to_arabic(chapter_num_unconverted)
                do_get_chapter_title = True
                chapter_num += 1

            if do_get_part_title:
                do_get_part_title = False
                part_title = line

            in_publisher_to_reader_matcher = re.findall(in_publisher_to_reader_pattern, line)
            in_letter_to_sympson_matcher = re.findall(letter_to_sympson_pattern, line)
            end_sympson_matcher = re.findall(r'April 2, 1727', line)
            
            if in_publisher_to_reader_matcher:
                current_state = "in_publisher_to_reader"
            if in_letter_to_sympson_matcher:
                current_state = "in_letter_to_sympson"
            if end_sympson_matcher:               
                current_state="gulliver_text"


            if current_state == "gulliver_text":

                line = re.sub(r'p\. \d+|\d+|[\[\](){}]|[\t]', '', line).strip()
                if part_num == 1:
                    scriblerus_data['part_1'].append(nodes.GeneralNode(
                        title=f"chapter_{chapter_num}",
                        identifier=part_title + " / " + chapter_title,
                        text=line
                    ))
                elif part_num == 2:
                    scriblerus_data['part_2'].append(nodes.GeneralNode(
                        title=f"chapter_{chapter_num}",
                        identifier=part_title + " / " + chapter_title,
                        text=line
                    ))
                elif part_num == 3:
                    scriblerus_data['part_3'].append(nodes.GeneralNode(
                        title=f"chapter_{chapter_num}",
                        identifier=part_title + " / " + chapter_title,
                        text=line
                    ))
                elif part_num == 4:
                    scriblerus_data['part_4'].append(nodes.GeneralNode(
                        title=f"chapter_{chapter_num}",
                        identifier=part_title + " / " + chapter_title,
                        text=line
                    ))
            elif current_state == "in_publisher_to_reader":
                line = re.sub(r'p\. \d+|\d+|[\[\](){}]|[\t]', '', line).strip()
                scriblerus_data['publisher_to_reader'].append(nodes.GeneralNode(
                    title=f"publisher_to_reader",
                    identifier="publisher_to_reader",
                    text=line
                ))
            elif current_state == "in_letter_to_sympson":
                scriblerus_data['gulliver_to_sympson'].append(nodes.GeneralNode(
                    title=f"gulliver_to_sympson",
                    identifier="gulliver_to_sympson",
                    text=line
                ))
            
            if re.findall(end_pattern, line):
                return scriblerus_data
    results = {
        'gulliver_data': scriblerus_data
    }
    return results