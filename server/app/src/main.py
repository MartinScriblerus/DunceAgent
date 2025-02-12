
import asyncio
from urllib.request import urlopen
import sys
from fastapi import APIRouter, FastAPI, Request
import pandas as pd
import re
from dateutil import parser
import numpy as np
# import pprint
# # from sentence_transformers import SentenceTransformer
# import json
from tqdm import tqdm
# import opendatasets as od
from datasets import load_dataset
import os
import json 
from pathlib import Path
from dotenv import dotenv_values
# import zipfile
# from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pydantic import BaseModel
from playwright.async_api import async_playwright

from playwright.async_api import async_playwright
import nltk
nltk.download('punkt')
# try:
#     nltk.data.find('taggers/averaged_perceptron_tagger')
# except LookupError:
#     nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import sent_tokenize

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification, pipeline

# Load tokenizer and model for NER
tokenizer = AutoTokenizer.from_pretrained("MrRobson9/distilbert-base-cased-finetuned-conll2003-english-ner")
model = AutoModelForTokenClassification.from_pretrained("MrRobson9/distilbert-base-cased-finetuned-conll2003-english-ner")
ner_pipeline = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", aggregation_strategy="simple")
# ner_tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
# ner_model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
# # ner_model_name="distilbert-base-cased"

# # Set up NER pipeline
# ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

# Load tokenizer and model for sentiment analysis
sentiment_tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
sentiment_model = AutoModelForSequenceClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")

# Set up sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)

# # Specify the exact model and revision
# ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
# model_name = "RoBERTa-base"
# nlp = pipeline("ner", model=ner_model_name, tokenizer=ner_model_name)

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# inputs = tokenizer("Your input text here", return_tensors="pt")

import server.app.src.peri_bathous_scraper as peri_bathous_scraper
import server.app.src.scraper as scraper
import server.app.src.pope_letters_scraper as pope_letters_scraper
import server.app.src.memoirs_scriblerus_scraper as memoirs_scriblerus_scraper
import server.app.src.threebk_dunciad_scraper as threebk_dunciad_scraper
import server.app.src.elwin_popeworks_scraper as elwin_popeworks_scraper
import server.app.src.three_hours_scraper as three_hours_scraper
import server.app.src.moral_essays_scraper as moral_essays_scraper
import server.app.src.iliad_odyssey_scraper as iliad_odyssey_scraper
import server.app.src.volume_one_scraper as volume_one_scraper
import server.app.src.swift_tub_scraper as swift_tub_scraper
import server.app.src.swift_gulliver_scraper as swift_gulliver_scraper
import server.app.src.beggars_opera_scraper as beggars_opera_scraper
import server.app.src.miscellanies_scraper as miscellanies_scraper
import server.app.src.swift_miscellanies_scraper as swift_miscellanies_scraper

sys.path.append('./')
dir_path = os.path.dirname(os.path.realpath(__file__))
print("WHAT IS DIRPATH? ", dir_path)
# import meltano_api as meltano

config = dotenv_values(".env")

from sqlalchemy import create_engine, ForeignKey, String, MetaData, text
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship, relationship
from typing import List
# from typing import Optional

# print("Current working directory:", os.getcwd())
# print("Python search paths:", sys.path)

import tracemalloc

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(30))

  addresses: Mapped[List["Address"]] = relationship(
    back_populates="users", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"User(id={self.id!r}, name={self.name!r} )"

class Address(Base):
  __tablename__ = "addresses"

  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str]
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  users: Mapped["User"] = relationship(back_populates="addresses")

  def __repr__(self) -> str:
    return f"Address(id={self.id!r}, email_address={self.email!r})"

conn_url = 'postgresql+psycopg2://warehouse:warehouse@warehouse_db/warehouse'

engine = create_engine(conn_url)

db = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)
# MetaData.create_all()

# ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
# model_name = "RoBERTa-base"
# Load tokenizer and model for NER
# ner_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
# ner_model = AutoModelForTokenClassification.from_pretrained("distilbert-base-cased")

# # Set up NER pipeline
# ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

