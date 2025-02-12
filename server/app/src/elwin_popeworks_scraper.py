from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import server.app.src.nodes as nodes
import time

def extract_first_number_and_text(input_text):
    # Extract the first number
    number_match = re.search(r'\d+', input_text)
    first_number = number_match.group() if number_match else None

    # Extract text up to "Ver"
    text_match = re.search(r'^(.*?)Ver', input_text)
    text_up_to_ver = text_match.group(1).strip() if text_match else None

    return first_number, text_up_to_ver

# @profile
async def scraper_elwin_popeworks(divs, sent_tokenize):
    start = time.time()
    global scriblerus_data
    scriblerus_data = {
        'elwin_preface_essay_on_criticism': [],
        'essay_on_criticism_contents': [],
        'essay_on_criticism_poem': [],
        'warburton_essay_on_eoc_elwin_intro': [],
        'warburton_essay_on_eoc': [],
        'rol_elwin_intro': [],
        'rol_fermor_preface': [],
        'rol_poem': [],
        'rol_1712_poem': [],

        'unfortunate_lady_elwin_intro': [],
        'unfortunate_lady_poem': [],

        'eloisa_elwin_intro': [],
        'eloisa_poem': [],
        'eloisa_argument': [],

        'eom_elwin_intro': [],
        'eom_argument': [],
        'eom_poem': [],
        
        'universal_prayer_elwin_intro': [],
        'universal_prayer_poem': [],
        'warburton_essay_on_man_appendix': [],
        'warburton_essay_on_man_notes': [],

    }
    global current_state
    current_state = ''
    global current_line_nums
    current_line_nums = []
    global sents
    sents = []
    global last_line_num
    last_line_num = None
    global short_line_ticker
    short_line_ticker = 0
    ebook_end_matcher = r'End of the Project Gutenberg EBook'

    global current_line_num
    current_line_num = 0
    global in_warburton_essay
    in_warburton_essay = False
    global current_line_ftn
    current_line_ftn = None
    global in_ftn_update 
    in_ftn_update = False
    global current_cited_line
    current_cited_line = None
    global cited_line            
    cited_line = None
    global current_canto
    current_canto = 0
    global current_epistle
    current_epistle = 0
    global sent_cited_line
    sent_cited_line = ''
    global current_eom_state 
    current_eom_state = 'arguments'
    global eom_commentary_epistle 
    eom_commentary_epistle = 0
    global next_entry_ready
    next_entry_ready = False

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
    
    last_comment = []

    print("in pope works -> scrape")

    for div in divs:
        content_text = await div.inner_text()
        soup_popeworks_unparsed = BeautifulSoup(content_text, "html.parser")

        soup_popeworks = soup_popeworks_unparsed.get_text()
        
        all_sents = sent_tokenize(soup_popeworks, "english")
        for s in all_sents:
            sents.append(s)

    for sent in sents:
        in_elwin_intro_eoc_poem = len(re.findall(r'WRITTEN IN THE YEAR 1709', sent)) > 0
        in_rol_elwin_intro = re.findall(r'AN HEROI-COMICAL POEM.', sent)
        sent = re.sub(r'\[Pg \d+\]', '', sent)

        if in_elwin_intro_eoc_poem:
            current_state = 'elwin_intro_eoc_poem'
        if in_rol_elwin_intro:
            current_state = 'rol_elwin_intro'
           
        if current_state == 'elwin_intro_eoc_poem':
               
            lines = re.split(r'\n', sent)

            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                if len(re.findall(r'CONTENTS', line)) > 0:
                    current_state = 'essay_on_criticism_contents'
                scriblerus_data['elwin_preface_essay_on_criticism'].append(nodes.ShortGeneralNode(
                    title="Elwin Preface",
                    text=line
                ))
        # print(f"Elapsed time in elwin pope works _ elwin_eoc_intro: {time.time() - start} seconds") 
        if current_state == 'essay_on_criticism_contents':
            curr_verse_matcher=r'(Introduction|ver\. (\d+)(?: to (\d+))?—?)'
            global line_nums_eoc_warburton
            line_nums_eoc_warburton = ''
            nums = re.findall(curr_verse_matcher, sent) or None
            if len(re.findall(r'AN\n\nESSAY ON CRITICISM', sent)) > 0:
                current_state = 'essay_on_criticism_poem'
            # sents = sent_tokenize(soup_popeworks, "english")
            # for sent in sents:
            # else:
            match = re.match(r'(\d+)\s*to\s*(\d+)—(.*)', sent)
            
            if match:
                all_matches = match.groups()
                line_text = all_matches[:-1] 
                line_nums_eoc_warburton = all_matches[-1]

                scriblerus_data['essay_on_criticism_contents'].append(nodes.GeneralNode(
                    title="Essay on Criticism Contents",
                    identifier=line_nums_eoc_warburton,
                    text=line_text
                ))
            # print(f"Elapsed time in elwin pope works _ eoc_contents: {time.time() - start} seconds") 
        if current_state == 'essay_on_criticism_poem':
            lines = re.split(r'\n', sent)
            if re.findall(r'endeavouring to demonstrate', sent):
                current_state = 'warburton_essay_on_eoc_elwin_intro'
            for line in lines:
                possible_line_numbers = re.findall(r'(?<!\[)\b\d+\b(?!\])', line)
                if len(possible_line_numbers) > 0:
                    last_line_num = []
                    last_line_num=possible_line_numbers
                    current_line_num = int(last_line_num[0])
                if last_line_num and len(last_line_num) and last_line_num[0] == line:
                    continue
                # Remove the brackets and numbers from the original text
                line = re.sub(r"\[\d+\]", "", line)
                line_left = re.findall(r'^[1-9]\d*',line)
                if line_left or len(line) < 1:
                    continue
                # if last_line_num and len(last_line_num):
                #     current_line_num += 1
                if 'greater want of skill' in line:
                    current_line_num = 1
                else:
                    current_line_num += 1
                scriblerus_data['essay_on_criticism_poem'].append(nodes.PoemNode(
                    line_number= current_line_num,
                    line=line,
                    book_number=int(last_line_num[0]) if last_line_num and len(last_line_num) else None
                ))
            # print(f"Elapsed time in elwin pope works _ elwin_eoc_poem: {time.time() - start} seconds") 
        if current_state == 'warburton_essay_on_eoc_elwin_intro':
            lines = re.split(r'\n', sent)
            for line in lines:
                flip_to_warburton = re.findall(r'THE COMMENTARY AND NOTES OF', line)
                if flip_to_warburton:
                    in_warburton_essay = True
                    current_state = 'warburton_essay_on_eoc'
                if in_warburton_essay is True or current_state == 'warburton_essay_on_eoc':
                    current_line_ftn = re.findall(r"Ver\. (\d+)",line)
                    scriblerus_data['warburton_essay_on_eoc'].append(nodes.GeneralNode(
                        title="Warburton Essay on Essay on Criticism",
                        identifier=" ".join(current_line_ftn),
                        text=line
                    )) 
                else:
                    scriblerus_data['warburton_essay_on_eoc_elwin_intro'].append(nodes.GeneralNode(
                        title="Elwin essay on Warburton's essay on Essay on Criticism",
                        identifier=current_line_ftn,
                        text=line
                    ))
            # print(f"Elapsed time in elwin pope works _ elwin_warburton_on_eoc_elwin_intro: {time.time() - start} seconds") 
        if current_state == 'warburton_essay_on_eoc':
            verse_matcher_line_nums = re.findall(r"Ver\.", sent)
            line = re.sub(r"(Ver\. \d+)", '', sent)
            rol_title_pattern = r'WRITTEN IN THE YEAR 1712.'
            rol_match = re.findall(rol_title_pattern, sent)
            if rol_match:
                current_state = "rol_elwin_intro"
            if verse_matcher_line_nums:
                in_ftn_update = True
                continue
            if in_ftn_update:
                num_matcher = r'\d+'
                sent_num = re.findall(num_matcher, sent)
                current_line_ftn = sent_num

                in_ftn_update = False  
                # if get_cited_line:
                cited_line_pattern = r'^[^\]]*'
                # sent = re.sub(r'\.', '', line)
                # sent = re.sub(num_matcher, '', line)
    
                line = re.sub(cited_line_pattern, '', line)
            # print(f"Elapsed time in elwin pope works _ warburton_essay_on_eoc: {time.time() - start} seconds")   
            scriblerus_data['warburton_essay_on_eoc'].append(nodes.GeneralNode(
                title="Warburton Essay on Essay on Criticism",
                identifier=int(current_line_ftn[0]) if len(current_line_ftn) else None,
                text=line
            ))

        if current_state == "rol_elwin_intro":
            in_fermor_matcher = r'almost deserving the name of revelations.'
            in_fermor_preface = re.findall(in_fermor_matcher, sent)
            if in_fermor_preface:
                current_state = "rol_fermor_preface"
                last_line_num = []
            lines = re.split(r'\n', sent)
            for line in lines:
                if len(line) < 1:
                    continue
                scriblerus_data['rol_elwin_intro'].append(nodes.ShortGeneralNode(
                    title="RoL Elwin Intro",
                    text=line
                ))
            # print(f"Elapsed time in elwin pope works _ rol_elwin_intro: {time.time() - start} seconds") 
        if current_state == "rol_fermor_preface":
            in_rol_poem_pattern = r'RAPE OF THE LOCK.'
            lines = re.split(r'\n', sent)
            for line in lines:
                in_rol_poem_match = re.findall(in_rol_poem_pattern, line)
                if in_rol_poem_match:
                    current_state = "rol_poem"
                    last_line_num = []
                    current_line_num = 0
                scriblerus_data['rol_fermor_preface'].append(nodes.ShortGeneralNode(
                    title="Letter to Fermor - Preface to RoL",
                    text=line
                ))
            # print(f"Elapsed time in elwin pope works _ rol_fermor_preface: {time.time() - start} seconds") 
        if current_state == "rol_poem":
            new_canto_matcher = r'CANTO\s[IVX]+\.'
            rom_num_matcher = r'CANTO\s([IVX]+)\.'
            lines = re.split(r'\n', sent)

            in_rol_1712_matcher = r' tribuisse tuis.—Mart.'
            
            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                is_num = re.findall(r"\d+", line)
                if is_num:
                    continue
                if len(line) < 1:
                    continue
                new_canto_match = re.findall(new_canto_matcher, line)

                in_rol_1712_match = re.findall(in_rol_1712_matcher, line)
                if in_rol_1712_match:
                    current_state = "rol_1712"
                    last_line_num = []
                    current_line_num = 0

                if new_canto_match:
                    current_canto += 1
                    num = re.findall(rom_num_matcher, new_canto_match[0])
                    if num:
                        current_canto = await rom_num_converter(num[0]) if rom_num_converter(num[0]) != 0 else current_canto

                possible_line_numbers = re.findall(r'(?<!\[)\b\d+\b(?!\])', line)
                if len(possible_line_numbers) > 0:
                    last_line_num = []
                    last_line_num=possible_line_numbers

                if len(last_line_num) and last_line_num[0] == last_line_num:
                    continue

                if 'What dire offence' in line:
                    current_line_num = 1
                else:
                    current_line_num += 1

                line = re.sub(r"\d+", '', line)
                if len(line) < 1:
                    continue
                
                scriblerus_data['rol_poem'].append(nodes.PoemNode(
                    book_number=current_canto,
                    # 'rol_line_number': int(last_line_num[0]) if len(last_line_num) else None,
                    line_number=current_line_num,
                    line=line
                ))
            # print(f"Elapsed time in elwin pope works _ elwin_rol_poem: {time.time() - start} seconds") 
        if current_state == "rol_1712":
            new_canto_matcher = r'CANTO\s[IVX]+\.'
            rom_num_matcher = r'CANTO\s([IVX]+)\.'
            lines = re.split(r'\n', sent)

            unfortunate_lady_elwin_intro_matcher = r'See the Duke of'
            new_canto_match = re.findall(new_canto_matcher, sent)
            if new_canto_match:
                current_canto += 1
                num = re.findall(rom_num_matcher, new_canto_match[0])
                if num:
                    # if re.findall(new_canto_matcher, num[0]) and rom_num_converter[num[0]]:
                    current_canto = await rom_num_converter(num[0]) if rom_num_converter(num[0]) != 0 else current_canto

            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                line = re.sub(r"\d+", '', line)

                if len(line) < 1:
                    continue
                in_unfortunate_lady_intro = re.findall(unfortunate_lady_elwin_intro_matcher, line, re.IGNORECASE)
                if in_unfortunate_lady_intro:
                    last_line_num = []
                    current_state = "unfortunate_lady_elwin_intro"

                possible_line_numbers = re.findall(r'(?<!\[)\b\d+\b(?!\])', line)
                if len(possible_line_numbers) > 0:
                    last_line_num = []
                    last_line_num=possible_line_numbers

                if len(last_line_num) and last_line_num[0] == last_line_num:
                    continue

                if 'What dire offence' in line:
                    current_line_num = 1
                else:
                    current_line_num += 1
                scriblerus_data['rol_1712_poem'].append(nodes.PoemNode(
                    book_number=current_canto,
                    # 'rol_1712_line_number': int(last_line_num[0]) if len(last_line_num) else None,
                    line_number=current_line_num,
                    line=line
                ))
            #print(f"Elapsed time in elwin pope works _ rol_1712: {time.time() - start} seconds") 
        if current_state == "unfortunate_lady_elwin_intro":
            unfortunate_lady_poem_matcher = r'too artificial for the occasion'
            lines = re.split(r'\n', sent)
            for line in lines:
                in_unfortunate_lady_poem = re.findall(unfortunate_lady_poem_matcher, line, re.IGNORECASE)
                if in_unfortunate_lady_poem:
                    current_state = "unfortunate_lady_poem"
                    last_line_num = []
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                scriblerus_data['unfortunate_lady_elwin_intro'].append(nodes.ShortGeneralNode(
                    title="Elwin Intro - Unfortunate Lady",
                    text=line
                ))
            # print(f"Elapsed time in elwin pope works _ elwin_unfortunate_lady_intro: {time.time() - start} seconds") 
        if current_state == "unfortunate_lady_poem":
            eloisa_intro_matcher = r'ELOISA TO ABELARD.'
            lines = re.split(r'\n', sent)
            for line in lines:
                in_eloisa_intro = re.findall(eloisa_intro_matcher, line)
                if in_eloisa_intro:
                    current_state = "eloisa_elwin_intro"
                possible_line_numbers = re.findall(r'(?<!\[)\b\d+\b(?!\])', line)
                if len(possible_line_numbers) > 0:
                    last_line_num = []
                    last_line_num=possible_line_numbers
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue    
                scriblerus_data['unfortunate_lady_poem'].append(nodes.PoemAnnotationNode(
                    book_number=1,
                    line_number=int(last_line_num[0]) if len(last_line_num) else None,
                    text=line
                ))
            # print(f"Elapsed time in elwin pope works _ unfortunate_lady_elwin_poem: {time.time() - start} seconds") 
        if current_state == "eloisa_elwin_intro":
            eloisa_argument_pattern = r'impassioned strains in his Epistle of Eloisa.'
            lines = re.split(r'\n', sent)
            for line in lines:
                in_eloisa_arg = re.findall(eloisa_argument_pattern, line)
                if in_eloisa_arg:
                    current_state = "eloisa_argument"
                    last_line_num = []
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                scriblerus_data['eloisa_elwin_intro'].append(nodes.ShortGeneralNode(
                    title="Elwin Intro - Eloisa to Abelard",
                    text=line
                ))
            # print(f"Elapsed time in elwin pope works _ elwin_elwin_intro: {time.time() - start} seconds") 
        if current_state == "eloisa_argument":
            eloisa_poem_matcher = r'virtue and passion'
            lines = re.split(r'\n', sent)
            for line in lines:
                scriblerus_data['eloisa_argument'].append(nodes.ShortGeneralNode(
                    title="Argument to Eloisa to Abelard",
                    text=line
                ))
                in_eloisa_poem = re.findall(eloisa_poem_matcher, line)
                if in_eloisa_poem:
                    current_state = "eloisa_poem"
                    current_line_num = 0
            # print(f"Elapsed time in elwin pope works _ eloisa argument: {time.time() - start} seconds") 
        if current_state == "eloisa_poem":
            eom_elwin_intro_pattern = r'IN FOUR EPISTLES'
            lines = re.split(r'\n', sent)
            for line in lines:

                in_eom_elwin_intro = re.findall(eom_elwin_intro_pattern, line)
                if in_eom_elwin_intro:
                    last_line_num = []
                    current_state = "eom_elwin_intro"
                possible_line_numbers = re.findall(r'(?<!\[)\b\d+\b(?!\])', line)
                if len(possible_line_numbers) > 0:
                    last_line_num = []
                    last_line_num=possible_line_numbers
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                if len(last_line_num) and last_line_num[0] == line:
                    continue
                if "In these deep solitudes" in line:
                    current_line_num = 1
                else:
                    current_line_num +=1
                
                scriblerus_data['eloisa_poem'].append(nodes.PoemNode(
                    book_number=1,
                    # 'line_number_eloisa': int(last_line_num[0]) if len(last_line_num) else None,
                    line_number=current_line_num,
                    line=line
                ))
            # print(f"Elapsed time in elwin pope works _ eloisa_intro: {time.time() - start} seconds") 
        if current_state == "eom_elwin_intro":
            eom_poem_intro_matcher = r'found worthless.'
            lines = re.split(r'\n', sent)
            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                in_eom_intro = re.findall(eom_poem_intro_matcher, line)
                if in_eom_intro:
                    current_state = "eom_poem"
                    last_line_num = []
                    current_line_num = 0
                line = re.sub(r"\\", "", line)
                scriblerus_data['eom_elwin_intro'].append(nodes.ShortGeneralNode(
                    title="Essay on Man - Elwin Intro",
                    text=line
                ))
            # print(f"Elapsed time in elwin pope works _ elwin_eom_intro: {time.time() - start} seconds") 
        if current_state == "eom_poem":
            new_epistle_matcher = r'EPISTLE\s[IVX]+\.'
            rom_num_matcher = r'EPISTLE\s([IVX]+)\.'
            
            # universal_prayer_intro_pattern = r'DEO OPT.'
            universal_prayer_intro_pattern = r'And all our knowledge is, ourselves to know.'
            in_arg_pattern = r'OF THE NATURE AND STATE OF MAN'
            in_poem_pattern = r'EPISTLE '
           
            lines = re.split(r'\n', sent)
            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                new_epistle_match = re.findall(new_epistle_matcher, line)
                in_poem_matcher = re.findall(in_poem_pattern, line)
                in_arguments_matcher = re.findall(in_arg_pattern, line)

                if in_arguments_matcher:
                    current_eom_state = "arguments"
                
                if new_epistle_match:
                    current_state = "eom_poem"
                    current_epistle += 1
                    
                    num = re.findall(rom_num_matcher, new_epistle_match[0])
                    
                    if num:
                        current_epistle = await rom_num_converter(num[0]) if rom_num_converter(num[0]) != 0 else current_epistle
                possible_line_numbers = re.findall(r'(\d+)', line)
                if possible_line_numbers:
                    last_line_num=possible_line_numbers
                    # print("got line num???? ", last_line_num)

                if current_eom_state == "arguments":
                    if in_poem_matcher:
                        current_eom_state = "poem"
                        last_line_num = []
                        continue
                    scriblerus_data['eom_argument'].append(nodes.PoemAnnotationNode(
                        book_number=current_epistle,
                        line_number=int(last_line_num[0]) if len(last_line_num) else None,
                        text=line
                    ))
                    continue
                in_universal_prayer_intro = re.findall(universal_prayer_intro_pattern, line)
                if in_universal_prayer_intro:
                    current_state = "universal_prayer_elwin_intro"

                if line == "Awake, my St." or new_epistle_match:
                    current_line_num = 1
                else:
                    current_line_num += 1
                if len(last_line_num) and last_line_num[0] in line:
                    continue
                scriblerus_data['eom_poem'].append(nodes.PoemNode(
                    book_number=current_epistle,
                    line_number=current_line_num,
                    line=line
                ))
            # print(f"Elapsed time in elwin pope works _ elwin_eom_poem: {time.time() - start} seconds") 

        if current_state == "universal_prayer_elwin_intro":
            lines = re.split(r'\n', sent)
            universal_prayer_poem_pattern = r'second rate hymn'
            ## NEED TO SWITCH BETWEEN ARGUMENTS HERE...
            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                in_universal_prayer_poem = re.findall(universal_prayer_poem_pattern, line)
                scriblerus_data["universal_prayer_elwin_intro"].append(nodes.ShortGeneralNode(
                    title="Universal Prayer - Elwin Intro",
                    text=line
                ))
                if in_universal_prayer_poem:
                    current_state = "universal_prayer_poem"
                    print('emptying elwin intro')
                    last_line_num = []
                    continue
            #print(f"Elapsed time in elwin pope works _ elwin_universal_prayer_intro: {time.time() - start} seconds") 
        if current_state == "universal_prayer_poem":
            lines = re.split(r'\n', sent)
            warburton_eom_appendices_pattern = r'WILLIAM WARBURTON, D.D.'
            for line in lines:
                line = re.sub(r"\[(\d+)\]", '', line)
                if len(line) < 1:
                    continue
                in_warburton_eom_appendices = re.findall(warburton_eom_appendices_pattern, line)
                if in_warburton_eom_appendices:
                    current_state = "in_warburton_eom_appendices"
                    last_line_num = []
                    continue
                possible_line_numbers = re.findall(r'(?<!\[)\b\d+\b(?!\])', line)
                if len(possible_line_numbers) > 0:
                    last_line_num = []
                    last_line_num=possible_line_numbers
                father_of_all_matcher = r'Father of all!'
                is_first_line = re.findall(father_of_all_matcher, line)
                if is_first_line:
                    current_line_num = 1
                else:
                    current_line_num += 1
                if (len(last_line_num) and last_line_num[0] in line):
                    continue
                if line != "APPENDIX." and line != "THE COMMENTARY AND NOTES OF" and line != "The composition is tame and prosaic, and never rises above the level of a second rate hymn.":
                    scriblerus_data["universal_prayer_poem"].append(nodes.PoemNode(
                        book_number=1,
                        line_number=current_line_num,
                        line=line
                    ))
        
                    # for line in lines:
        eom_notes_matcher = r'The wild relates'
        in_eom_notes = re.findall(eom_notes_matcher, sent)
        if in_eom_notes:
            print("FUCKING HERE")
            current_state = "in_eom_warburton_notes"
            last_line_num = []
            current_line_nums = []
            eom_commentary_epistle = 0
      
        # print(f"Elapsed time in elwin pope works _ universal_prayer_poem: {time.time() - start} seconds") 
        if current_state == "in_warburton_eom_appendices":
            commentary_matcher = r'COMMENTARY ON EPISTLE'
            
            if len(sent) < 1:
                continue
            if re.findall(commentary_matcher, sent):
                eom_commentary_epistle += 1
                last_comment = []
            got_ver = re.findall(r'Ver\.', sent)
            if (got_ver):
                next_entry_ready = True
            if next_entry_ready is True:
                line_nums = []
                number_match = re.findall(r'(\d+)', sent)
                print("we do get number match... ", number_match)
                if number_match:
                    last_line_num = number_match[0]
                    scriblerus_data['warburton_essay_on_man_appendix'].append(nodes.PoemAnnotationNode(
                        book_number=eom_commentary_epistle,
                        line_number=int(last_line_num) if len(last_line_num) > 0 else None,
                        text=last_comment
                    ))
                    last_comment = []
                    next_entry_ready = False
            else:
                last_comment.append(sent)
            # print(f"Elapsed time in elwin pope works _ elwin_warburton_appendices: {time.time() - start} seconds")   

        if current_state == "in_eom_warburton_notes":
            notes_next_epistle_matcher = r'NOTES ON EPISTLE'
            volume_end_matcher = r'NOTES ON EPISTLE'
            lines = re.split(r'\n', sent)
            # verse_matcher_pattern = r"Ver\. (\d+)(?: to (\d+))?|(?:, )?(\d+)"
            verse_matcher_pattern = r"Ver\."
            for line in lines:
                next_entry_ready = False
                has_verse_pattern = re.findall(verse_matcher_pattern, line)
                if has_verse_pattern:
                    current_line_nums = has_verse_pattern
                    next_entry_ready = True


                if next_entry_ready is True:
                    line_nums = []
                    number_match = re.findall(r'(\d+)(?: to (\d+))?|(?:, )?(\d+)', line)
                    
                    if re.findall(notes_next_epistle_matcher, line):
                        eom_commentary_epistle += 1
                        last_comment = []
                    if re.findall(volume_end_matcher, line):
                        current_state = "vol_end"

                    if number_match:
                        last_line_num = number_match[0]
                        last_line_num = [s for s in last_line_num if s]
                        for num in last_line_num:
                            scriblerus_data['warburton_essay_on_man_notes'].append(nodes.PoemAnnotationNode(
                                book_number=eom_commentary_epistle,
                                line_number=num,
                                text=last_comment
                            ))
                        last_comment = []
                        next_entry_ready = False
                else:
                    last_comment.append(sent)



                # print(f"Elapsed time in elwin pope works _ elwin_notes_to_end: {time.time() - start} seconds") 
                # return scriblerus_data
        if current_state == "vol_end":
        # if re.findall(ebook_end_matcher, sent):
            pass

    return scriblerus_data

# if __name__ == "__main__":
#     import asyncio
#     result = asyncio.run(scraper_elwin_popeworks())
