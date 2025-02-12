import json
import pprint
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

# @profile
async def scraper_memoirs_scriblerus(divs, sent_tokenize):
    start = time.time()
    print("in scrib memoirs -> scrape")
    global scriblerus_data
    scriblerus_data = {
        'memoirs': []
    }
    
    chapter_starter = r"\bCHAP\.\s+[IVXLCDM]+\b"
    chapter_regex = r"\bCHAP\.\s+([IVXLCDM]+)\b"
    chapter_title_matcher = r"\b(?:[A-Z']+\s+)+(?:[A-Z']+)\b"
    curr_title = None
    curr_chapter = 0
    for div in divs:
        content_text = await div.inner_text()
        soup_memoirs_unparsed = BeautifulSoup(content_text, "html.parser")
        soup_memoirs = soup_memoirs_unparsed.get_text()
        soup_memoirs = re.sub(r'\s+', ' ', soup_memoirs).strip()

        lines = sent_tokenize(soup_memoirs)
        # entities = ner_pipeline(lines)
        # sentiment = sentiment_pipeline(lines)
        for idx, line in enumerate(lines):
            current_entity = ""
            entity_type = None
            current_label = None

            
            if re.findall(chapter_starter, soup_memoirs):
                curr_title = re.findall(chapter_title_matcher, soup_memoirs)
                curr_rom_num = re.findall(chapter_regex, soup_memoirs)
                chap_num = await roman_to_arabic(curr_rom_num[0])

                curr_chapter = chap_num
            if re.findall(r'END OF THE PROJECT GUTENBERG EBOOK', line):
                continue
            line = re.sub(r'PAGE \[UNNUMBERED\]', '', line)
            line = re.sub(r'PAGE \d+\.', '', line)
            line = re.sub(r'[|/\\]', '', line)

            scriblerus_data['memoirs'].append(nodes.ChapterProseNode(
                id=idx,
                chapter_number=curr_chapter,
                subtitle=" ".join(curr_title).strip() if curr_title is not None else None,
                text=line,
                annotation=''
            ))
    print(f"Elapsed time for Memoirs of Martinus Scriblerus: {time.time() - start} seconds")
    
    return scriblerus_data['memoirs']