# Load tokenizer and model for sentiment analysis
sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Set up sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)
# nlp = pipeline("ner", model=ner_model_name, tokenizer=ner_model_name)

def add_user_with_email(name, email):
  new_user = User()
  new_address = Address()
  new_address.email = email

  user_exists = db.query(User).filter(User.name == name).all()
  print("user exists: ", user_exists)
  # add_user_with_email('MartinScriblerus', 'matthewfreilly@gmail.com')

  if (user_exists is not True):
    print("USER EXISTS: ", user_exists)
    # Link the address to the user
    # new_user.addresses.append(new_address)
    # new_user.name = name
    # db.add(new_user)
    # db.add(new_address)
    # db.commit()
    db.close()
  db.close()

# # Update addresses to set user_id to NULL
# db.execute(text("UPDATE addresses SET user_id = NULL WHERE user_id = :user_id"), {'user_id': Address.user_id})

# # Then delete the user
# db.execute(text("DELETE FROM users WHERE id = :user_id"), {'user_id': Address.user_id})

# db.commit()

# db.execute(text("DELETE FROM users"))
# db.execute(text("DELETE FROM users"))



query_rows = db.execute(text("SELECT * FROM users, addresses")).fetchall()
for register in query_rows:
    print(f"{register} ")
    # Note that this Python way of printing is available in Python3 or more!!



class VectorDb(BaseModel):
  dbName: str

# your api key
# api_key = {
# 'username': 'matthewreilly',
# 'key': '86c59f355c3b0dd930eb57335cc99c4a'
# }

# from kaggle.api.kaggle_api_extended import KaggleApi
# api = KaggleApi()
# api.authenticate()

from pydantic import BaseModel
app = FastAPI(debug=True)   
api_router = APIRouter()

from starlette.middleware.cors import CORSMiddleware

# app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/") 
async def main_route():
  #  add_user_with_email('MartinScriblerus', 'matthewfreilly@gmail.com')

  return {"message": "hello"}
  # # result = await scraper.initial_scrape()  # Call the function from script.py
  # # print({"result": result})  
  # # result = await scraper.initial_scrape()  # Call the function from script.py
  # # print({"result": result})  
  # dataset = 'kouroshalizadeh/history-of-philosophy'
  
  # # download single file
  # # Signature: dataset_download_file(dataset, file_name, path=None, force=False, quiet=True)
  # # TODO: Get the Dataset URL from user & recursively search page for .csv file
  # api.dataset_download_file(dataset, "philosophy_data.csv", path="imported_datasets/kaggle/zip")

  # # client = QdrantClient("localhost", port=6333)
  # client = QdrantClient("http://qdrant:6333")
  # client.recreate_collection(
  #     collection_name="philosophers_collection",
  #     vectors_config=VectorParams(size=768,distance=Distance.DOT),
  # )

  # for i in os.listdir("imported_datasets/kaggle/zip/"):
  #   print("kaggle_test ", i)
  #   if (i == "test"):
  #     continue

  #   # base_zip="imported_datasets/kaggle/zip"
  #   # base_csv="imported_datasets/kaggle/csv"
  #   # filename_csv=i.replace(".zip","")
  #   # filename_zip=f"{base_zip}/{i}"
  #   # # # loading the temp.zip and creating a zip object
  #   # #for i in filenames_zip:
    
  #   # try:
  #   #   if i.index(".zip") != -1:
  #   #     print("try with ", i)
  #   #     with zipfile.ZipFile(f"{filename_zip}", 'r') as zObject:
  #   #       zObject.extractall("/" + base_csv)
  #   #       print("success!! ")
  #   #       print("check filename: ", base_csv + "/" + filename_csv)
  #   #       df = pd.read_csv("/" + base_csv + "/" + filename_csv)
  #   #       print('df shape', df.shape)
  #   #       print('df columns', df.columns)
  #   #       # # sentence transformer
  #   #       model = SentenceTransformer('distilbert-base-nli-mean-tokens')

  #   #       # author_sentence_matrix = df[['author', 'tokenized_txt']].to_numpy()[10:]
  #   #       sentence_matrix = [str(i) for i in df['tokenized_txt'].to_numpy()][:10000]
  #   #       # label_matrix = [i for i in df['school'][:10].to_numpy()]

  #   #       print("test matrix: ", len(sentence_matrix))

  #   #       embeddings = model.encode(sentence_matrix)

  #   #       print("YO EMBEDDINGS: ", len(embeddings))

  #   #       points_to_upsert = []
  #   #       for idx, i in enumerate(embeddings):
  #   #         print("ug idx ", idx)
  #   #         points_to_upsert.append(PointStruct(id=idx, vector=i, payload={
  #   #           #  "title": df["title"][idx],
  #   #           #  "author": df["author"][idx],
  #   #           "school": df["school"][idx],
  #   #           #  "sentence_str": df["sentence_str"][idx],
  #   #           #  "original_publication_date": df["original_publication_date"][idx]
  #   #         }))
  #   #       print("PTU: ", points_to_upsert)

  #   #       for chunk in np.array_split(points_to_upsert, 5):
  #   #         print("CHUNK??? ", chunk)
  #   #       operation_info = client.upsert(
  #   #           collection_name="philosophers_collection",
  #   #           wait=True,
  #   #           points=points_to_upsert,
  #   #       )

  #   #       print("OP INFO: ", operation_info)
  #   #     zObject.close()
  #   # except:
  #   #    print("FAIL!", i)
 

  # return {"message": "hello"}

