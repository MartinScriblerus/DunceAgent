import pprint
from bs4 import BeautifulSoup
import re
from memory_profiler import profile
import time

import server.app.src.nodes as nodes

def month_name_to_number(month):
    if month in 'January':
        return 1 
    elif month in 'February':
        return 2
    elif month in 'March':
        return 3
    elif month in 'April':
        return 4
    elif month in 'May':
        return 5
    elif month in 'June':
        return 6
    elif month in 'July':
        return 7
    elif month in 'August':
        return 8
    elif month in 'September':
        return 9
    elif month in 'October':
        return 10
    elif month in 'November':
        return 11
    elif month in 'December':
        return 12
    else:
        print(f"Invalid month: {month}")
        return None


# @profile
async def scraper_pope_letters(divs, sent_tokenize):
    start = time.time()
    print("in pope letters -> scrape")
    global scriblerus_data
    scriblerus_data = {
        'pope_letters': []
    }

    date_matcher = r'\b([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})\b'

    global last_div
    last_div = ''
    global recipient
    recipient = ''
    global last_date
    last_date = ''
    global last_addressee
    last_addressee = ''
    global last_sender 
    last_sender = ''

    for div in divs:
        content_text = await div.inner_text()
        pope_letters_unparsed = BeautifulSoup(content_text, "html.parser")
        soup_pope_letters = pope_letters_unparsed.get_text()
        soup_pope_letters = re.sub(r'\s+', ' ', soup_pope_letters).strip()
        soup_pope_letters = re.sub(r'To the extent possible under law, the Text Creation Partnership has waived all copyright and related or neighboring rights to this keyboarded and encoded edition of the work described above, according to the terms of the CC0 1.0 Public Domain Dedication (http://creativecommons.org/publicdomain/zero/1.0/). This waiver does not extend to any page images or other supplementary files associated with this work, which may be protected by copyright or other license restrictions. Please go to http://www.lib.umich.edu/tcp/ecco/ for more information', '', soup_pope_letters)

        tag_name = await div.evaluate('(element) => element.tagName.toLowerCase()')
        class_name = await div.get_attribute('class')

        if tag_name == 'h4':
            last_div += soup_pope_letters

        last_date_in_text = re.findall(date_matcher, soup_pope_letters)
        if last_date_in_text and class_name and 'indentlevel1' in class_name.split():
            recipient = last_div
            last_date = last_date_in_text[0]
            last_div = ''

        if last_date and len(last_date) == 3:
            last_date_to_string = str(month_name_to_number(last_date[0])) + "_" + last_date[1] + "_" + last_date[2]
        
            # lines = re.split(r'\n', soup_pope_letters)
            lines = sent_tokenize(soup_pope_letters, "english")
            match_addressee = re.findall(r'[Tt]o\s*(.*)', recipient)
            match_sender = re.findall(r'(.*)\s*to Mr\. POPE', recipient)
            the_same = r"the\s[Ss]ame"
            got_the_same_match = re.findall(the_same, recipient)
            if got_the_same_match:
                recipient = re.sub(got_the_same_match[0], last_addressee, recipient)
            if match_sender:
                last_sender = match_sender[0]
            elif match_addressee:
                last_addressee = match_addressee[0]
            if recipient == r"Mr. POPE's Answer.":
                recipient = f"Mr. POPE's Answer to {last_sender}"
            for line in lines:
                line = re.sub(r'\|', '', line)
                if len(line) < 1 or line == ".":
                    continue
                scriblerus_data['pope_letters'].append(nodes.GeneralNode(
                    title = recipient,
                    identifier = last_date_to_string,
                    text=line
                ))
        last_div = soup_pope_letters
    print(f"Elapsed time in Pope Letters: {time.time() - start} seconds")
    return scriblerus_data['pope_letters']

# if __name__ == "__main__":
#     import asyncio
#     result = asyncio.run(scraper_pope_letters())
#     pprint.pprint(result)