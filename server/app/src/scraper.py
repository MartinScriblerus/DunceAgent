# import pprint
# import pandas as pd
# from bs4 import BeautifulSoup
# import re
# from playwright.async_api import async_playwright
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import sent_tokenize
# import server.app.src.nodes as nodes

# # Download the punkt tokenizer if needed
# nltk.download('punkt')

# from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# nlp = pipeline("ner")

# # Specify the exact model and revision
# # ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
# model_name = "RoBERTa-base"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
# print("MODEL CONFIG: ", model)

# inputs = tokenizer("Your input text here", return_tensors="pt")

# async def initial_scrape():
#     async with async_playwright() as p:

#         scriblerus_data = {
#             'dunciad_essays': [],
#             'dunciad_appendices': [],
#             'dunciad_summaries': [],
#             'dunciad_poem': [],
#             'dunciad_ftns': [],
#             'dunciad_index': [],
#             # 'peri_bathous_data': [],
#             'memoirs_data': [],
#             'pope_letters': []
#         }

#         # Launch the browser
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         # Define the target URL
#         url = "https://quod.lib.umich.edu/cgi/t/text/text-idx?c=ecco;cc=ecco;rgn=main;view=text;idno=004809160.0001.000"  # Replace with your target URL

#         # Navigate to the URL
#         await page.goto(url)

#         button_xpath = '//*[@id="maincontent"]/div[2]/div/div/div/a'

#         await page.locator(button_xpath).click()

#         await page.wait_for_load_state('networkidle')
#         await page.set_extra_http_headers({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
#         dunciad_content_divs = await page.query_selector_all('.fullview-main')
        
#         push_to_dunciad_ftns = False
#         poem_and_remaining = []
#         global current_book
#         global in_dunciad_index
#         global in_poem
#         global in_essays
#         global in_dunciad_appendices
#         global in_summaries
#         global in_authors_of_notes_index
#         global in_index_of_things
#         global last_entry
#         global last_book_num
#         global last_line
#         global processed_combinations
#         global index_hash
#         global curr_entry

#         current_book = 1
#         current_ftn = 1
#         in_authors_of_notes_index = False
#         in_index_of_things = False
#         last_entry = ""
#         last_book_num = None
#         last_line = None
#         processed_combinations = set() 
#         index_hash = []
#         curr_entry = {
#             'book': last_book_num,
#             'line': last_line,
#             'text': last_entry,
#         }

#         in_summaries = False
#         in_dunciad_appendices = False
#         in_essays = True
#         in_poem = False
#         in_dunciad_index = False

#         sentences_dunciad_ftns = None

#         text_start_matcher = r'THE DUNCIAD, IN THREE BOOKS, WITH Notes Variorum.'
#         book_1_poem_matcher = r"BOOKS and the Man I sing,"
#         book_2_poem_matcher = r"HIGH on a gorgeous seat,"
#         book_3_poem_matcher = r"BUT in her Temple's last recess"
        
#         matcher_insummaries_start = r"ARGUMENT to BOOK the FIRST."
#         matcher_remarks_start = r"REMARKS on BOOK the"
#         pattern_end_book_3 = r'REMARKS on BOOK the THIRD'
#         pattern_end = r"ARGUMENT to BOOK the"
#         index_pattern_matcher_start = r'JOHN BARBER'
#         index_pattern_matcher_end = r'others, passim'
#         extended_index_pattern_matcher_start = r'A little abject Thing'
#         extended_index_pattern_matcher_end = r'Whirligigs iii. 49'

#     # try:
#         for div in dunciad_content_divs:
#             content_text = await div.inner_text()
#             soup_dunciad_unparsed = BeautifulSoup(content_text, "html.parser")
#             soup_dunciad = soup_dunciad_unparsed.get_text()
#             soup_dunciad = re.sub(r'Line \d+', '', soup_dunciad)
#             soup_dunciad = soup_dunciad.replace("b.", "")

#             # Regex pattern for "V. [number]"
#             pattern_start = r'\b(?!Nov\.)V\.\s\d+\b'
#             pattern_start_book_3 = r'\d+ V\.'
            
#             matches_start = re.findall(pattern_start, soup_dunciad)
#             matches_end = re.findall(pattern_end, soup_dunciad)
#             matches_third_book_done = re.findall(pattern_end_book_3, soup_dunciad)
#             match_remarks_start = re.findall(matcher_remarks_start, soup_dunciad)
            