from typing import Any
import numpy as np

def convert_to_serializable(obj: Any):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.float32):
        return float(obj)
    elif hasattr(obj, '__dict__'):
        return vars(obj)
    return obj

def flatten_object(obj, prefix=''):
    result = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f'{prefix}{key}.' if prefix else f'{key}.'
            result.extend(flatten_object(value, new_prefix))
    else:
        result.append(f'{prefix}{obj}')
    return result

peri_bathous_url_identifier = 'Art_of_Sinking_In_Poetry'
pope_letters_url_identifier = 'idno=004809116.0001.002'
memoirs_scriblerus_url_identifier = 'idno=004809278.0001.000'
dunciad_url_identifier = 'idno=004809160.0001.000'
elwin_popeworks_url_identifier = '43271-h.htm#Footnote_73_73'
three_hours_url_identifier = 'pg37667-images.html'
moral_essays_url_identifer = 'pg2428-images.html'
iliad_odyssey_url_identifier = 'pg6130-images.html'
volume_one_url_identifier = 'pg32190-images.html'
tale_of_a_tub_url_identifier = 'pg4737-images.html'
gulliver_url_identifier = '829-h/829-h.htm'
beggars_opera_url_identifier = 'pg2421-images.html'
miscellanies_url_identifier = 'idno=004898469.0001.000'
swift_miscellanies_url_identifier = 'pg623-images.html'

