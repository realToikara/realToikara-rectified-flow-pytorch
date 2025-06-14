import torch

# hf datasets for easy oxford flowers training

import torchvision.transforms as T
from torch.utils.data import Dataset
from datasets import load_dataset

class OxfordFlowersDataset(Dataset):
    def __init__(
        self,
        image_size
    ):
        self.ds = load_dataset('nelorth/oxford-flowers')['train']

        self.transform = T.Compose([
            T.Resize((image_size, image_size)),
            T.PILToTensor()
        ])

    def __len__(self):
        return len(self.ds)

    def __getitem__(self, idx):
        pil = self.ds[idx]['image']
        tensor = self.transform(pil)
        return tensor / 255.

flowers_dataset = OxfordFlowersDataset(
    image_size = 64
)

# models and trainer

from rectified_flow_pytorch import MeanFlow, Unet, Trainer

model = Unet(
    dim = 64,
    dim_cond = 1,
    accept_cond = True
)

mean_flow = MeanFlow(
    model,
    normalize_data_fn = lambda t: t * 2. - 1.,
    unnormalize_data_fn = lambda t: (t + 1.) / 2.
)

trainer = Trainer(
    mean_flow,
    dataset = flowers_dataset,
    num_train_steps = 70_000,
    learning_rate = 1e-4,
    results_folder = './results'   # samples will be saved periodically to this folder
)

trainer()