#             if matches_start or matches_third_book_done or match_remarks_start:
#                 in_summaries = False
#                 push_to_dunciad_ftns = True
#             if matches_end:
#                 push_to_dunciad_ftns = False
#                 in_summaries = True
#             if push_to_dunciad_ftns is True:
#                 in_summaries = False
#                 soup_dunciad = re.sub(r'\s+', ' ', soup_dunciad).strip()
                

#                 sentences_dunciad_ftns = sent_tokenize(soup_dunciad, "english")
#                 for sentence in sentences_dunciad_ftns:
#                     sentence = re.sub(r"\b(Book |Verse)\b", "", sentence)
#                     if index_pattern_matcher_start in sentence or extended_index_pattern_matcher_start in sentence:
#                         in_dunciad_index = True
#                     if in_dunciad_appendices is True:
#                         scriblerus_data["dunciad_appendices"].append(sentence)
#                     if extended_index_pattern_matcher_end in sentence:
#                         scriblerus_data['dunciad_index'].append(sentence + '. 49')
#                         in_dunciad_index = False
#                     if index_pattern_matcher_end in sentence:
#                         scriblerus_data['dunciad_index'].append(sentence)
#                         in_dunciad_appendices = True   
#                         in_dunciad_index = False
#                     if in_dunciad_index and (index_pattern_matcher_start not in sentence and extended_index_pattern_matcher_start not in sentence):
                        
#                         scriblerus_data["dunciad_index"].append(sentence)
#                     if extended_index_pattern_matcher_start in sentence:
#                         sentence = re.sub(r'\b(?!i{1,3}\b)[ivxlcdm]+\b', '', sentence)

#                         in_dunciad_appendices = False
#                         scriblerus_data["dunciad_index"].append(sentence)
#                     match = re.search(pattern_start, sentence)
#                     match_book_3 = re.search(pattern_start_book_3, sentence)                       
#                     if match and in_dunciad_index is False and in_dunciad_appendices is False:
#                         current_ftn = match.group().split(" ")[1]
#                         scriblerus_data["dunciad_ftns"].append(nodes.DunciadNode(
#                             book_number = current_book,
#                             line_number = current_ftn,
#                             line = sentence
#                             )
#                         )
#                     elif match_book_3 and in_dunciad_index is False and in_dunciad_appendices is False:
#                         current_book = 3
#                         current_ftn = match_book_3.group().split(" ")[0]
#                         scriblerus_data["dunciad_ftns"].append(nodes.DunciadNode(
#                             book_number = current_book,
#                             line_number = current_ftn,
#                             line = sentence
#                             )
#                         )
#                     elif in_dunciad_index is False and in_dunciad_appendices is False:
#                         scriblerus_data["dunciad_ftns"].append(nodes.DunciadNode(
#                             book_number = current_book,
#                             line_number = current_ftn,
#                             line = sentence
#                             )
#                         )
                
#             else:
#                 book_1_start_matcher = r"cause, and apprehending the period of her empire from the old age of the present monarch Settle: Wherefore debating whether to betake himself to Law or Politicks, he raises an altar of proper books, and (making first his solemn prayer and declaration) purposes thereon to sacrifice all his unsuccessful wri∣tings. As the pile is kindled, the Goddess behold∣ing the slame from her seat, flies in person and puts it out, by casting upon it the poem of Thule. She forthwith reveals berself to him, transports him to her Temple, unfolds her arts, and initiates him into her mysteries: then announcing the death of Settle that night, anoints, and proclaims him Successor.\n\nBOOKS and the Man I sing, the first who brings\nThe Smithfield Muses to the Ear of Kings."
#                 book_1_poem_matcher = r"BOOKS and the Man I sing,"
#                 book_2_poem_matcher = r"HIGH on a gorgeous seat"
#                 essays_start_matcher = r'IT will be sufficient to say of this Edition'
#                 initial_essay_done = r'THE DUNCIAD, IN THREE BOOKS, WITH Notes Variorum.'