async def scrape_page(scrape_method, url):
  async with async_playwright() as p:
    # global scriblerus_data
    # scriblerus_data = {
    #     'pope_letters': []
    # }
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    await page.goto(url)
    if pope_letters_url_identifier in url:
      button_xpath = '//*[@id="maincontent"]/div[2]/div/div/div/a'
      await page.locator(button_xpath).click()
    elif memoirs_scriblerus_url_identifier in url:
      memoirs_button_xpath = '//*[@id="maincontent"]/div[2]/div/div/div/a'
      await page.locator(memoirs_button_xpath).click()
    elif dunciad_url_identifier in url:
      dunciad_button_xpath = '//*[@id="maincontent"]/div[2]/div/div/div/a'
      await page.locator(dunciad_button_xpath).click()
    elif miscellanies_url_identifier in url:
      miscellanies_button_xpath = '//*[@id="maincontent"]/div[2]/div/div/div/a'
      await page.locator(miscellanies_button_xpath).click()
    await page.wait_for_load_state('networkidle', timeout=60000)
    await page.set_extra_http_headers({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    
    if pope_letters_url_identifier in url:
      divs = await page.query_selector_all('p, h4')
    elif peri_bathous_url_identifier in url:
      divs = await page.query_selector_all('p')
    elif memoirs_scriblerus_url_identifier in url:
      divs = await page.query_selector_all('.fullview-main')
    elif dunciad_url_identifier in url:
      divs = await page.query_selector_all('.fullview-main')
    elif elwin_popeworks_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif three_hours_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif moral_essays_url_identifer in url:
      divs = await page.query_selector_all('body')
    elif iliad_odyssey_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif volume_one_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif tale_of_a_tub_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif gulliver_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif beggars_opera_url_identifier in url:
      divs = await page.query_selector_all('body')
    elif miscellanies_url_identifier in url:
      divs = await page.query_selector_all('#maincontent')
    elif swift_miscellanies_url_identifier in url:
      divs = await page.query_selector_all('body')
    
    # if dunciad_url_identifier in url or elwin_popeworks_url_identifier in url or pope_letters_url_identifier in url or memoirs_scriblerus_url_identifier:
    content = await scrape_method(divs, sent_tokenize)
    # else:
    #   content = await scrape_method(divs)
    await browser.close()
    return content

@app.get("/scrape_pope_letters")
async def scrape_pope_letters():
  tracemalloc.start()

  scrape_methods = [
    pope_letters_scraper.scraper_pope_letters,
  ]

  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_pope_letters)]  
  all_tasks = await asyncio.gather(*tasks)

  snapshot = tracemalloc.take_snapshot()
  top_stats = snapshot.statistics('lineno')
  for stat in top_stats[:10]:
    print('MEMORY STAT!::: ', stat)

  return {"pope_letters_scrapes": all_tasks}

@app.get("/scrape_pope_iliad")
async def scrape_pope_iliad():
  tracemalloc.start()

  scrape_methods = [
    iliad_odyssey_scraper.scraper_iliad_odyssey,
  ]

  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_iliad)]  
  all_tasks = await asyncio.gather(*tasks)

  snapshot = tracemalloc.take_snapshot()
  top_stats = snapshot.statistics('lineno')
  for stat in top_stats[:10]:
    print('MEMORY STAT!::: ', stat)

  return {"pope_iliad": all_tasks}

@app.get("/scrape_pope_second")
async def scrape_pope_second():
  tracemalloc.start()

  scrape_methods = [
    moral_essays_scraper.scraper_moral_essays,
    volume_one_scraper.scraper_volume_one, # Elwin / Croker vol. 1 => ToF, Pastorals, 
  ]

  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_pope_second_scrape)]  
  all_tasks = await asyncio.gather(*tasks)

  return {"pope_vol1_moral": all_tasks}

@app.get("/scrape_scriblerian_collaborators_second")
async def scrape_scriblerian_collaborators_second():
  scrape_methods = [
    miscellanies_scraper.scraper_miscellanies,
    swift_miscellanies_scraper.scraper_swift_miscellanies,
  ]
  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_scriblerian_collaborators_second)]
  all_tasks = await asyncio.gather(*tasks)
  print("all tasks.... ", all_tasks)
  return {"scrib_collabs_miscellanies": all_tasks}

@app.get("/scrape_dunciad")
async def scrape_dunciad():
  scrape_methods = [
    threebk_dunciad_scraper.scraper_dunciad,
  ]
  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_dunciad)]

  all_tasks = await asyncio.gather(*tasks)
  print("all tasks.... ", all_tasks)
  return {"pope_major_works_scrapes": all_tasks}

@app.get("/scrape_dramatic_scriblerian_collaborators")
async def scrape_dramatic_scriblerian_collaborators():
  scrape_methods = [
    beggars_opera_scraper.scraper_beggars_opera,
    three_hours_scraper.scraper_three_hours,
  ]

  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_dramatic)]

  all_tasks = await asyncio.gather(*tasks)
  print("all tasks.... ", all_tasks)
  return {"scrib_collabs_dramatic": all_tasks}

@app.get("/scrape_scriblerian_collaborators")
async def scrape_scriblerian_collaborators():
  scrape_methods = [
    swift_tub_scraper.scraper_tale_of_a_tub,
    swift_gulliver_scraper.scraper_gulliver,
  ]

  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_scriblerian_collaborators)]

  all_tasks = await asyncio.gather(*tasks)
  print("all tasks.... ", all_tasks)
  return {"swift_major_works": all_tasks}

