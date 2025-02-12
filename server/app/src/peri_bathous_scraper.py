import json
from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import server.app.src.nodes as nodes
import time
import asyncio 
from concurrent.futures import ThreadPoolExecutor
from datasets import load_dataset

executor = ThreadPoolExecutor()

# Define your async function
async def async_re_find(pattern, text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, re.findall, pattern, text)

async def async_re_sub(pattern, repl, text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, re.sub, pattern, repl, text)

pos_tag_helper = {
    'CC':'coordinating conjunction',
    'CD':'cardinal number',
    'DT':'determiner',
    'EX':'existential there',
    'FW':'foreign word',
    'IN':'preposition or subordinating conjunction',
    'JJ':'adjective',
    'JJR':'adjective, comparative',
    'JJS':'adjective, superlative',
    'LS':'list item marker',
    'MD':'medium or moderately',
    'NN':'noun, singular or mass',
    'NNS':'noun, plural',
    'NNP':'proper noun, singular',
    'NNPS':'proper noun, plural',
    'PDT':'predeterminer',
    'POS':'possessive ending',
    'PRP': 'personal pronoun',
    'PRP$':'possessive pronoun',
    'RB': 'adverb',
    'RBR': 'adverb, comparative',
    'RBS':'adverb, superlative',
    'RP': 'particle',
    'SYM': 'symbol',
    'TO':'to',
    'UH':'interjection',
    'VB': 'verb, base form',
    'VBD':'verb, past tense',
    'VBG':'verb, gerund or present participle',
    'VBN':'verb, past participle',
    'VBP':'verb, non-3rd person singular present',
    'VBZ':'verb, 3rd person singular present',
    'WDT': 'WH-determiner', #that what whatever which whichever
    'WP': 'who', #that what whatever whatsoever which who whom whosoever
    'WP$': 'possessive wh-pronoun',
    'WRB': 'wh-adverb' #that what whatever which whichever
    }

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
async def scraper_peri_bathous(divs, sent_tokenize):
    start = time.time()
    global scriblerus_data
    scriblerus_data = {
        'peri_bathous': [],
    }
    global current_chapter_peri_bathous
    global current_subtitle_peri_bathous
    global current_entity
    global human_readable_entities
    global in_endnotes
    global pattern_match_begin_endnotes
    pattern_match_begin_endnotes = r'Mediocribus'
    in_endnotes = False
    human_readable_entities = []
    current_entity = ''
    current_chapter_peri_bathous = 1
    current_subtitle_peri_bathous=''
    
    pattern_match_new_pb_chapter = r'CHAP\.\s+([IVXLCDM]+)'
    get_endnote_pattern = r'\[(\d+)\]'
    
    get_subtitle = False
    curr_subtitle = "Introduction"
    print("in peri bathous -> scrape")
    
    global gather_endnotes_array
    gather_endnotes_array = []
    
    for idx, div in enumerate(divs):
        content_text = await div.inner_text()
        soup_peri_bathous_unparsed = BeautifulSoup(content_text, "html.parser")
        soup_peri_bathous = soup_peri_bathous_unparsed.get_text()

        soup_peri_bathous = await async_re_sub(r'\s+', ' ', soup_peri_bathous)
        soup_peri_bathous = await async_re_sub(r'While this work is included within The Works of the Rev. Jonathan Swift and is not attributed to anyone other than Jonathan Swift, it may have been written by another member of the Scriblerus Club. The club, which was founded in 1714, included Jonathan Swift, Alexander Pope, John Gay, John Arbuthnot, Henry St John, and Thomas Parnell. See the note regarding this poem in a letter from Benjamin Motte to Jonathan Swift attributing this poem to Alexander Pope.', '', soup_peri_bathous)

        if len(str(soup_peri_bathous).strip()) < 1:
            continue

        if get_subtitle is True:
            get_subtitle = False
            curr_subtitle = soup_peri_bathous

        match = await async_re_find(pattern_match_new_pb_chapter, soup_peri_bathous)
        match_endnotes = await async_re_find(pattern_match_begin_endnotes, soup_peri_bathous)
        if match_endnotes:
            in_endnotes = True
        if match:
            if len(match) > 0:
                current_chapter_peri_bathous=await roman_to_arabic(match[0])
            get_subtitle = True

        lines = sent_tokenize(soup_peri_bathous)
        
        edited_lines = async_re_find(r'CHAP\.\s([IVX]{1,4})', lines)
        chapter_header_to_remove = async_re_find(r'CHAP', lines)
        rom_pat = r'\b(I{1,3}|IV|V?I{0,3}|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX|XXI|XXII|XXIII|XXIV)\b'
        found_edited_lines = async_re_find(rom_pat, edited_lines)
        
        if found_edited_lines or chapter_header_to_remove:
            continue

        if in_endnotes is True:
            gather_endnotes_array.append(lines)
        
        concatenated_lines = []
        for inner_idx, line in enumerate(lines):

            # Initialize variables for processing tokens
            current_entity = ""
            # edited_lines = re.findall(r'CHAP\.\s([IVX]{1,4})', line)
            rom_pat = r'\b(I{1,3}|IV|V?I{0,3}|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX|XXI|XXII|XXIII|XXIV)\b'
            found_edited_lines = async_re_find(rom_pat, line)

            if found_edited_lines:
                continue
            concatenated_lines.append(await async_re_sub(get_endnote_pattern, "", edited_lines))
            human_readable_entities = []

 

        scriblerus_data["peri_bathous"].append(
            nodes.ChapterProseNode(
                id=f"{idx}",
                chapter_number=current_chapter_peri_bathous,
                subtitle=curr_subtitle.strip(),
                text=" ".join(concatenated_lines),
                annotation=''
            )
        )
        concatenated_lines = [] 

        all_endnotes = " ".join(gather_endnotes_array)
        gather_endnotes_array = []
        matches = await async_re_find(r"(\d{1,3})\.\s+(.*?)(?=\d{1,3}\.\s+|$)", all_endnotes)
        print("WTF!>!>!> MATCHES ", matches)
        pb_endnotes_hash = {f"[{num}]": content for num, content in matches}
        print("ENDNOTE HASH: ", pb_endnotes_hash)
    for idx, i in enumerate(scriblerus_data['peri_bathous']):
        note_key = await async_re_find(get_endnote_pattern, i.text)
        if note_key or len(note_key) < 1: 
            continue
        clean_text = await async_re_sub(get_endnote_pattern, "", i.text)
        print("test string-- ", f"[{int(note_key[0])}]", "NOTE KEY: ", note_key, "TEXT: ", clean_text)
        # if len(note_key) > 0:
        i['annotation'] = pb_endnotes_hash.get(note_key[0])
        i['text'] = clean_text or i.text
        # scriblerus_data['peri_bathous'][idx]['annotation'].append(i['annotation'])
        print("annotation is -- ", i['annotation'], "text is -- ", i['text'])
    print(f"Elapsed time in Art of Sinking: {time.time() - start} seconds")
    # serialized_data = [node for node in scriblerus_data]
    return scriblerus_data['peri_bathous']
