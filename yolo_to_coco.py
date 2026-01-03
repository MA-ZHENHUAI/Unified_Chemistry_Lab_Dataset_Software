"""
YOLO to COCO Format Conversion Script
Converts YOLO format annotation files to COCO JSON format for Faster R-CNN training

"""

import json
import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import yaml


def load_config(config_path):
    """Load configuration file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def convert_yolo_to_coco(images_dir, labels_dir, class_names, output_json):
    """
    Convert YOLO format to COCO format
    
    Args:
        images_dir: Image directory path
        labels_dir: YOLO annotation file directory path
        class_names: List of class names
        output_json: Output COCO JSON file path
    """
    images_path = Path(images_dir)
    labels_path = Path(labels_dir)
    
    # COCO format data structure
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    # Add category information
    for idx, class_name in enumerate(class_names):
        coco_format["categories"].append({
            "id": idx,
            "name": class_name,
            "supercategory": "chemical_equipment"
        })
    
    # Get all image files
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = [f for f in images_path.iterdir() 
                   if f.suffix.lower() in valid_extensions]
    
    annotation_id = 0
    missing_labels = 0
    
    print(f"Processing {len(image_files)} images...")
    
    for image_id, img_file in enumerate(tqdm(image_files)):
        # Read image to get dimensions
        try:
            with Image.open(img_file) as img:
                width, height = img.size
        except Exception as e:
            print(f"Warning: Cannot read image {img_file}: {e}")
            continue
        
        # Add image information
        coco_format["images"].append({
            "id": image_id,
            "file_name": img_file.name,
            "width": width,
            "height": height
        })
        
        # Read corresponding YOLO annotation file
        label_file = labels_path / f"{img_file.stem}.txt"
        
        if not label_file.exists():
            missing_labels += 1
            continue
        
        # Parse YOLO annotation
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) != 5:
                print(f"Warning: Incorrect annotation format {label_file}: {line}")
                continue
            
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            bbox_width = float(parts[3])
            bbox_height = float(parts[4])
            
            # Convert YOLO format to COCO format
            # YOLO: (x_center, y_center, width, height) normalized coordinates
            # COCO: (x_min, y_min, width, height) absolute coordinates
            x_min = (x_center - bbox_width / 2) * width
            y_min = (y_center - bbox_height / 2) * height
            bbox_width_abs = bbox_width * width
            bbox_height_abs = bbox_height * height
            
            # Ensure coordinates are within valid range
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            bbox_width_abs = min(bbox_width_abs, width - x_min)
            bbox_height_abs = min(bbox_height_abs, height - y_min)
            
            # Calculate area
            area = bbox_width_abs * bbox_height_abs
            
            # Add annotation information
            coco_format["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": class_id,
                "bbox": [x_min, y_min, bbox_width_abs, bbox_height_abs],
                "area": area,
                "iscrowd": 0
            })
            
            annotation_id += 1
    
    # Save COCO JSON file
    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(coco_format, f, indent=2)
    
    print(f"\nConversion completed!")
    print(f"Number of images: {len(coco_format['images'])}")
    print(f"Number of annotations: {len(coco_format['annotations'])}")
    print(f"Number of categories: {len(coco_format['categories'])}")
    if missing_labels > 0:
        print(f"Warning: {missing_labels} images are missing annotation files")
    print(f"Output file: {output_path.absolute()}")
    
    return coco_format


def main():
    # ==================== Configuration Parameters ====================
    # Modify configuration file paths here directly, no need for command line arguments
    CONFIG_FILE = '../config_fasterrcnn.yaml'  # Faster R-CNN configuration file path
    DATASET_YAML = '../UCLD.yaml'  # YOLO dataset configuration file path
    # ================================================================
    
    # Load configuration
    config = load_config(CONFIG_FILE)
    dataset_root = config['dataset']['root']
    
    # Load YOLO dataset configuration to get class names
    with open(DATASET_YAML, 'r', encoding='utf-8') as f:
        yolo_config = yaml.safe_load(f)
    
    class_names = [yolo_config['names'][i] for i in range(len(yolo_config['names']))]
    
    print("=" * 60)
    print("YOLO to COCO Format Conversion Tool")
    print("=" * 60)
    print(f"Dataset root directory: {dataset_root}")
    print(f"Number of categories: {len(class_names)}")
    print(f"Category list: {', '.join(class_names[:5])}..." if len(class_names) > 5 else f"Category list: {', '.join(class_names)}")
    print("=" * 60)
    
    # Convert training set
    print("\n[1/3] Converting training set...")
    train_images = os.path.join(dataset_root, 'train', 'images')
    train_labels = os.path.join(dataset_root, 'train', 'labels')
    train_json = os.path.join(dataset_root, 'annotations', 'train_coco.json')
    convert_yolo_to_coco(train_images, train_labels, class_names, train_json)
    
    # Convert validation set
    print("\n[2/3] Converting validation set...")
    val_images = os.path.join(dataset_root, 'valid', 'images')
    val_labels = os.path.join(dataset_root, 'valid', 'labels')
    val_json = os.path.join(dataset_root, 'annotations', 'val_coco.json')
    convert_yolo_to_coco(val_images, val_labels, class_names, val_json)
    
    # Convert test set
    print("\n[3/3] Converting test set...")
    test_images = os.path.join(dataset_root, 'test', 'images')
    test_labels = os.path.join(dataset_root, 'test', 'labels')
    test_json = os.path.join(dataset_root, 'annotations', 'test_coco.json')
    convert_yolo_to_coco(test_images, test_labels, class_names, test_json)
    
    print("\n" + "=" * 60)
    print("All conversions completed! ✓")
    print("=" * 60)
    print(f"\nGenerated files:")
    print(f"  - {train_json}")
    print(f"  - {val_json}")
    print(f"  - {test_json}")


if __name__ == '__main__':
    main()


