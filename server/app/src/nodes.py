# class DunciadNode:
#     def __init__(self, book_number, line_number, line):
#         self.book_number = book_number
#         self.line_number = line_number
#         self.line = line

#     def __eq__(self, other):
#         # Check if two nodes are equal (compare book_number and line_number)
#         return (self.book_number, self.line_number) == (other.book_number, other.line_number)

#     def __hash__(self):
#         # Hash the node based on book_number and line_number
#         return hash((self.book_number, self.line_number))

#     def __repr__(self):
#         # String representation of the object for debugging
#         return f"Book {self.book_number}, Line {self.line_number}: {self.line}"

class POS_Datum:
    def __init__(self, token, pos):
        self.token = token
        self.part_of_speech = pos
         
class PoemNode:
    def __init__(self, book_number, line_number, line):
        self.book_number = book_number
        self.line_number = line_number
        self.line = line

    def __eq__(self, other):
        # Check if two nodes are equal (compare book_number and line_number)
        return (self.book_number, self.line_number) == (other.book_number, other.line_number)

    def __hash__(self):
        # Hash the node based on book_number and line_number
        return hash((self.book_number, self.line_number))

    def __repr__(self):
        # String representation of the object for debugging
        return f"Book {self.book_number}, Line {self.line_number}: {self.line}"

class PoemAnnotationNode:
    def __init__(self, book_number, line_number, text):
        self.book_number = book_number
        self.line_number = line_number
        self.text = text

    def __eq__(self, other):
        # Check if two nodes are equal (compare book_number and line_number)
        return (self.book_number, self.line_number) == (other.book_number, other.line_number)

    def __hash__(self):
        # Hash the node based on book_number and line_number
        return hash((self.book_number, self.line_number))

    def __repr__(self):
        # String representation of the object for debugging
        return f"Book {self.book_number}, Line {self.line_number}: {self.text}"
    
class PlayNode:
    def __init__(self, id, act_number, scene_number, speaker, characters_present, line, is_stage_direction):
        self.id = id
        self.act_number = act_number
        self.scene_number = scene_number
        self.speaker = speaker
        self.characters_present = characters_present
        self.line = line
        self.is_stage_direction = is_stage_direction

    def __eq__(self, other):
        # Check if two nodes are equal (compare book_number and line_number)
        return (self.id) == (other.id)

    def __hash__(self):
        # Hash the node based on book_number and line_number
        return hash((self.id))

    def __repr__(self):
        # String representation of the object for debugging
        return f"Act {self.act_number}, Scene {self.scene_number}, SPEAKER: {self.speaker}, CHARACTERS PRESENT: {self.characters_present}, LINE: {self.line} / is stage direction? {self.is_stage_direction}"

class GeneralNode:
    def __init__(self, title, identifier, text):
        self.title = title
        self.identifier = identifier
        self.text = text

    def __eq__(self, other):
        # Check if two nodes are equal (compare book_number and line_number)
        return (self.tile, self.identifier) == (other.title, other.identifier)

    def __hash__(self):
        # Hash the node based on book_number and line_number
        return hash((self.title, self.identifier))

    def __repr__(self):
        # String representation of the object for debugging
        return f"Book {self.title}, Line {self.identifier}: {self.text}"

class ShortGeneralNode:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __eq__(self, other):
        # Check if two nodes are equal (compare book_number and line_number)
        return self.title == other.title

    def __hash__(self):
        # Hash the node based on book_number and line_number
        return hash(self.title)

    def __repr__(self):
        # String representation of the object for debugging
        return f"Book {self.title}: {self.text}"


class ChapterProseNode:
    def __init__(self, id, chapter_number, subtitle, text, annotation=None ):
        self.id = id
        self.chapter_number = chapter_number
        self.subtitle = subtitle
        self.text = text
        self.annotation = annotation

    def __eq__(self, other):
        # Check if two nodes are equal (compare book_number and line_number)
        return (self.chapter_number, self.id) == (other.chapter_number, other.id)

    def __hash__(self):
        # Hash the node based on book_number and line_number
        return hash((self.chapter_number, self.id))

    def to_dict(self, id, chapter_number, subtitle, text, annotation=None):
        return {
            self.id : id,
            self.chapter_number: chapter_number,
            self.subtitle: subtitle,
            self.text: text,
            self.annotation: annotation
        }

    def __repr__(self):
        # String representation of the object for debugging
        return f"Book {self.chapter_number}, Line {self.subtitle}: {self.text}"

import re

# Function to convert Roman numerals to integers
roman_to_int = {
    'i': 1,
    'ii': 2,
    'iii': 3
}

# Regex patterns for Roman numerals, line numbers, and ibid
roman_numeral_pattern = r'\b(i|ii|iii)\b'  # Matches 'i', 'ii', 'iii'
line_number_pattern = r'\d+'  # Matches digits (line numbers)
ibid_pattern = r'\bIbid\b'  # Matches 'Ibid'

# Function to create the hash object with nested dictionary structure
def create_hash_object(text):
    hash_obj = {}
    last_book = None
    last_line_numbers = []

    # Split entries by lines for simplicity
    entries = text.splitlines()

    for entry in entries:
        # Remove leading/trailing whitespace
        entry = entry.strip()

        # Check for Roman numerals and line numbers
        roman_numerals = re.findall(roman_numeral_pattern, entry)
        line_numbers = re.findall(line_number_pattern, entry)

        # If "Ibid." is found, use the last book and line numbers
        if re.search(ibid_pattern, entry):
            for ln in last_line_numbers:
                if last_book not in hash_obj:
                    hash_obj[last_book] = {}
                if ln not in hash_obj[last_book]:
                    hash_obj[last_book][ln] = []
                hash_obj[last_book][ln].append(entry)
        else:
            # Convert Roman numerals to integers and store them with line numbers
            if roman_numerals and line_numbers:
                for rn in roman_numerals:
                    # print("WTF RN? ", rn)
                    book_number = roman_to_int[rn]
                    last_book = book_number  # Remember last book
                    last_line_numbers = line_numbers  # Remember last line numbers
                    for ln in line_numbers:
                        ln = int(ln)  # Ensure line number is an integer
                        if book_number not in hash_obj:
                            hash_obj[book_number] = {}
                        if ln not in hash_obj[book_number]:
                            hash_obj[book_number][ln] = []
                        hash_obj[book_number][ln].append(entry)
                        
    return hash_obj

