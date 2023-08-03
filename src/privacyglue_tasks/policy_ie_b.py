#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import cast

import datasets

from dataset.templates import PATTERNS

from ..utils.task_utils import expand_dataset_per_task, policy_ie_file_mapping

SUBTASKS = ["type-I", "type-II"]
LABELS = [
    [
        "data-protector",
        "data-protected",
        "data-collector",
        "data-collected",
        "data-receiver",
        "data-retained",
        "data-holder",
        "data-provider",
        "data-sharer",
        "data-shared",
        "storage-place",
        "retention-period",
        "protect-against",
        "action",
    ],
    [
        "purpose-argument",
        "polarity",
        "method",
        "condition-argument",
    ],
]


def load_policy_ie_b(directory: str) -> datasets.DatasetDict:
    # initialize DatasetDict object
    combined = datasets.DatasetDict()

    data_files = policy_ie_file_mapping(directory, "seq.in")
    
    # load tokens which are common for all sub-tasks
    tokens = datasets.load_dataset(
        "text", data_files=policy_ie_file_mapping(directory, "seq.in")
    ).map(lambda example: {"tokens": example["text"].split()}, remove_columns=["text"])

    # since this is task B, load all NER tags
    ner_tags_first = datasets.load_dataset(
        "text", data_files=policy_ie_file_mapping(directory, "seq_type_I.out")
    ).map(
        lambda example: {"ner_tags_type_one": example["text"].split()},
        remove_columns=["text"],
    )
    ner_tags_second = datasets.load_dataset(
        "text", data_files=policy_ie_file_mapping(directory, "seq_type_II.out")
    ).map(
        lambda example: {"ner_tags_type_two": example["text"].split()},
        remove_columns=["text"],
    )

    # mypy-related fixes
    tokens = cast(datasets.DatasetDict, tokens)
    ner_tags_first = cast(datasets.DatasetDict, ner_tags_first)
    ner_tags_second = cast(datasets.DatasetDict, ner_tags_second)

    # zip together data in splits
    for split in ["train", "validation", "test"]:
        combined[split] = datasets.concatenate_datasets(
            [tokens[split], ner_tags_first[split], ner_tags_second[split]], axis=1
        )

    # merge NER tags and drop old ones
    combined = combined.map(
        lambda x: {"tags": list(zip(x["ner_tags_type_one"], x["ner_tags_type_two"]))},
        remove_columns=["ner_tags_type_one", "ner_tags_type_two"],
    )

    # reassign splits to combined and multiply tags to rows
    combined["train"] = expand_dataset_per_task(combined["train"], SUBTASKS)
    combined["validation"] = expand_dataset_per_task(combined["test"], SUBTASKS)

    combined["test"] = expand_dataset_per_task(combined["test"], SUBTASKS)

    # get all the unique tags and add to feature information
    label_names = {
        task: ["O"] + [f"{pre}-{label}" for pre in ["B", "I"] for label in tags]
        for task, tags in zip(SUBTASKS, LABELS)
    }

    for split in ["train", "validation", "test"]:
        for st in SUBTASKS:
            combined[split][st].features["tags"] = datasets.Sequence(
                feature=datasets.ClassLabel(names=label_names[st])
            )
    
    transform_to_text_to_text(combined)
        
    return combined


def transform_to_text_to_text(combined):
    for split in ["train", "validation", "test"]:
        # Convert the dataset to a pandas DataFrame
        df = combined[split]
        
        for st in SUBTASKS:
            df = combined[split][st].to_pandas()
            # df['tags'] = df.apply(lambda row: clean_tags(row['tags']), axis=1)
            df['label'] = df.apply(lambda row: extract_entities(row['tags'], row["tokens"]), axis=1)
            df['text'] = df.apply(lambda row: extract_text(row["tokens"]), axis=1)
            df['text'] = df.apply(lambda row: replace_with_template(row["text"], st), axis=1)
            # Convert the DataFrame back to a dataset
            combined[split][st] = datasets.Dataset.from_pandas(df)
        
def extract_text(words):
    # Join the list elements with space
    result_string = " ".join(words)
    return result_string
    
def clean_tags(tags):
    # Join the list elements with space
    new_tags = []
    for tag in tags:
        if len(tag) > 2:
            new_tags.append(tag.split(".")[0].upper())
    return new_tags
    
def replace_with_template(text, subtask_type):
    # Join the list elements with space
    if subtask_type == "type-I":
        return PATTERNS['policy_ie_b'][0].format(text=text)
    else:
        return PATTERNS['policy_ie_b'][1].format(text=text)

def extract_entities(tags, words):
    entities_string = ""
    for tag, word in zip(tags, words):
        if tag == 'O':
            continue
        # Store the entity in the dictionary
        if len(entities_string) > 0:
            if tag[0] == 'B':
                entities_string = entities_string + "; " \
                    + tag[2:].split(".")[0].upper() + ": " + word
            else:
                entities_string = entities_string + " " + word   
        else:
            entities_string = tag[2:].split(".")[0].upper()  + ": " + word
    return entities_string
