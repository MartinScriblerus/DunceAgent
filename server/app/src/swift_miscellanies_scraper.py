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

async def scraper_swift_miscellanies(divs, sent_tokenize):
    start = time.time()
    print("in swift miscellanies -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global scriblerus_data
    scriblerus_data = {
        'battle_of_books_intro': [],
        'battle_of_books_bookseller_to_reader': [],
        'battle_of_books_preface': [],
        'battle_of_books_text': [],
        'episode_bentley_wotton': [],
        'meditation_broomstick': [],
        'predictions_1708': [],
        'bickerstaff_first_prediction': [],
        'baucis_philemon': [],
        'logicians_refuted': [],
        'puppet_show': [],
        'cadenus_vanessa': [],
        'stella_birthday_1718': [],
        'stella_birthday_1720': [],
        'stella_birthday': [],
        'stella_birthday_1724': [],
        'stella_birthday_1726': [],
        'to_stella': [],
        'first_he_wrote': [],
        'second_prayer_written': [],
        'beast_confession': [],
        'argument_against_christianity': [],
        'essay_on_conversation': [],
        'thoughts_on_various_subjects': [],
    }

    global scrape_ready
    scrape_ready = False


    battle_of_books_intro_pattern = r'Jonathan Swift was born in 1667'
    battle_of_books_bookseller_to_reader_pattern = r'THE BOOKSELLER TO THE READER.'
    battle_of_books_preface_pattern = r'THE PREFACE OF THE AUTHOR'
    battle_of_books_text_pattern = r'A FULL AND TRUE ACCOUNT OF THE'
    episode_bentley_wotton_pattern = r'THE EPISODE OF BENTLEY AND WOTTON'
    meditation_broomstick_pattern = r'A MEDITATION UPON A BROOMSTICK'
    predictions_1708_pattern = r'PREDICTIONS FOR THE YEAR 1708'
    bickerstaff_first_prediction_pattern = r'THE ACCOMPLISHMENT OF THE FIRST OF'
    baucis_philemon_pattern = r'BAUCIS AND PHILEMON'
    logicians_refuted_pattern = r'THE LOGICIANS REFUTED'
    puppet_show_pattern = r'THE PUPPET SHOW'
    cadenus_vanessa_pattern = r'CADENUS AND VANESSA.'
    stella_birthday_1718_pattern = r'Stella this day is'
    stella_birthday_1720_pattern = r'All travellers at first'
    stella_birthday_pattern = r'STELLA’S BIRTHDAY.'
    stella_birthday_1724_pattern = r'STELLA’S BIRTHDAY, 1724'
    stella_birthday_1726_pattern = r'STELLA’S BIRTHDAY, MARCH 13, 1726'
    to_stella_pattern = r'TO STELLA,'
    first_he_wrote_pattern = r'THE FIRST HE WROTE OCT'
    second_prayer_written_pattern = r'THE SECOND PRAYER WAS WRITTEN'
    beast_confession_pattern = r'THE BEASTS’ CONFESSION'
    argument_against_christianity_pattern = r'ABOLISHING OF CHRISTIANITY IN'
    essay_on_conversation_pattern = r'HINTS TOWARDS AN ESSAY ON CONVERSATION'
    thoughts_on_various_subjects_pattern = r'THOUGHTS ON VARIOUS SUBJECTS'

    end_pattern = r'END OF THE PROJECT GUTENBERG EBOOK'



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
            line = re.sub(r'PAGE \d+|PAGE \[UNNUMBERED\]', '', line)
            if len(line) < 1 or line == '.':
                continue
            if re.findall(battle_of_books_intro_pattern, line, re.IGNORECASE):
                scrape_ready = True
                current_state = "in_bob_advertisement"
            if re.findall(battle_of_books_bookseller_to_reader_pattern, line, re.IGNORECASE):
                current_state = "in_bob_bookseller_to_reader"
            if re.findall(battle_of_books_preface_pattern, line, re.IGNORECASE):
                current_state = "in_bob_preface"
            if re.findall(battle_of_books_text_pattern, line, re.IGNORECASE):
                current_state = "in_bob_text"
            if re.findall(episode_bentley_wotton_pattern, line, re.IGNORECASE):
                current_state = "in_episode_bentley_wotton"
            if re.findall(meditation_broomstick_pattern, line, re.IGNORECASE):
                current_state = "in_meditation_broomstick"
            if re.findall(predictions_1708_pattern, line, re.IGNORECASE):
                current_state = "in_predictions_1708"
            if re.findall(bickerstaff_first_prediction_pattern, line, re.IGNORECASE):
                current_state = "in_bickerstaff_first_prediction"
            if re.findall(baucis_philemon_pattern, line, re.IGNORECASE):
                current_state = "in_baucis_philemon"
            if re.findall(logicians_refuted_pattern, line, re.IGNORECASE):
                current_state = "in_logicians_refuted"
            if re.findall(puppet_show_pattern, line, re.IGNORECASE):
                current_state = "in_puppet_show"
            if re.findall(cadenus_vanessa_pattern, line, re.IGNORECASE):
                current_state = "in_cadenus_vanessa"
            if re.findall(stella_birthday_1718_pattern, line, re.IGNORECASE):
                current_state = "in_stella_birthday_1718"
            if re.findall(stella_birthday_1720_pattern, line, re.IGNORECASE):
                current_state = "in_stella_birthday_1720"
            if re.findall(stella_birthday_pattern, line, re.IGNORECASE):
                current_state = "in_stella_birthday"
            if re.findall(stella_birthday_1724_pattern, line, re.IGNORECASE):
                current_state = "in_stella_birthday_1724"
            if re.findall(stella_birthday_1726_pattern, line, re.IGNORECASE):
                current_state = "in_stella_birthday_1726"
            if re.findall(to_stella_pattern, line, re.IGNORECASE):
                current_state = "in_to_stella"
            if re.findall(first_he_wrote_pattern, line, re.IGNORECASE):
                current_state = "in_first_he_wrote"
            if re.findall(second_prayer_written_pattern, line, re.IGNORECASE):
                current_state = "in_second_prayer_written"
            if re.findall(beast_confession_pattern, line, re.IGNORECASE):
                current_state = "in_beast_confession"
            if re.findall(argument_against_christianity_pattern, line, re.IGNORECASE):
                current_state = "in_argument_against_christianity"
            if re.findall(essay_on_conversation_pattern, line, re.IGNORECASE):
                current_state = "in_essay_on_conversation"
            if re.findall(thoughts_on_various_subjects_pattern, line, re.IGNORECASE):
                current_state = "in_thoughts_on_various_subjects"
            if re.findall(end_pattern, line, re.IGNORECASE):
                current_state = "in_end_pattern"
        
            if current_state == "in_bob_advertisement":
                scriblerus_data['battle_of_books_intro'].append(line)
            elif current_state == "in_bob_bookseller_to_reader":
                scriblerus_data['battle_of_books_bookseller_to_reader'].append(line)
            elif current_state == "in_bob_preface":
                scriblerus_data['battle_of_books_preface'].append(line)
            elif current_state == "in_bob_text":
                scriblerus_data['battle_of_books_text'].append(line)
            elif current_state == "in_episode_bentley_wotton":
                scriblerus_data['episode_bentley_wotton'].append(line)
            elif current_state == "in_meditation_broomstick":
                scriblerus_data['meditation_broomstick'].append(line)
            elif current_state == "in_predictions_1708":
                scriblerus_data['predictions_1708'].append(line)
            elif current_state == "in_bickerstaff_first_prediction":
                scriblerus_data['bickerstaff_first_prediction'].append(line)
            elif current_state == "in_baucis_philemon":
                scriblerus_data['baucis_philemon'].append(line)
            elif current_state == "in_logicians_refuted":
                scriblerus_data['logicians_refuted'].append(line)
            elif current_state == "in_puppet_show":
                scriblerus_data['puppet_show'].append(line)
            elif current_state == "in_cadenus_vanessa":
                scriblerus_data['cadenus_vanessa'].append(line)
            elif current_state == "in_stella_birthday_1718":
                scriblerus_data['stella_birthday_1718'].append(line)
            elif current_state == "in_stella_birthday_1720":
                scriblerus_data['stella_birthday_1720'].append(line)
            elif current_state == "in_stella_birthday":
                scriblerus_data['stella_birthday'].append(line)
            elif current_state == "in_stella_birthday_1724":
                scriblerus_data['stella_birthday_1724'].append(line)
            elif current_state == "in_stella_birthday_1726":
                scriblerus_data['stella_birthday_1726'].append(line)
            elif current_state == "in_to_stella":
                scriblerus_data['to_stella'].append(line)
            elif current_state == "in_first_he_wrote":
                scriblerus_data['first_he_wrote'].append(line)
            elif current_state == "in_second_prayer_written":
                scriblerus_data['second_prayer_written'].append(line)
            elif current_state == "in_beast_confession":
                scriblerus_data['beast_confession'].append(line)
            elif current_state == "in_argument_against_christianity":
                scriblerus_data['argument_against_christianity'].append(line)
            elif current_state == "in_essay_on_conversation":
                scriblerus_data['essay_on_conversation'].append(line)
            elif current_state == "in_thoughts_on_various_subjects":
                scriblerus_data['thoughts_on_various_subjects'].append(line)
            elif current_state == "in_end_pattern":
                continue
    results = {
        "swift_miscellanies": scriblerus_data
    }

    return results





            
    return scriblerus_data         
            

            
            