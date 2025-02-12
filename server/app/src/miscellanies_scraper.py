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

async def scraper_miscellanies(divs, sent_tokenize):
    start = time.time()
    print("in miscellanies -> scrape")
    global sents
    sents = []
    global current_state
    current_state = ''
    global current_line_num
    current_line_num = 0
    global scriblerus_data
    scriblerus_data = {
        'advertisement': [],
        'deplorable_frenzy': [],
        'revenge_by_poison': [],
        'curll_deplorable_condition': [],
        'curll_converted': [],
        'revenge_against_punning': [],
        'wonderful_wonder_1': [],
        'wonderful_wonder_2': [],
        'humble_petition': [],
        'examining_drugs': [],
        'annus_mirabilis': [],
        'virgilius_restauratus': [],
        'origin_of_sciences': [],
        'cannot_rain': [],
        'infallible_schemes': [],
        'modest_proposal': [],
        'vindication_of_carteret': [],
        'fates_of_clergymen': [],
        'on_modern_education': [],
        'second_letter_intelligencer': [],
        'true_faithful_narrative': [],
        'journal_modern_lady': [],
        'country_life': [],
        'cutting_old_thorn': [],
        'pastoral_dialogue': [],
        'mary_the_cook': [],
        'mad_mullineux_and_timothy': [],
        'epitaph_on_francis': [],
        'peter_epigram': [],
        'epitaph_round_woman': [],
        'epigram_on_a_prelate': [],
        'epigram_from_french': [],
        'epitaph_on_jack': [],
        'epigram_kit_kats': [],
        'to_a_lady_temple_of_fame': [],
        'england_arch_poet': [],
        'swift_to_pope_while_writing_dunciad': [],
        'bounce_to_fop': [],
        'countess_cutting_paper': [],
        'certain_lady_at_court': [],
        'soldier_scholar': [],
        'to_dr_dly': [],
    }

    global scrape_ready
    scrape_ready = False

    advertisement_pattern = r'it contains the Remainder'
    deplorable_frenzy_pattern = r'THE NARRATIVE OF Dr. Robert Norris'
    revenge_by_poison_pattern = r'A full and true ACCOUNT OF A Horrid and Barbarous'
    curll_deplorable_condition_pattern = r'THE Publick is already acquainted with the Manner'
    curll_converted_pattern = r'A Strange but True RELATION HOW EDMUND CURLL'
    revenge_against_punning_pattern = r'Revenge AGAINST PUNNING'
    wonderful_wonder_1_pattern = r'THE WONDERFUL WONDER of WONDERS'
    wonderful_wonder_2_pattern = r'THE WONDER Of all the Wonders'
    humble_petition_pattern = r'To the RIGHT HONOURABLE The MAYOR and ALDERMEN'
    examining_drugs_pattern = r'Company exercising the Trade and Mistery'
    annus_mirabilis_pattern = r'Annus Mirabilis'
    origin_of_sciences_pattern = r'AN ESSAY Of the Learned MARTINUS SCRIBLERUS'
    virgilius_restauratus_pattern= r'VIRGILIUS RESTAURATUS'
    cannot_rain_but_it_pours_pattern = r'the Arrival of a White Bear'
    infallible_schemes_pattern = r'An INFALIBLE SCHEME To Pay'
    modest_proposal_pattern = r'A MODEST PROPOSAL FOR'
    vindication_of_carteret_pattern = r'A VINDICATION OF THE Lord Lieutenant of Ireland'
    fates_of_clergymen_pattern = r'AN ESSAY ON THE Fates of CLERGYMEN'
    on_modern_education_pattern = r'AN ESSAY ON Modern Education'
    second_letter_intelligencer_pattern = r'A SECOND LETTER TO THE Intelligencer'
    true_faithful_narrative_pattern = r'A True and Faithful NARRATIVE OF'
    journal_modern_lady_pattern = r'THE JOURNAL OF A Modern LADY'
    country_life_pattern = r'THE COUNTRY LIFE'
    cutting_old_thorn_pattern = r'Cutting down the OLD'
    pastoral_dialogue_pattern = r'A PASTORAL DIALOGUE'
    mary_the_cook_pattern = r'Mary the Cook-Maid'
    mad_mullineux_and_timothy_pattern = r'tis not my Bread and Butter'
    epitaph_on_francis_pattern = r'HERE continueth to rot'
    peter_epigram_pattern = r'PEter complains, that God has given'

 
    epitaph_round_woman_pattern = r'HERE lies a round Woman'
    epigram_on_a_prelate_pattern = r'On seeing a worthy Prelate'
    epigram_from_french_pattern = r'SIR, I admit your gen'
    epitaph_on_jack_pattern = r'WELL then, poor'
    epigram_kit_kats_pattern = r'WHence deathless Kit-Cat took its Name'
    to_a_lady_temple_of_fame_pattern = r'Fame with Men'
    england_arch_poet_pattern = r'was or will be half read'
    swift_to_pope_while_writing_dunciad_pattern = r'POpe has the Talent well to speak'
    bounce_to_fop_pattern = r'TO thee sweet Fop'
    countess_cutting_paper_pattern = r'On the Countess of B'
    certain_lady_at_court_pattern = r'I Know the thing'
    soldier_scholar_pattern = r'THUS spoke to my Lady the Knight full of Care'
    to_dr_dly_pattern = r'some raw Youth in'

    for div in divs:
        content_text = await div.inner_text()
        soup_popeworks_unparsed = BeautifulSoup(content_text, "html.parser")

        soup_popeworks = soup_popeworks_unparsed.get_text()
        
        all_sents = sent_tokenize(soup_popeworks, "english")
        for s in all_sents:
            sents.append(s)
    print("here....!!")
    for sent in sents:
        sent = re.sub(r'PAGE \[UNNUMBERED\]', '', sent)
        sent = re.sub(r'PAGE \d+\.', '', sent)
        sent = re.sub(r'\|', '', sent)
        sent = re.sub(r'PAGE(?: \d+)?|[\\/|]', '', sent)
        
        lines = re.split(r'\n', sent)
        for line in lines:
            if line == "description":
                continue
            if len(line) < 1:
                continue
            if scrape_ready == False and re.findall(advertisement_pattern, line):
                scrape_ready = True
                current_state = "in_advertisement"
            if scrape_ready is False:
                continue
            if re.findall(deplorable_frenzy_pattern, line, re.IGNORECASE):
                current_state = "in_deplorable"
            if re.findall(revenge_by_poison_pattern, line, re.IGNORECASE):
                current_state = "in_revenge_by_poison"
            if re.findall(curll_deplorable_condition_pattern, line, re.IGNORECASE):
                print('in deplorable condition')
                current_state = "deplorable_condition"
            if re.findall(curll_converted_pattern, line, re.IGNORECASE):
                current_state = "curll_converted"
            if re.findall(revenge_against_punning_pattern, line, re.IGNORECASE):
                current_state = "revenge_against_punning"
            if re.findall(wonderful_wonder_1_pattern, line, re.IGNORECASE):
                current_state = "wonderful_wonder_1"
            if re.findall(wonderful_wonder_2_pattern, line, re.IGNORECASE):
                current_state = "wonderful_wonder_2"
            if re.findall(humble_petition_pattern, line, re.IGNORECASE):
                current_state = "humble_petition"
            if re.findall(examining_drugs_pattern, line, re.IGNORECASE):
                current_state = "examining_drugs"
            if re.findall(annus_mirabilis_pattern, line, re.IGNORECASE):
                current_state = "annus_mirabilis"
            if re.findall(origin_of_sciences_pattern, line, re.IGNORECASE):
                current_state = "origin_of_sciences"
            if re.findall(virgilius_restauratus_pattern, line, re.IGNORECASE):
                current_state = "virgilius_restauratus"
            if re.findall(cannot_rain_but_it_pours_pattern, line, re.IGNORECASE):
                current_state = "cannot_rain"
            if re.findall(infallible_schemes_pattern, line, re.IGNORECASE):
                current_state = "infallible_schemes"
            if re.findall(modest_proposal_pattern, line, re.IGNORECASE):
                current_state = "modest_proposal"
            if re.findall(vindication_of_carteret_pattern, line, re.IGNORECASE):
                current_state = "vindication_of_carteret"
            if re.findall(fates_of_clergymen_pattern, line, re.IGNORECASE):
                current_state = "fates_of_clergymen"
            if re.findall(on_modern_education_pattern, line, re.IGNORECASE):
                current_state = "on_modern_education"
            if re.findall(second_letter_intelligencer_pattern, line, re.IGNORECASE):
                current_state = "second_letter_intelligencer"
            if re.findall(true_faithful_narrative_pattern, line, re.IGNORECASE):
                current_state = "true_faithful_narrative"
            if re.findall(journal_modern_lady_pattern, line, re.IGNORECASE):
                current_state = "journal_modern_lady"
            if re.findall(country_life_pattern, line, re.IGNORECASE):
                current_state = "country_life"
            if re.findall(cutting_old_thorn_pattern, line, re.IGNORECASE):
                current_state = "cutting_old_thorn"
            if re.findall(pastoral_dialogue_pattern, line, re.IGNORECASE):
                current_state = "pastoral_dialogue"
            if re.findall(mary_the_cook_pattern, line, re.IGNORECASE):
                current_state = "mary_the_cook"
            if re.findall(mad_mullineux_and_timothy_pattern, line, re.IGNORECASE):
                print('in mad mullineux')
                current_state = "mad_mullineux_and_timothy"
            if re.findall(epitaph_on_francis_pattern, line, re.IGNORECASE):
                current_state = "epitaph_on_francis"
            if re.findall(peter_epigram_pattern, line, re.IGNORECASE):
                current_state = "peter_epigram"
            if re.findall(epitaph_round_woman_pattern, line, re.IGNORECASE):
                current_state = "epitaph_round_woman"
            if re.findall(epigram_on_a_prelate_pattern, line, re.IGNORECASE):
                current_state = "epigram_on_a_prelate"
            if re.findall(epigram_from_french_pattern, line, re.IGNORECASE):
                current_state = "epigram_from_french"
            if re.findall(epitaph_on_jack_pattern, line, re.IGNORECASE):
                current_state = "epitaph_on_jack"
            if re.findall(epigram_kit_kats_pattern, line, re.IGNORECASE):
                current_state = "epigram_kit_kats"
            if re.findall(to_a_lady_temple_of_fame_pattern, line, re.IGNORECASE):
                current_state = "to_a_lady_temple_of_fame"
            if re.findall(england_arch_poet_pattern, line, re.IGNORECASE):
                current_state = "england_arch_poet"
            if re.findall(swift_to_pope_while_writing_dunciad_pattern, line, re.IGNORECASE):
                current_state = "swift_to_pope_while_writing_dunciad"
            if re.findall(bounce_to_fop_pattern, line, re.IGNORECASE):
                current_state = "bounce_to_fop"
            if re.findall(countess_cutting_paper_pattern, line, re.IGNORECASE):
                current_state = "countess_cutting_paper"
            if re.findall(certain_lady_at_court_pattern, line, re.IGNORECASE):
                current_state = "certain_lady_at_court"
            if re.findall(soldier_scholar_pattern, line, re.IGNORECASE):
                current_state = "soldier_scholar"
            if re.findall(to_dr_dly_pattern, line, re.IGNORECASE):
                current_state = "dr_dly"
            
            
            
        

            if current_state == 'in_advertisement':
                scriblerus_data['advertisement'].append(line)
            if current_state == 'in_deplorable':
                scriblerus_data['deplorable_frenzy'].append(line)
            if current_state == 'in_revenge_by_poison':
                scriblerus_data['revenge_by_poison'].append(line)
            if current_state == 'in_deplorable_condition':
                scriblerus_data['curll_deplorable_condition'].append(line)
            if current_state == 'curll_converted':
                scriblerus_data['curll_converted'].append(line)
            if current_state == 'revenge_against_punning':
                scriblerus_data['revenge_against_punning'].append(line)
            if current_state == 'wonderful_wonder_1':
                scriblerus_data['wonderful_wonder_1'].append(line)
            if current_state == 'wonderful_wonder_2':
                scriblerus_data['wonderful_wonder_2'].append(line)
            if current_state == 'humble_petition':
                scriblerus_data['humble_petition'].append(line)
            if current_state == 'examining_drugs':
                scriblerus_data['examining_drugs'].append(line)
            if current_state == 'annus_mirabilis':
                scriblerus_data['annus_mirabilis'].append(line)
            if current_state == 'origin_of_sciences':
                scriblerus_data['origin_of_sciences'].append(line)
            if current_state == 'virgilius_restauratus':
                scriblerus_data['virgilius_restauratus'].append(line)
            if current_state == 'cannot_rain':
                scriblerus_data['cannot_rain'].append(line)
            if current_state == 'infallible_schemes':
                scriblerus_data['infallible_schemes'].append(line)
            if current_state =='modest_proposal':
                scriblerus_data['modest_proposal'].append(line)
            if current_state == 'vindication_of_carteret':
                scriblerus_data['vindication_of_carteret'].append(line)
            if current_state == 'fates_of_clergymen':
                scriblerus_data['fates_of_clergymen'].append(line)
            if current_state == 'on_modern_education':
                scriblerus_data['on_modern_education'].append(line)
            if current_state =='second_letter_intelligencer':
                scriblerus_data['second_letter_intelligencer'].append(line)
            if current_state == 'deplorable_condition':
                scriblerus_data['curll_deplorable_condition'].append(line)
            if current_state == 'true_faithful_narrative':
                scriblerus_data['true_faithful_narrative'].append(line)
            if current_state == 'journal_modern_lady':
                scriblerus_data['journal_modern_lady'].append(line)
            if current_state == 'country_life':
                scriblerus_data['country_life'].append(line)
            if current_state == 'mad_mullineux_and_timothy':
                scriblerus_data['mad_mullineux_and_timothy'].append(line)
            if current_state == 'dr_dly':
                scriblerus_data['to_dr_dly'].append(line)
            if current_state == 'cutting_old_thorn':
                scriblerus_data['cutting_old_thorn'].append(line)
            if current_state == 'pastoral_dialogue':
                scriblerus_data['pastoral_dialogue'].append(line)
            if current_state =='mary_the_cook':
                scriblerus_data['mary_the_cook'].append(line)
            if current_state =='mad_mullineux_and_timothy':
                scriblerus_data['mad_mullineux_and_timothy'].append(line)
            if current_state == 'epitaph_on_francis':
                scriblerus_data['epitaph_on_francis'].append(line)
            if current_state == 'peter_epigram':
                scriblerus_data['peter_epigram'].append(line)
            if current_state == 'epitaph_round_woman':
                scriblerus_data['epitaph_round_woman'].append(line)
            if current_state == 'epigram_on_a_prelate':
                scriblerus_data['epigram_on_a_prelate'].append(line)
            if current_state == 'epigram_from_french':
                scriblerus_data['epigram_from_french'].append(line)
            if current_state == 'epitaph_on_jack':
                scriblerus_data['epitaph_on_jack'].append(line)
            if current_state == 'epigram_kit_kats':
                scriblerus_data['epigram_kit_kats'].append(line)
            if current_state == 'to_a_lady_temple_of_fame':
                scriblerus_data['to_a_lady_temple_of_fame'].append(line)
            if current_state == 'england_arch_poet':
                scriblerus_data['england_arch_poet'].append(line)
            if current_state =='swift_to_pope_while_writing_dunciad':
                scriblerus_data['swift_to_pope_while_writing_dunciad'].append(line)
            if current_state == 'bounce_to_fop':
                scriblerus_data['bounce_to_fop'].append(line)
            if current_state == 'countess_cutting_paper':
                scriblerus_data['countess_cutting_paper'].append(line)
            if current_state == 'certain_lady_at_court':
                scriblerus_data['certain_lady_at_court'].append(line)
            if current_state =='soldier_scholar':
                scriblerus_data['soldier_scholar'].append(line)
            if current_state == 'to_dr_dly':
                scriblerus_data['to_dr_dly'].append(line)
            
    return scriblerus_data         
            

            
            