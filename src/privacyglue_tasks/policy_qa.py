#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from glob import glob
from typing import Any, Dict, List

import datasets
import pandas as pd

from dataset.templates import PATTERNS

def load_policy_qa(directory: str) -> datasets.DatasetDict:
    # define DatasetDict for data storage
    combined = datasets.DatasetDict()

    # loop over JSON files
    for json_file in glob(os.path.join(directory, "*.json")):
        # infer split from filename
        filename = os.path.basename(json_file)
        split = (
            "validation"
            if filename.startswith("dev")
            else filename.replace(".json", "")
        )

        # define temporarily dictionary
        temp_dict: Dict[str, List[Any]] = {
            "id": [],
            "title": [],
            "context": [],
            "question": [],
            "label": [],
            "text": []
        }

        # read JSON file
        with open(json_file, "r") as input_file_stream:
            dataset = json.load(input_file_stream)

        # loop over data and save to dictionray
        for article in dataset["data"]:
            title = article["title"]
            for paragraph in article["paragraphs"]:
                context = paragraph["context"]
                for qa in paragraph["qas"]:
                    temp_dict["id"].append(qa["id"])
                    temp_dict["title"].append(title)
                    temp_dict["context"].append(context)
                    temp_dict["question"].append(qa["question"])
                    temp_dict["label"].append(f'{qa["answers"][0]["text"]}',
                    )
                    temp_dict["text"].append(
                        replace_with_template(qa["question"], context,  qa["answers"][0]["text"])
                    )

        # convert temp_dict to Dataset and insert into DatasetDict
        combined[split] = datasets.Dataset.from_dict(temp_dict)
        
        # Convert the dataset to a pandas DataFrame
        df = combined[split].to_pandas()

        # Drop duplicates based on 'id' column
        df = df.drop_duplicates(subset="context").reset_index(drop=True)

        # Convert the DataFrame back to a dataset
        combined[split] = datasets.Dataset.from_pandas(df)

    return combined


def replace_with_template(question,context,answer):
    return PATTERNS['q&a'][1].format(question = question,context = context, answer = answer )