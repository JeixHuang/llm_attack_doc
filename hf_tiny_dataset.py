import pandas as pd
from datasets import Dataset,Image
import time
import os
os.environ['HF_API_TOKEN'] = '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'
# from transformers import CLIPModel
 
# model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14", from_tf=True)
df = pd.read_csv("CMIC/3MAD-Tiny-1K.csv")

# Get unique attribute values
attributes = df["original_attribute"].unique()

# Create a Hugging Face Dataset for each attribute value
for attribute in attributes:
    print(attribute)
    time.sleep(15)

    attribute_dataset = Dataset.from_pandas(df[df["original_attribute"] == attribute])
    attribute_dataset = attribute_dataset.map(lambda example: {"image": example["file_name"]}, batched=True)
    attribute_dataset = attribute_dataset.cast_column("image", Image())
    split_name = attribute.replace(" and ", "_")
    print(split_name)
    attribute_dataset.push_to_hub(
        "MedMLLM-attack/3MAD-Tiny-1K", split=split_name, max_shard_size="1GB"
    )