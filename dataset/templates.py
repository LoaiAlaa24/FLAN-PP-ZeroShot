"""Templates for FLAN."""

# pylint: disable=line-too-long

PATTERNS = {
    'q&a': [
        ('Answer this question: \n\n{question}'),
        ('Answer this question: \n\n{question} \n\ncontext: {context} \n\nanswer:'),
        ('Answer this question: \n\n{question} \n\ncontext: {context} \n\nanswer:{answer}')
    ],
    'opp115':[
        ('Text:\n{text}\nSelect the list topics that this text is about?\nOPTIONS:\n-Data Retention \n-Data Security \n-Do Not Track \n-First Party Collection/Use \n-International and Specific Audiences \n-Introductory/Generic \n-Policy Change \n-Practice not covered \n-Privacy contact information \n-Third Party Sharing/Collection \n-User Access, Edit and Deletion \n-User Choice/Control'),
                ('Classify the following text into a list of relevant categories.\n\n Text:\n{text} \n\nOPTIONS:\n-Data Retention \n-Data Security \n-Do Not Track \n-First Party Collection/Use \n-International and Specific Audiences \n-Introductory/Generic \n-Policy Change \n-Practice not covered \n-Privacy contact information \n-Third Party Sharing/Collection \n-User Access, Edit and Deletion \n-User Choice/Control'),
                ('Here are some text and categories. .\n\n Text:\n{text} \n\nOPTIONS:\n-Data Retention \n-Data Security \n-Do Not Track \n-First Party Collection/Use \n-International and Specific Audiences \n-Introductory/Generic \n-Policy Change \n-Practice not covered \n-Privacy contact information \n-Third Party Sharing/Collection \n-User Access, Edit and Deletion \n-User Choice/Control'),
    ],
    'policy_detection':[
        ('Text:\n{text}\nIs this text policy?\nOPTIONS:\n-Policy\n-Not Policy'),
        ('Classify this text into the relevant category:\n\ntext: {text}\n\nOPTIONS:\n-Policy \n-Not Policy')
    ],
    'policy_ie_a':[
        ('Text:\n{text}\nWhich topic is this text about?\nOPTIONS:\n-Other\n-Data Collection Usage\n-Data Security Protection\n-Data Sharing Disclosure\n-Data Storage Retention Deletion')
    ],
    'policy_ie_b':[
        ('Specify the following text into the relevant data entities \n\n Text:\n{text} \n\nOPTIONS:\n -DATA-PROTECTOR \n -DATA-PROTECTED \n -DATA-COLLECTOR \n -DATA-COLLECTED \n -DATA-RECEIVER \n -DATA-RETAINED \n -DATA-HOLDER \n -DATA-PROVIDER \n -DATA-SHARER \n -DATA-SHARED \n -STORAGE-PLACE \n -RETENTION-PERIOD \n -PROTECT-AGAINST \n -ACTION'),
        ('Specify the following text into the relevant data entities \n\n Text:\n{text} \n\nOPTIONS:\n -PURPOSE-ARGUMENT \n -POLARITY \n -METHOD \n -CONDITION-ARGUMENT')
    ],
    'privacy_qa':[
        ('Classify the relevance of the answer to the question:\n\nquestion: {question}\n\n answer: {answer} \n\nIs this answer relevant?\n\nOPTIONS:\n-Relevant \n-Irrelevant')
    ],
    'piextract':[
        ('Given the following text, identify the relevant information to be collected and mark it with the appropriate tags:\n\n Text: {text}'),
        ('Given the following text, identify the relevant information to be not collected and mark it with the appropriate tags:\n\n Text: {text}'),
        ('Given the following text, identify the relevant information to be shared and mark it with the appropriate tags:\n\n Text: {text}'),
        ('Given the following text, identify the relevant information to be not shared and mark it with the appropriate tags:\n\n Text: {text}')
    ],
    
}