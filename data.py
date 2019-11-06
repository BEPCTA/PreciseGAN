import logging
import math
import pickle
import random
from pathlib import Path

import numpy as np
from torch.utils.data.dataset import Dataset


class DiJetDataset(Dataset):
    def __init__(self, items):
        self.items = items

    def __getitem__(self, item):
        return self.items[item]

    def __len__(self):
        return len(self.items)

    @classmethod
    def from_path(cls, path, scaler=None):
        items = np.load(path)

        if scaler is not None:
            items = scaler.transform(items)

        return cls(items)


def get_data(args):
    if args.training_filename is None:
        args.training_filename = "csv/%s.%s.%s.%s.csv" % (args.dsid, args.level, args.preselection, args.systematic)
        logging.info(f'training file: {args.training_filename}')
    else:
        args.systematic = args.training_filename.split("/")[-1].split('.')[-2]

    scaler_filename = "scaler.%s.pkl" % args.level
    logging.info(f'loading scaler from {scaler_filename}')
    with open(scaler_filename, "rb") as file_scaler:
        scaler = pickle.load(file_scaler)

    source_path = Path(args.training_filename)
    parent_path = source_path.parent
    file_name = source_path.stem

    train_file = parent_path / f'train_{file_name}.npy'
    test_file = parent_path / f'test_{file_name}.npy'

    dataset_train = DiJetDataset.from_path(train_file, scaler)
    dataset_test = DiJetDataset.from_path(test_file)

    return dataset_train, dataset_test, scaler


PTCL_HEADER = [
  "eventNumber", "weight",
  "ljet1_pt", "ljet1_eta", "ljet1_phi", "ljet1_E", "ljet1_M",
  "ljet2_pt", "ljet2_eta", "ljet2_phi", "ljet2_E", "ljet2_M",
  "jj_pt",    "jj_eta",    "jj_phi",    "jj_E",    "jj_M",
  "jj_dPhi",  "jj_dEta",  "jj_dR",
]
PTCL_FEATURES = [
    "ljet1_pt", "ljet1_eta", "ljet1_M",
    "ljet2_pt", "ljet2_eta", "ljet2_phi", "ljet2_M"
]