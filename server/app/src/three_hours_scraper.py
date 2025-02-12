from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import server.app.src.nodes as nodes
import time

character_names=[
    'Foss.', 
    'Town.', 
    'Serv.', 
    'Clink.', 
    'Maid',
    'Boy.',
    'Ptis.',
    '1st Play.',
    'Sir Trem.',
    'Plot.',
    'Plotw.',
    '2d Play.',
    'Sars.',
    'Within.',
    'Old Wom.',
    'Fos.',
    'Fossile,',
    'Foot.',
    'Underp.',
    'Hugh.',
    '1st Wom.',
    '2d Wom.',
    '3d Wom.',
    'Naut.',
    'Pos.',
    'Poss.',
    'Prue.',
    'Sail.',
    'Fossile.',
]

character_fullnames = [
    "Fossile",
    "Townley",
    "Servant",
    "Clinket",
    "Maid",
    "Boy",
    "Ptisan",
    "First Player",
    "Sir Tremendous",
    "Plotwell",
    "Second Player",
    "Sarsnet",
    "Within",
    "Old Woman",
    "Footman",
    "Underplot",
    "Hugh",
    "First Woman"
    "Second Woman"
    "Third Woman"
    "Nautilus",
    "Prue",
    "Sailor",
]

match_pattern_full_names = r'\b(' + '|'.join(map(re.escape, character_fullnames)) + r')\b'

match_pattern_exit = r'\bexit\b'

async def get_character(short_name):
    if short_name == character_names[0]:
        return "Fossile"
    elif short_name == character_names[1]:
        return "Townley"
    elif short_name == character_names[2]:
        return "Servant"
    elif short_name == character_names[3]:
        return "Clinket"
    elif short_name == character_names[4]:
        return "Maid"
    elif short_name == character_names[5]:
        return "Boy"
    elif short_name == character_names[6]:
        return "Ptisan"
    elif short_name == character_names[7]:
        return "First Player"
    elif short_name == character_names[8]:
        return "Sir Tremendous"
    elif short_name == character_names[9]:
        return "Plotwell"
    elif short_name == character_names[10]:
        return "Plotwell"
    elif short_name == character_names[11]:
        return "Second Player"
    elif short_name == character_names[12]:
        return "Sarsnet"
    elif short_name == character_names[13]:
        return "Within"
    elif short_name == character_names[14]:
        return "Old Woman"
    
    elif short_name == character_names[15]:
        return "Fossile"
    elif short_name == character_names[16]:
        return "Fossile"
    elif short_name == character_names[17]:
        return "Footman"
    elif short_name == character_names[18]:
        return "Underplot"
    elif short_name == character_names[19]:
        return "Hugh"
    elif short_name == character_names[20]:
        return "First Woman"
    elif short_name == character_names[21]:
        return "Second Woman"
    elif short_name == character_names[22]:
        return "Third Woman"
    elif short_name == character_names[23]:
        return "Nautilus"
    elif short_name == character_names[24]:
        return "Fossile"
    elif short_name == character_names[25]:
        return "Fossile"
    elif short_name == character_names[26]:
        return "Prue"
    elif short_name == character_names[27]:
        return "Sailor"
    elif short_name == character_names[27]:
        return "Fossile"
    else:
        return None
    

async def rom_num_converter(rom_num):
    if rom_num == "I": 
        return 1
    if rom_num == "II": 
        return 2
    if rom_num == "III": 
        return 3
    if rom_num == "IV": 
        return 4
    if rom_num == "V": 
        return 5
    else:
        return 0 

