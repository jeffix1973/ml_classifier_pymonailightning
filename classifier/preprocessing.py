import numpy as np
import pydicom
import torch
from torchvision.transforms import Compose, Resize
from monai.transforms import (
    ScaleIntensity,
    RandFlip, RandRotate, RandZoom, RandAdjustContrast, RandGaussianNoise, NormalizeIntensity
)


def preprocess_pipeline(dcm_path, resize_shape, mode):
    
    # Load the image using load_dicom
    img, uids = load_dicom(dcm_path)
    # add channel dimension
    if img.ndim == 2:
        img = np.expand_dims(img, axis=-1)
    # Convert to PyTorch tensor
    img_tensor = torch.from_numpy(img).permute(2, 0, 1)  # Convert to [C, H, W] format

    # Make a copy of the original image tensor for augmentation
    augmented_img = img_tensor.clone()

    # Scale intensity
    scale_intensity = ScaleIntensity()
    img_tensor = scale_intensity(img_tensor)

    # Apply MONAI augmentations only on train images
    if mode == 'train':
        augmented_img = apply_augmentation(augmented_img)

    # Resize images
    resize_transform = Resize(resize_shape, antialias=True)
    img_tensor = resize_transform(img_tensor)
    augmented_img = resize_transform(augmented_img)
    # Normalize intensity
    normalize_intensity = NormalizeIntensity()
    augmented_img = normalize_intensity(augmented_img)
    
    return img_tensor, augmented_img, uids


def load_dicom(dcm_path):
    # Load DICOM image
    dcm_data = pydicom.dcmread(dcm_path)
    img = dcm_data.pixel_array.astype(np.float32)
    uids = {}
    uids['StudyInstanceUID'] = dcm_data.StudyInstanceUID
    uids['SeriesInstanceUID'] = dcm_data.SeriesInstanceUID
    uids['SOPInstanceUID'] = dcm_data.SOPInstanceUID
    
    return img, uids


def apply_augmentation(image_tensor):

    # Define augmentations
    augmentations = Compose([
        # RandFlip(prob=0.3, spatial_axis=0),  # Flip along height axes
        # RandFlip(prob=0.3, spatial_axis=1),  # Flip along width axes
        RandRotate(range_x=np.pi/12, prob=0.3),
        RandZoom(min_zoom=0.9, max_zoom=1.1, prob=0.3),
        RandAdjustContrast(gamma=(0.9, 1.1), prob=0.3),
        RandGaussianNoise(prob=0.3),
    ])

    augmented_img = augmentations(image_tensor)
    
    return augmented_img