#                 if len(str(soup_dunciad)) > 0 and str(soup_dunciad) is not None:
#                     if essays_start_matcher in str(soup_dunciad):
#                         in_essays = True
#                         in_summaries = False
#                     if initial_essay_done in str(soup_dunciad):
#                         in_essays = False
#                         in_summaries = True
#                     if book_3_poem_matcher in str(soup_dunciad):
#                         current_book = 3
#                     if book_1_poem_matcher in soup_dunciad:
#                         in_essays = False
#                         in_poem = True
#                         split_1_text = re.split(book_1_poem_matcher, soup_dunciad)

#                         book_1_opening_couplet = book_1_poem_matcher + split_1_text[1]
#                         book_1_opening_couplet_split = re.split("brings", book_1_opening_couplet)
#                         book_1_opening_couplet_split_1 = book_1_opening_couplet_split[0] + "brings"
#                         book_1_opening_couplet_split_2 = re.split(book_1_start_matcher, book_1_opening_couplet_split[1])[0].split()

#                         opening_earofkings = ' '.join(book_1_opening_couplet_split_2)
#                         poem_and_remaining.append(book_1_opening_couplet_split_1  + '\n')
#                         poem_and_remaining.append(opening_earofkings  + '\n')
#                     elif book_2_poem_matcher in str(soup_dunciad):
#                         in_essays = False
#                         current_book = 2
#                         in_poem = True
#                         in_summaries = False
#                         split_2_text = re.split(book_2_poem_matcher, soup_dunciad)                    
#                         book_2_part_2 = book_2_poem_matcher + split_2_text[1]
#                         poem_and_remaining.append(book_2_part_2 + '\n')
#                     elif in_essays is not True and in_poem is True:
#                         poem_and_remaining.append(soup_dunciad + '\n')
#                     elif in_essays is True and in_summaries is not True:
#                         elem = re.sub(r'\s+', ' ', soup_dunciad)
#                         scriblerus_data["dunciad_essays"].append(soup_dunciad)
#         the_poem = {
#             'book_1': [],
#             'book_2': [],
#             'book_3': []
#         }

#         for elem in poem_and_remaining:
#             if pattern_end in elem:
#                 in_summaries = True
#             if text_start_matcher in elem:
#                 in_summaries = False
#             if book_1_poem_matcher in elem:
#                 in_summaries = False
#                 in_essays = False
#                 current_book = 1
#             if book_2_poem_matcher in elem:
#                 in_summaries = False
#                 in_essays = False
#                 current_book = 2
#             if book_3_poem_matcher in elem:
#                 in_summaries = False
#                 in_essays = False
#                 current_book = 3
#             if matcher_remarks_start in elem and pattern_end_book_3 not in elem:
#                 in_summaries = False
#                 scriblerus_data["dunciad_ftns"].append(nodes.DunciadNode(
#                     book_number = current_book,
#                     line_number = 0,
#                     line = elem
#                     )
#                 )
#                 push_to_dunciad_ftns = True
#             if (matcher_insummaries_start in elem and pattern_end_book_3 not in elem) or in_summaries is True:
#                 in_summaries = True
#                 elem = re.sub(r'\s+', ' ', elem).strip()
#                 sentences_dunciad_summaries = sent_tokenize(elem)
#                 for sentence in sentences_dunciad_summaries:
#                     if matcher_insummaries_start in sentence:
#                         begin_bk_1_args = matcher_insummaries_start + sentence
#                         scriblerus_data["dunciad_summaries"].append({
#                             "dunciad_book_summary": begin_bk_1_args,
#                             "current_book": current_book
#                         })
#                     else:
#                         scriblerus_data["dunciad_summaries"].append({
#                             "dunciad_book_summary": sentence,
#                             "current_book": current_book
#                         })
#             else:
#                 if current_book == 1 and elem is not None and in_summaries is not True:
#                     the_poem['book_1'].append(str(elem))
#                 elif current_book == 2 and elem is not None and in_summaries is not True:
#                     the_poem['book_2'].append((elem))
#                 elif current_book == 3 and elem is not None and in_summaries is not True:
#                     the_poem['book_3'].append((elem))
    
#         joined_books = {
#             '1': " ".join(the_poem['book_1']),
#             '2': " ".join(the_poem['book_2']),
#             '3': " ".join(the_poem['book_3'])
#         } 
#         # List to store the processed text with line numbers
#         processed_lines = {
#             'book_1': [],
#             'book_2': [],
#             'book_3': []
#         }

#         the_line = 0
#         in_book_2 = False
#         in_book_3 = False