@app.get("/scrape_major_works")
async def scrape_major_works():
  scrape_methods=[
    elwin_popeworks_scraper.scraper_elwin_popeworks,
    memoirs_scriblerus_scraper.scraper_memoirs_scriblerus,
  ]
  tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls_major_works)]

  all_tasks = await asyncio.gather(*tasks)
  print("all tasks.... ", all_tasks)
  return {"pope_major_works": all_tasks}


global all_sentiment_entity_items
all_sentiment_entity_items = []

@app.post("/extend_peri_bathous")
async def extend_peri_bathous(data: Request):
  json_data = await data.json()  # Extract JSON data
  # print("HIT THE EXTEND", json_data)
  # entities=ner_pipeline("".join(json_data[0]['data']))
  for d in json_data[0]['data']:
    # print("SANNITY!!! ", d)
    # entities=ner_pipeline(d)
    # print("SANNITY ENTITIES!!! ", entities)
    edited_lines = re.findall(r'CHAP\.\s([IVX]{1,4})', d)
    chapter_header_to_remove = re.findall(r'CHAP', d)
    rom_pat = r'\b(I{1,3}|IV|V?I{0,3}|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX|XXI|XXII|XXIII|XXIV)\b'
    found_edited_lines = re.findall(rom_pat, edited_lines)
    
    if edited_lines or found_edited_lines or chapter_header_to_remove:
        continue
    sentiment = sentiment_pipeline(d)
    # human_readable_entities = []
    # current_entity = ""
    # for token in entities:
    #   # for token in entity:
    #   entity_type = token["entity"]
    #   word = token["word"].replace("Ġ", " ")  # Remove the 'Ġ' indicating a new word
      
    #   if word.startswith("##"):
    #       current_entity +=  word.replace("##", "")
    #   else:
    #     if current_entity:
    #       print("curr ent ", current_entity)
    #       human_readable_entities.append((current_entity, entity_type))
          
    #       # current_entity = token["word"]
    #       # entity_type = token["entity"]
    # print("ENT ENT ENTITIES: ", entities)
    # serializable_results = [convert_to_serializable(res) for res in entities]
    # if type(entities) is 'dict':
    #   entities = float(entities) 
    all_sentiment_entity_items.append({
      "text": d,
      "sentiment": sentiment,
    })

  return all_sentiment_entity_items  # Send JSON data back as response (for testing)

@app.get("/scrape_peri_bathous")
async def scrape_peri_bathous():
  # tracemalloc.start()

  # dataset = load_dataset("deepmind/pg19", trust_remote_code=True)
  # Load dataset in streaming mode (no full download)

  
  # dataset = load_dataset("deepmind/pg19", split="train", streaming=True)
  # pope_pattern = r'Pope'
  # # # Use the dataset's filtering capabilities
  # # Filter the dataset on-the-fly
  # filtered_data = dataset.filter(lambda x: x['publication_date'] == 1728)
  # # filtered_data = (example for example in dataset if re.findall(pope_pattern, str(example['text']), re.IGNORECASE) and example['publication_date'] == 1728)

  # # Iterate over the filtered examples
  # for example in filtered_data:
  #     print("YO DATA!!! ", example)  # Process only the matching records


  # # Iterate over examples without loading the entire dataset
  # for example in dataset:
  #     # Process each example as it streams in
  #     print(example)

  # # Access the train split
  # train_data = dataset['train']

  # # Peek at the first example
  # print("YO TRAINING! ", train_data[0].filter(lambda x: x['publication_date'] == 1728))
  # print("HEY IN PY....")
  
  
  
  ################################################################
  dataset = load_dataset("mscriblerus/scriblerus_data")

  # Convert each split (e.g., train) to a dictionary and then to JSON
  train_data = dataset['train'].to_dict()

  # Convert to a JSON string for easy inspection (optional)
  train_json = train_data
  # print("hey train datasewt: ", train_dataset, flush=True)

  if train_json is not None:
    print("CHECK RETURN HERE ", train_json)
    return {"peri_bathous": train_json}
  ################################################################
  
  
  else:
    scrape_methods = [
        peri_bathous_scraper.scraper_peri_bathous,  # This should also be an async function
    ]


    # # Perform concurrent scraping tasks
    tasks = [scrape_page(method, url) for method, url in zip(scrape_methods, urls)]
    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics('lineno')

    # for stat in top_stats[:10]:
    #     print('MEMORY STAT!::: ', stat)
    # # Wait for all tasks to complete
    all_tasks = await asyncio.gather(*tasks)
    return {"peri_bathous": all_tasks}


