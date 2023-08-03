"""Dataset for facial keypoint detection"""

import os
import re

from datasets import Dataset, concatenate_datasets

from src.privacyglue_tasks.policy_qa import load_policy_qa
from src.privacyglue_tasks.privacy_qa import load_privacy_qa
from src.privacyglue_tasks.policy_ie_a import load_policy_ie_a
from src.privacyglue_tasks.policy_ie_b import load_policy_ie_b
from src.privacyglue_tasks.opp_115 import load_opp_115
from src.privacyglue_tasks.piextract import load_piextract
from src.privacyglue_tasks.policy_detection import load_policy_detection

from .base_dataset import BaseDataset

FILE_PATH = 'dataset/OPP-115/sanitized_policies/'


class DatasetLoader(BaseDataset):
    """Dataset for OPP-115 tasks"""
    def __init__(self):
        self.policy_qa_dataset = load_policy_qa('./dataset/privacyglue/policy_qa/')
        self.privacy_qa_dataset = load_privacy_qa('./dataset/privacyglue/privacy_qa/')
        self.policy_ie_a_dataset = load_policy_ie_a('./dataset/privacyglue/policy_ie_a/')
        self.policy_ie_b_dataset = load_policy_ie_b('./dataset/privacyglue/policy_ie_b/')
        self.opp_115_dataset = load_opp_115('./dataset/privacyglue/opp_115/')
        self.piextract_dataset = load_piextract('./dataset/privacyglue/piextract/')
        self.policy_detection_dataset = load_policy_detection('./dataset/privacyglue/policy_detection/')

        
    def load_clean_html_files(self):
        html_dict = {}
        for filename in os.listdir(FILE_PATH):
            # Extract the desired part using regex
            pattern = r"\d+_(.+)\.html"
            match = re.match(pattern, filename)
            if match:
                clean_name = match.group(1)
            if filename.endswith(".html"):
                file_path = os.path.join(FILE_PATH, filename)
                with open(file_path, 'r') as file:
                    html_content = file.read()
                    clean_text = self.remove_html_tags(html_content)
                    html_dict[clean_name] = clean_text.strip().replace("\n","")
        return html_dict
        
    def remove_html_tags(self, raw_html) -> str:
        """
        params: raw_html
        returns a cleaned privacy policy text
        """
        cleaner_html = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleaner_pipe = re.compile(r"\s{2,}|(\|{3})")
        cleaned_text = re.sub(cleaner_html, ' ', raw_html)
        cleaned_text = re.sub(cleaner_pipe, ' ', cleaned_text)
        return cleaned_text
    