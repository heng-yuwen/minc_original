import torch
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader, RandomSampler
from torchvision import transforms

from minctools.datasets.minc import MINC
from pytorchtools.sampler import PySubsetRandomSampler


class MINCDataModule(LightningDataModule):
    def __init__(self, data_root, json_data):
        super().__init__()

        self._use_gpu = torch.cuda.is_available()
        self._data_root = data_root
        self._json_data = json_data
        self._dataset = self._json_data["dataset"]
        self._classes = self._json_data["classes"]
        self._batch_size = self._json_data["train_params"]["batch_size"]

    def train_dataloader(self):
        train_trans = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor()
        ])
        train_set = MINC(root_dir=self._data_root, set_type='train',
                         classes=self._classes, transform=train_trans)
        print("Training set loaded, with {} samples".format(len(train_set)))
        return DataLoader(dataset=train_set,
                          batch_size=10,
                          pin_memory=self._use_gpu,
                          sampler=PySubsetRandomSampler(train_set, 23))

    def val_dataloader(self):
        val_trans = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor()
        ])
        val_set = MINC(root_dir=self._data_root, set_type='validate',
                       classes=self._classes, transform=val_trans)
        print("Validation set loaded, with {} samples".format(len(val_set)))
        return DataLoader(dataset=val_set, batch_size=10,
                          shuffle=False, pin_memory=self._use_gpu, sampler=RandomSampler(val_set, replacement=True, num_samples=23))

    def test_dataloader(self):
        test_trans = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor()
        ])

        test_set = MINC(root_dir=self._data_root, set_type='test',
                        classes=self._classes, transform=test_trans)
        print("Test set loaded, with {} samples".format(len(test_set)))

        return DataLoader(dataset=test_set, batch_size=10,
                          shuffle=False, pin_memory=self._use_gpu, sampler=RandomSampler(test_set, replacement=True, num_samples=23))
