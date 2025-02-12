class Person:
    def __init__(self, name, works, association):
        self.name = name
        self.works = works
        self.associations = []

class Work:
    def __init__(self, title, author, critical_intro, sections, genres):
        self.title = title
        self.author = author
        self.critical_intro = critical_intro or None
        self.sections = sections or []
        self.genres = genres or []

class Section:
    def __init__(self, title, work, author, is_secondary, lines, speaker, addressee):
        self.title = title
        self.lines = lines
        self.work = work
        self.author = author
        self.is_secondary = is_secondary
        self.speaker = speaker
        self.addressee = addressee

class Line:
    def __init__(self, id, text, tokenized_text, section, work, author, annotation, pos_data, stresses, phonemes, speaker, addressee, mentions, sentiment):
        self.id = id
        self.text = text
        self.tokenized_text = tokenized_text
        self.section = section
        self.work = work
        self.author = author
        self.annotation = annotation
        self.pos_data = pos_data
        self.stresses = stresses
        self.phonemes = phonemes
        self.speaker = speaker
        self.addressee = addressee
        self.mentions = mentions
        self.sentiment = sentiment

class GenericNode:
    def __init__(self, id, type, label, info, data):
        self.id = id
        self.type = type
        self.label = label
        self.info = info
        self.data = data
