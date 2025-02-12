from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import time

import server.app.src.nodes as nodes

character_names=[
    'Player.', 
    'Beggar.', 
    'Filch.', 
    'Peachum.', 
    'Mrs. Peachum.',
    'Polly.',
    'Macheath.',
    'Ben.',
    'Matt.',
    'Jemmy.',
    'Crook.',
    'Wat.',
    'Robin.',
    'Ned.',
    'Harry.',
    'Chorus.',
    'Drawer,',
    'Jenny.',
    'Mrs. Coaxer.',
    'Mrs. Vixen.',
    'Brazen.',
    'Tawdry.',
    'Mrs. Slammekin.',
    'Trull.',
    'Lockit.',
    'Lucy.',
    'Servant.',
    'Mrs. Trapes.',
    'Jailor', #
    'All.' #
]

async def get_character(short_name):
    if short_name == character_names[0]:
        return "Player"
    elif short_name == character_names[1]:
        return "Beggar"
    elif short_name == character_names[2]:
        return "Filch"
    elif short_name == character_names[3]:
        return "Peachum"
    elif short_name == character_names[4]:
        return "Mrs. Peachum"
    elif short_name == character_names[5]:
        return "Polly"
    elif short_name == character_names[6]:
        return "Macheath"
    elif short_name == character_names[7]:
        return "Ben"
    elif short_name == character_names[8]:
        return "Matt"
    elif short_name == character_names[9]:
        return "Jemmy"
    elif short_name == character_names[10]:
        return "Crook"
    elif short_name == character_names[11]:
        return "Wat"
    elif short_name == character_names[12]:
        return "Robin"
    elif short_name == character_names[13]:
        return "Ned"
    elif short_name == character_names[14]:
        return "Harry"
    
    elif short_name == character_names[15]:
        return "Chorus"
    elif short_name == character_names[16]:
        return "Drawer"
    elif short_name == character_names[17]:
        return "Jenny"
    elif short_name == character_names[18]:
        return "Mrs. Coaxer"
    elif short_name == character_names[19]:
        return "Mrs. Vixen"
    elif short_name == character_names[20]:
        return "Brazen"
    elif short_name == character_names[21]:
        return "Tawdry"
    elif short_name == character_names[22]:
        return "Mrs. Slammekin"
    elif short_name == character_names[23]:
        return "Trull"
    elif short_name == character_names[24]:
        return "Lockit"
    elif short_name == character_names[25]:
        return "Lucy"
    elif short_name == character_names[26]:
        return "Servant"
    elif short_name == character_names[27]:
        return "Mrs. Trapes"
    elif short_name == character_names[28]:
        return "Jailor"
    elif short_name == character_names[29]:
        return "All"
    else: 
        return short_name

character_fullnames = [
    "Player", 
    "Beggar", 
    "Filch", 
    "Peachum", 
    "Mrs. Peachum", 
    "Polly", 
    "Macheath", 
    "Ben", 
    "Matt", 
    "Jemmy", 
    "Crook", 
    "Wat", 
    "Robin", 
    "Ned", 
    "Harry", 
    "Chorus", 
    "Drawer", 
    "Jenny", 
    "Mrs. Coaxer", 
    "Mrs. Vixen", 
    "Brazen", 
    "Tawdry", 
    "Mrs. Slammekin", 
    "Trull", 
    "Lockit", 
    "Lucy", 
    "Servant", 
    "Mrs. Trapes", 
    "Jailor", 
    "All"
]

match_pattern_full_names = r'\b(' + '|'.join(map(re.escape, character_fullnames)) + r')\b'

match_pattern_exit = r'\bexit\b'  

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
        'XXV': 25, 
        'XXVI': 26, 
        'XXVII': 27,
        'XXVIII': 28, 
        'XXIX': 29,
        'XXX': 30, 
        'XXXI': 31, 
        'XXXII': 32,
        'XXXIII': 33, 
        'XXXIV': 34,
        'XXXV': 35, 
        'XXXVI': 36, 
        'XXXVII': 37,
        'XXXVIII': 38, 
        'XXXIX': 39,
        'XL': 40, 
        'XLI': 41, 
        'XLII': 42, 
        'XLIII': 43,
        'XLIV': 44,
        'XLV': 45, 
        'XLVI': 46, 
        'XLVII': 47,
        'XLVIII': 48, 
        'XLIX': 49,
        'L': 50, 
        'LI': 51, 
        'LII': 52, 
        'LIII': 53,
        'LIV': 54,
        'LV': 55, 
        'LVI': 56, 
        'LVII': 57,
        'LVIII': 58, 
        'LIX': 59,
        'LX': 60, 
        'LXI': 61, 
        'LXII': 62, 
        'LXIII': 63,
        'LXIV': 64,
        'LXV': 65, 
        'LXVI': 66, 
        'LXVII': 67,
        'LXVIII': 68, 
    }
    if roman in roman_values.keys():
        arabic_num = roman_values[roman]
    else:
        arabic_num = roman
    return arabic_num