urls = [
   'https://en.wikisource.org/wiki/The_Works_of_the_Rev._Jonathan_Swift/Volume_17/Martinus_Scriblerus,_or_the_Art_of_Sinking_In_Poetry', # Peri Bathous
]

urls_dunciad = [
  'https://quod.lib.umich.edu/cgi/t/text/text-idx?c=ecco;cc=ecco;rgn=main;view=text;idno=004809160.0001.000', # 3-book Dunciad
]

urls_dramatic = [
  'https://www.gutenberg.org/cache/epub/2421/pg2421-images.html', #beggar's opera
  'https://www.gutenberg.org/cache/epub/37667/pg37667-images.html', # Three Hours After Marriage
]

urls_iliad = [
  'https://www.gutenberg.org/cache/epub/6130/pg6130-images.html', #iliad
]

urls_major_works = [
    'https://www.gutenberg.org/files/43271/43271-h/43271-h.htm#Footnote_73_73', # Elwin's edition (EoC, RoL, EoM)
  'https://quod.lib.umich.edu/cgi/t/text/text-idx?c=ecco;idno=004809278.0001.000',  #Scriblerus's Memoirs
  # 'https://quod.lib.umich.edu/cgi/t/text/text-idx?c=ecco;cc=ecco;rgn=main;view=text;idno=004809160.0001.000', # 3-book Dunciad
  # 'https://www.gutenberg.org/files/43271/43271-h/43271-h.htm#Footnote_73_73', # Elwin's edition (EoC, RoL, EoM)
]

urls_pope_letters = [
    'https://quod.lib.umich.edu/cgi/t/text/text-idx?c=ecco;cc=ecco;rgn=main;view=text;idno=004809116.0001.002', # Pope letters (1735?)
]

urls_pope_second_scrape = [
  'https://www.gutenberg.org/cache/epub/2428/pg2428-images.html', #moral essays
  'https://www.gutenberg.org/cache/epub/32190/pg32190-images.html', # volume 1 (ToF, Pastorals)
  # 'https://www.gutenberg.org/cache/epub/2428/pg2428-images.html', #moral essays
]

urls_scriblerian_collaborators = [
  'https://www.gutenberg.org/cache/epub/4737/pg4737-images.html', #a tale of a tub
  'https://www.gutenberg.org/files/829/829-h/829-h.htm', #gulliver's travels
]

urls_scriblerian_collaborators_second = [
  'https://quod.lib.umich.edu/cgi/t/text/text-idx?c=ecco;idno=004898469.0001.000', #miscellanies in one vol
  'https://www.gutenberg.org/cache/epub/623/pg623-images.html', # swift miscellanies
]

@app.post("/createvectordb/")
async def createvectordb(dbName: VectorDb):
  # result = await scraper.initial_scrape()  # Call the function from script.py
  # print({"result": result})  
  newpath = '/{dbName}/data' 
  print("new path: ", newpath)
  if not os.path.exists(newpath):
    os.makedirs(newpath)
  # else:
  #   return {"messageReturn": "already_exists"}  
  print("dbName1: ", dbName)
  print("does newpath exist? ", os.path.exists(newpath))
  result = await scraper.initial_scrape()  # Call the function from script.py

  return {"messageReturnuzuz": dbName}

@app.get("/initial_scrape")
async def initial_scrape():
  return {}
  # result = await scraper.initial_scrape()  # Call the function from script.py
  # print({"scrape_result": result})  
  # data = {
  #   "message": "Hello, in INIT SCRAPE!",
  #   "success": True
  # }
  # return data
