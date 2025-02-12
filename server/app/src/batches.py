# import tqdm as tdqm
# import app.src.embeddings as embeddings
# import pymilvus as pymilvus

# import pprint as pprint
# import pandas as pd 
# import numpy as np

# games_dict = pd.DataFrame.replace(np.nan, "Unknown").to_dict("records")  
# # It doesn't accept nan values
# j = 0
# batch = []

# for game_dict in tdqm(games_dict):
#     try:
#         game_dict["embedding"] = embeddings.embed_entry(game_dict)
#         batch.append(game_dict)
#         j += 1
#         if j % 5 == 0:
#             print("Embedded {} records".format(j))
#             pymilvus.Collection.insert(batch)
#             print("Batch insert completed")
#             batch = []
#     except Exception as e:
#         print("Error inserting record {}".format(e))
#         pprint(batch)
#         break

# pymilvus.Collection.insert(game_dict)
# print("Final batch completed")
# print("Finished with {} embeddings".format(j))