async def scraper_beggars_opera(divs, sent_tokenize):
    start = time.time()
    print("in beggar's opera -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global characters_present 
    characters_present = []
    global scriblerus_data
    scriblerus_data = {
        "beggars_opera": []
    }
    global current_act
    current_act = 0
    global current_scene
    current_scene = 0
    global current_air
    current_air = 0
    global current_air_name
    current_air_name = ''
    global current_speaker
    current_speaker = ''
    global is_stage_direction
    is_stage_direction = False

    beggars_opera_start_pattern = r'If Poverty be a Title to Poetry'
    new_act_pattern = r'ACT ([IVXLCDM]+)\.'
    new_scene_pattern = r'SCENE ([IVXLCDM]+)\.'
    new_air_pattern = r'([IVXLCDM]+)\.'
    new_air_name_pattern = r'([IVXLCDM]+)\.\s*(.*?)(?=\.)'
    epilogue_pattern = r'Epilogue'
    end_pattern=r'END OF THE PROJECT GUTENBERG EBOOK'
    character_names_pattern=r"[\w\s]+\.?"

    global play_ready
    play_ready = False
    global play_done
    play_done = False

    for div in divs:
        content_text = await div.inner_text()
        soup_three_hours_unparsed = BeautifulSoup(content_text, "html.parser")
        soup_three_hours = soup_three_hours_unparsed.get_text()

        all_sents = sent_tokenize(soup_three_hours, "english")
        for s in all_sents:
            sents.append(s)
        
        # soup_three_hours = re.sub(r'\s+', ' ', soup_three_hours).strip()
        for id, sent in enumerate(sents):
            if play_done is True:
                return scriblerus_data           
            is_exit = re.findall(match_pattern_exit, re.sub(r'.','',sent).strip())
            if is_exit:
                chars_to_remove = re.findall(match_pattern_full_names, sent)
                for i in chars_to_remove:
                    if i in characters_present:
                        characters_present.remove(i)

            match_start = re.findall(beggars_opera_start_pattern, sent)
            if match_start:
                play_ready = True            
            if play_ready is not True:
                continue
            match_stage_direction = re.findall(r'\[', sent)
            # Check whether the token matches any character name pattern
            match_speaker = re.search(character_names_pattern, sent)
            if match_speaker:
                is_stage_direction = False
                name = match_speaker.group().strip(",")
                # Check whether the cleaned name matches one of the character names (without trailing punctuation)
                if name == "Mrs.":
                    current_speaker = ''.join(re.findall(character_names_pattern, sent))
                elif any(name.strip(".") in n for n in character_names):
                    current_speaker = name
                char = await get_character(current_speaker)
                if char not in characters_present:
                    characters_present.append(char)
            match_new_act = re.findall(new_act_pattern, sent)
            if match_new_act:
                characters_present = []
                current_act = await roman_to_arabic(match_new_act[0])
            match_new_scene = re.findall(new_scene_pattern, sent)
            if match_new_scene:
                characters_present = []
                current_scene = await roman_to_arabic(match_new_scene[0])
            match_new_air = re.findall(new_air_pattern, sent)
            if match_new_air:
                current_air = await roman_to_arabic(match_new_air[0])
            match_new_air_name = re.findall(new_air_name_pattern, sent)
            if match_new_air_name:
                current_air = await roman_to_arabic(match_new_air[0])
            if match_stage_direction:
                is_stage_direction = True
            match_end = re.findall(end_pattern, sent)
            if match_end:
                play_done = True
                characters_present = []
                continue
            if sent and play_done is False:
    
                scriblerus_data["beggars_opera"].append(nodes.PlayNode(
                    id=id or None,
                    act_number=current_act,
                    scene_number=current_scene,
                    speaker=await get_character(current_speaker),
                    characters_present=characters_present,
                    line=sent,
                    is_stage_direction=is_stage_direction
                ))
    results = {
        "beggars_opera": scriblerus_data["beggars_opera"]
    }
    return results