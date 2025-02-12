from sentence_transformers import SentenceTransformer

transformer = SentenceTransformer("all-MiniLM-L6-v2")

def embed_entry():
# Add the data you want to be embedded
    
    # embed = "title {} by author {} in school {} reads as {} and is tokenized as {}. it was published in {}".format(
    #     data["title"],
    #     data["author"],
    #     data["school"],
    #     data["sentence_str"],
    #     # data["sentence_lowered"],
    #     data["tokenized_txt"],
    #     data["original_publication_date"],
    #     # data["corpus_edition_date"],
    #     # data["sentence_length"],
    # )

    embed = ["This is an example sentence", "Each sentence is converted"]

    embeddings = transformer.encode(embed)
    return embeddings