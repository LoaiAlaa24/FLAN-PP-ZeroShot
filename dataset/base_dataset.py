"""Dataset Base Class"""

from torch.utils.data import Dataset


class BaseDataset(Dataset):
    """
    Abstract Dataset Base Class
    All subclasses must define __getitem__() and __len__()
    """
    def __init__(self, root):
        self.root_path = root