# @profile
async def scraper_three_hours(divs, sent_tokenize):
    start = time.time() 
    global scriblerus_data
    scriblerus_data = {
        "three_hours_harrington_intro": [],
        "three_hours_prologue": [],
        "three_hours_dramatic_personae": [],
        "three_hours_play": [],
        "three_hours_key_to_marriage": [],
        "three_hours_letter_to_publisher": [],
    }
    global current_state
    current_state=''
    global current_act
    current_act = 0
    global current_speaker
    current_speaker = ''
    global is_stage_direction
    is_stage_direction = False
    global sents
    sents = []
    global characters_present
    characters_present = []
    global scrape_ready
    scrape_ready = False



    three_hours_editors_intro_pattern = r'It is a privilege'
    end_intro_pattern = r'Dashenka in The Cherry Orchard.'
    prologue_pattern = r'Spoke by Mr. Wilks.'
    dramatic_personae_pattern = r'Dramatis Personæ.'
    new_act_pattern = r'ACT ([IVXLCDM]+)'
    epilogue_pattern = r'Epilogue'
    key_to_marriage_pattern=r'To Sir H. M.'
    letter_to_publisher_pattern=r'To the Publisher.'
    end_pattern=r'PUBLICATIONS OF THE AUGUSTAN REPRINT SOCIETY'
    start_pattern = r'It is a privilege'
    character_names_pattern=r"[\w\s]+\.?"
    for div in divs:
        content_text = await div.inner_text()
        soup_three_hours_unparsed = BeautifulSoup(content_text, "html.parser")
        soup_three_hours = soup_three_hours_unparsed.get_text()


        all_sents = sent_tokenize(soup_three_hours, "english")
        for s in all_sents:
            sents.append(s)
        
        # soup_three_hours = re.sub(r'\s+', ' ', soup_three_hours).strip()
        for id, sent in enumerate(sents):
            if re.findall(match_pattern_exit, sent):
                chars_to_remove = re.findall(match_pattern_full_names, sent)
                for i in chars_to_remove:
                    if i in characters_present:
                        characters_present.remove(i)
            sent = re.sub(r'\n|\[\d+\]', '', sent)
            if re.findall(start_pattern, sent):
                sent = 'It is a privilege to have a part in this reprint of what is certainly one of the wittiest plays in the language, and one of the most neglected.'
                scrape_ready = True
            if scrape_ready is not True:
                continue
            in_editors_intro_matcher = re.findall(three_hours_editors_intro_pattern, sent)
            end_intro_matcher = re.findall(end_intro_pattern, sent)
            in_prologue_matcher = re.findall(prologue_pattern, sent)
            in_dramatic_personae_matcher = re.findall(dramatic_personae_pattern, sent)
            in_new_act_matcher = re.findall(new_act_pattern, sent)
            in_key_to_marriage_matcher = re.findall(key_to_marriage_pattern, sent)
            in_letter_to_publisher_matcher = re.findall(letter_to_publisher_pattern, sent)
            in_end_matcher = re.findall(end_pattern, sent)
            in_epilogue_matcher = re.findall(epilogue_pattern, sent)

            match_stage_direction = re.findall(r'\[', sent)
            if match_stage_direction:
                is_stage_direction = True
            
            # Check whether the token matches any character name pattern
            match_speaker = re.search(character_names_pattern, sent)
            if match_speaker:
                is_stage_direction = False
                name = match_speaker.group().strip(",")
               
                # Check whether the cleaned name matches one of the character names (without trailing punctuation)
                if any(name.strip(".") in n for n in character_names):
                    
                    current_speaker = name
                    actual_speaker = await get_character(current_speaker)
                    if actual_speaker is not None and current_state == "in_play":
                        if actual_speaker not in characters_present:
                            characters_present.append(actual_speaker)
            match_new_act = re.findall(new_act_pattern, sent)
            if match_new_act:
                characters_present = []
                current_act = await rom_num_converter(match_new_act[0])

            if in_editors_intro_matcher:
                current_state = "in_editors_intro"
            if end_intro_matcher:
                current_state = ""
            if in_prologue_matcher:
                current_state = "in_prologue"
            if in_dramatic_personae_matcher:
                current_state = "in_dramatic_personae"
            if in_new_act_matcher:
                current_state = "in_play"
            if in_key_to_marriage_matcher:
                current_state = "in_key_to_marriage"
            if in_letter_to_publisher_matcher:
                current_state = "in_letter_to_publisher"
            if in_end_matcher:
                characters_present = []
                # return scriblerus_data
                current_state = "end"
                continue
            if in_epilogue_matcher:
                current_state = "in_epilogue"

            if current_state == "in_editors_intro":
                scriblerus_data["three_hours_harrington_intro"].append(nodes.ShortGeneralNode(
                    title="Harrington 1962 intro to Three Hours After Marriage",
                    text=sent
                ))
            elif current_state == "in_prologue":
                scriblerus_data["three_hours_prologue"].append(nodes.PoemNode(
                    book_number=1,
                    line_number=None,
                    line=sent
                ))
            elif current_state == "in_dramatic_personae":
                scriblerus_data["three_hours_dramatic_personae"].append(nodes.ShortGeneralNode(
                    title="Dramatic Personae in Three Hours After Marriage",
                    text=sent
                ))
            elif current_state == "in_play":              
                scriblerus_data["three_hours_play"].append(nodes.PlayNode(
                    id=id,
                    act_number=current_act,
                    scene_number="1",
                    speaker=await get_character(current_speaker) or 'no speaker',
                    characters_present=characters_present,
                    line=sent,
                    is_stage_direction=is_stage_direction
                ))
            elif current_state == "in_key_to_marriage":
                scriblerus_data["three_hours_key_to_marriage"].append(nodes.ShortGeneralNode(
                    title="Key to Marriage in Three Hours After Marriage",
                    text=sent
                ))
            elif current_state == "in_letter_to_publisher":
                scriblerus_data["three_hours_letter_to_publisher"].append(nodes.ShortGeneralNode(
                    title="Letter to Publisher in Three Hours After Marriage",
                    text=sent
                ))
    results = {
        'three_hours_after_marriage': scriblerus_data
    }
    print("RESULTS?? ", results)
    return results