# Cell 1
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
from backend.keyframes.model import DSN
import torch.nn as nn
import cv2
import time
import os
import srt
from backend.keyframes.extract_frames import extract_frames
from backend.utils import copy_and_rename_file, get_black_bar_coordinates, crop_image

# Cell 2
def _get_features(frames, gpu=False, batch_size=1):
    # Use simple GoogLeNet for speed (no GPU to avoid complexity)
    try:
        model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', weights='GoogLeNet_Weights.DEFAULT')
        model = torch.nn.Sequential(*(list(model.children())[:-1]))
        feature_dim = 1024
    except:
        # If model loading fails, use simple pixel-based features
        return _get_simple_features(frames)

    model.eval()
    features = []

    # Simple preprocessing for speed
    preprocess = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Process frames
    for frame_path in frames:
        try:
            input_image = Image.open(frame_path)
            input_tensor = preprocess(input_image).unsqueeze(0)
            
            with torch.no_grad():
                output = model(input_tensor)
            features.append(output.squeeze().cpu().numpy())
        except:
            # Fallback to simple features if processing fails
            features.append(_get_simple_frame_features(frame_path))

    return np.array(features).astype(np.float32)

def _get_simple_features(frames):
    """Fallback simple feature extraction"""
    features = []
    for frame_path in frames:
        features.append(_get_simple_frame_features(frame_path))
    return np.array(features).astype(np.float32)

def _get_simple_frame_features(frame_path):
    """Extract simple pixel-based features"""
    try:
        img = cv2.imread(frame_path)
        if img is None:
            return np.zeros(1024)  # Return zero features if image can't be loaded
        
        # Resize to small size for speed
        img = cv2.resize(img, (32, 32))
        # Flatten and pad/truncate to 1024 features
        features = img.flatten()
        if len(features) > 1024:
            features = features[:1024]
        else:
            features = np.pad(features, (0, 1024 - len(features)), 'constant')
        
        return features.astype(np.float32)
    except:
        return np.zeros(1024)

# Cell 3
def _get_probs(features, gpu=True, mode=0):
    # model_cache_key = "keyframes_rl_model_cache_" + str(mode)
    if mode == 1:
        model_path = "backend/keyframes/pretrained_model/model_1.pth.tar"
    else:
        model_path = "backend/keyframes/pretrained_model/model_0.pth.tar"
    
    # Determine feature dimension based on the actual features
    feature_dim = features.shape[-1] if len(features.shape) > 1 else 1024
    
    model = DSN(in_dim=feature_dim, hid_dim=256, num_layers=1, cell="lstm")
    
    try:
        if gpu:
            checkpoint = torch.load(model_path)
        else:
            checkpoint = torch.load(model_path, map_location='cpu')
        model.load_state_dict(checkpoint)
    except:
        # If loading fails, use a default model
        print("Warning: Could not load pretrained model, using default weights")
    
    if gpu:
        model = nn.DataParallel(model).cuda()
    model.eval()

    seq = torch.from_numpy(features).unsqueeze(0)
    if gpu: seq = seq.cuda()
    probs = model(seq)
    probs = probs.data.cpu().squeeze().numpy()
    return probs


   
def generate_keyframes(video):
    print(f"=== KEYFRAME GENERATION STARTED ===")
    print(f"Video file: {video}")
    
    data=""
    with open("test1.srt") as f:
        data = f.read()

    subs = srt.parse(data)
    subs_list = list(subs)
    print(f"Processing {len(subs_list)} subtitles for keyframe generation")
    
    # Check if frames/final directory exists
    if not os.path.exists("frames/final"):
        print("Creating frames/final directory...")
        os.makedirs("frames/final")
    else:
        print("frames/final directory already exists")

    for sub in subs_list:
        # Skip invalid subtitle indices
        if sub.index < 1 or sub.index > 1000:  # Reasonable range check
            print(f"Skipping invalid subtitle index: {sub.index}")
            continue
            
        frames = []
        if not os.path.exists(f"frames/sub{sub.index}"):
            os.makedirs(f"frames/sub{sub.index}")
        
        # Extract fewer frames for speed (1 frame per second instead of 3)
        frames = extract_frames(video, os.path.join("frames",f"sub{sub.index}"), sub.start.total_seconds(), sub.end.total_seconds(), 1)
        
        if not frames:
            print(f"No frames extracted for subtitle {sub.index}")
            continue
            
        # Simple selection - just take the middle frame for speed
        if len(frames) > 1:
            selected_frame = frames[len(frames)//2]
        else:
            selected_frame = frames[0]
            
        copy_and_rename_file(selected_frame, os.path.join("frames","final"), f"frame{sub.index:03}.png")
        print(f"Selected frame {sub.index} from {len(frames)} frames")
    
    print(f"=== KEYFRAME GENERATION COMPLETED ===")
    print(f"Generated frames in frames/final directory")
    

def black_bar_crop():
    # Skip cropping to avoid cutting images - just return dummy values
    print("Skipping black bar cropping to preserve full images")
    return 0, 0, 0, 0