#         for book_num, book in enumerate(joined_books):
#             book_of_poem = filter(None, joined_books[str(book_num + 1)].split('\n'))
#             for i, line in enumerate(book_of_poem):
#                 cleaned_line = re.sub(r'\s+', ' ', line).strip()
#                 cleaned_line = re.sub(r'Line|\d+', '', cleaned_line)
#                 if cleaned_line is not None:
#                     processed_lines[f'book_{book_num + 1}'].append((i, cleaned_line))
#             for line_num, text in filter(None, processed_lines[f'book_{book_num + 1}']):
#                 if text is not None and len(str(text)) > 0:
                    
#                     if book_num == 2 and not in_book_2:
#                         in_book_2 = True
#                         the_line = 0
#                     elif book_num == 3 and not in_book_3:
#                         in_book_3 = True
#                         the_line = 0
#                     the_line = the_line + 1   
#                     scriblerus_data["dunciad_poem"].append(nodes.DunciadNode(
#                         book_number=book_num + 1,
#                         line_number=the_line,
#                         line=text
#                     ))
                
#         stripped_text = re.sub(r'[^A-Za-z0-9. -]+', ' ', " ".join(scriblerus_data["dunciad_index"]))
    
#         stripped_text = re.sub(r'\s+', ' ', stripped_text)
        
#         joined_index_data = stripped_text.strip()# # Release the resources
#         joined_index_data = joined_index_data.replace('INDEX OF PERSONS CELEBRATED IN THIS POEM.','')
#         joined_index_data = joined_index_data.replace('INDEX TO THE DUNCIAD OF THINGS INCLUDING AUTHORS TO BE FOUND IN THE NOTES C. THE FIRST NUMBER DENOTES THE BOOK THE SECOND THE VERSE. PRO. PROLEGOMENA.','')

#         regex = r"(?<=\d)\s+(?=[A-Z])|(?<=\s)(?=[ivxlc]{1,3}\s+[A-Z])"
#         result = [re.split(regex, joined_index_data)] 

#         joined_indices = [[x for x in lst if x] for lst in result]
        
#         essays_to_sentence = " ".join(scriblerus_data["dunciad_essays"])
#         essays_to_sentence = re.sub(r'\s+', ' ', essays_to_sentence).strip()

#         sentences_dunciad_essays = sent_tokenize(essays_to_sentence, "english")    
#         appendices_to_sentence = " ".join(scriblerus_data["dunciad_appendices"])
#         appendices_to_sentence = re.sub(r'\s+', ' ', appendices_to_sentence).strip()
#         sentences_dunciad_appendices = sent_tokenize(appendices_to_sentence, "english")    

#         rom_num_pattern = r"\b(i{1,3})\.\s*(\d+)"

#         roman_to_arabic = {
#             'i': 1,
#             'ii': 2,
#             'iii': 3
#         } 
        
#         sub_pattern = r"\b(i{1,3})\.\s*(\d+)"

#         first_entry_things = True
#         for entry in joined_indices[0]:
#             if re.findall(r'INDEX OF THE AUTHORS OF THE NOTES', entry):
#                 in_authors_of_notes_index = True
#             if in_index_of_things is True:
#                 if first_entry_things is True:
#                     author_things_overlap_arr = re.split(r" A. ", entry)
#                     # split_authors = author_things_overlap_arr[0]
#                     split_things = author_things_overlap_arr[1]
                    
#                     for ent in split_things:
#                         book_number = roman_to_arabic[match[0]]
#                         if book_number is None:
#                             continue
#                         line_number = int(match[1])
#                         if (book_number, line_number) in processed_combinations:
#                             continue
#                         processed_combinations.add((book_number, line_number))
#                         edited_entry = re.sub(sub_pattern, '', entry).strip()
#                         edited_entry2 = re.sub(r"\.", '', edited_entry).rstrip()

#                         if in_authors_of_notes_index is not True and in_index_of_things is not True:
#                             index_hash.append(nodes.DunciadNode(
#                                 book_number=book_number,
#                                 line_number=line_number,
#                                 line=edited_entry2
#                             ))   


#                 first_entry_things = False

#             if in_authors_of_notes_index is True:
#                 edited_entry = re.sub(r'\b(B|B\.|B—|b|b.|v|v\.|Book|Verse|\.)\b', '', entry)
#                 split_entry = re.split(r'\s+|,|Mr|MR|Mr\.', edited_entry)

#                 def extract_rom_num_and_num(text):
#                     no_roms = re.sub(rom_num_pattern, "", text)
#                     no_roms_or_nums = re.sub(r'\d+', '', no_roms)
#                     nrnn = no_roms_or_nums
#                     return nrnn

#                 c_lines = []
#                 for ent in split_entry: 
#                     if ent is None:
#                         continue
#                     is_text = re.compile(r'\b(?!i{1,3}\b)[a-zA-Z]{2,}\b')
#                     is_rom = re.compile(r'\b[i]{1,3}\b')
#                     is_num = re.compile(r'^\d+(\.\d+)?$')
#                     if re.fullmatch(is_text, ent):
#                         last_entry = last_entry + ' ' + extract_rom_num_and_num(re.findall(is_text, ent)[0])
#                         curr_entry['text'] = last_entry
#                     if re.fullmatch(is_rom, ent):
#                         curr_entry['book'] = int(roman_to_arabic[re.findall(is_rom, ent)[0]])
#                     if re.findall(is_num, ent):
#                         for l in ent:
#                             if l is not None:
#                                 c_lines.append(int(l))
#                     if curr_entry['book'] is not None and len(c_lines) > 0 and curr_entry['text'] != "":
#                         l = int("".join(map(str,c_lines)))
#                         if l == "" or l is None:
#                             continue
#                         index_hash.append(nodes.DunciadNode(
#                             book_number= curr_entry['book'],
#                             line_number= l,
#                             line= curr_entry['text']
#                         ))
#                         last_line = None
#                         last_entry = ''
#                         c_lines = []
#                     else:
#                         continue
                    
#             if entry is None:
#                 continue
#             matches = re.findall(sub_pattern, entry)
#             for match in matches:
#                 if in_authors_of_notes_index is True:
#                     continue
#                 book_number = roman_to_arabic[match[0]]
#                 if book_number is None:
#                     continue
#                 line_number = int(match[1])
#                 if (book_number, line_number) in processed_combinations:
#                     continue
#                 processed_combinations.add((book_number, line_number))
#                 edited_entry = re.sub(sub_pattern, '', entry).strip()
#                 edited_entry2 = re.sub(r"\.", '', edited_entry).rstrip()

#                 if in_authors_of_notes_index is not True and in_index_of_things is not True:
#                     index_hash.append(nodes.DunciadNode(
#                         book_number=book_number,
#                         line_number=line_number,
#                         line=edited_entry2
#                     ))    
    
#         def split_entry(entry):
#             return re.split(r'\s*,\s*|\s+', entry)

#         await browser.close()

#         def chunker(seq, size):
#             return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#         # for i in chunker(scriblerus_data["dunciad_poem"], 30):
#         # for i in scriblerus_data["dunciad_poem"]:
#         #     # test = nlp(' '.join([j.line for j in i]))
#         #     test = nlp(i.line)
#         #     # tokenized_test = tokenizer(' '.join([j.line for j in i]), return_tensors="pt")
#         #     tokenized_test = tokenizer(i.line, return_tensors="pt")
#         #     # print("FUCKING TEST! ", test)
#         #     # print("FUGGING TOKENS TEST ", tokenized_test)
#         # #     entities = nlp(i.line)
#         # #     print("ENTITIES!!: ", entities)

#         return {
#             # "title": page_title, 
#             "dunciad_poem": scriblerus_data["dunciad_poem"],
#             "dunciad_summaries": scriblerus_data["dunciad_summaries"],
#             "dunciad_essays": sentences_dunciad_essays,
#             "dunciad_appendices": sentences_dunciad_appendices,
#             "dunciad_ftns": scriblerus_data["dunciad_ftns"], 
#             "dunciad_index": index_hash,
#             # "peri_bathous_data": scriblerus_data["peri_bathous_data"],
#             "pope_letters": scriblerus_data["pope_letters"]
#             # "content_2":scriblerus_data["peri_bathous_data"], 
#             # "content_3":scriblerus_data["memoirs_data"]
#         }

# if __name__ == "__main__":
#     import asyncio
#     # Call the scraping function
#     result = asyncio.run(initial_scrape())
#     pprint.pprint(result)