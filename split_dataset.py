import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

# Configure paths
base_dir = Path(r"../Unified_Chemistry_Lab_Dataset")
images_dir = base_dir / "images"
labels_dir = base_dir / "labels"

# Dataset split ratio
TRAIN_RATIO = 0.70  # 70% training set
VALID_RATIO = 0.20  # 20% validation set
TEST_RATIO = 0.10   # 10% test set

# Class names
class_names = {
    0: "Hand", 1: "Eggplant_Shaped_Flask", 2: "Beaker", 3: "Conical_Flask",
    4: "Reagent_Bottle", 5: "Pipette", 6: "Separating_Funnel", 7: "Buchner_Funnel",
    8: "Burette_Stands", 9: "Calorimeter", 10: "Funnel", 11: "Glass_Rod",
    12: "Measuring_Cylinder", 13: "Mechanical_Balance_Scale", 14: "Nessler_Reagent_Bottle",
    15: "Porcelain_Mortar_Pestle", 16: "Precision_Weight_Scale", 17: "Round_Bottom_Flask_1_Neck",
    18: "Round_Bottom_Flask_2_Neck", 19: "Round_Bottom_Flask_3_Neck", 20: "Spirit_Lamp",
    21: "TestTube_Holder", 22: "Test_Tube", 23: "Volumetric_Flask",
    24: "Volumetric_Pipet", 25: "Wash_Bottle", 26: "Weighing_Bottle"
}

print("=" * 80)
print("Chemical27 Dataset Splitting Tool")
print("=" * 80)
print(f"Split Ratio: Training {TRAIN_RATIO*100}%, Validation {VALID_RATIO*100}%, Test {TEST_RATIO*100}%")
print("=" * 80)

print("=" * 80)
print("Chemical27 Dataset Splitting Tool")
print("=" * 80)
print(f"Split Ratio: Training {TRAIN_RATIO*100}%, Validation {VALID_RATIO*100}%, Test {TEST_RATIO*100}%")
print("=" * 80)

def count_labels_in_file(label_file):
    """Count labels in a single label file"""
    label_counts = defaultdict(int)
    try:
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    class_id = int(parts[0])
                    label_counts[class_id] += 1
    except Exception as e:
        print(f"Error reading file {label_file}: {e}")
    return label_counts

def collect_dataset_files():
    """Collect all image and label files"""
    print("\nScanning image and label files...")
    
    # Get all image files
    all_images = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
    print(f"Found {len(all_images)} image files")
    
    # Filter images with corresponding labels
    matched_files = []
    for img_path in all_images:
        img_stem = img_path.stem  # Filename without extension
        label_path = labels_dir / f"{img_stem}.txt"
        
        if label_path.exists():
            matched_files.append(img_stem)
    
    print(f"Found {len(matched_files)} paired image-label files")
    
    return matched_files

def split_dataset(all_files):
    """Split file list into training, validation and test sets"""
    # Shuffle file order
    random.seed(42)  # Set random seed for reproducibility
    shuffled_files = all_files.copy()
    random.shuffle(shuffled_files)
    
    total = len(shuffled_files)
    train_count = int(total * TRAIN_RATIO)
    valid_count = int(total * VALID_RATIO)
    
    train_files = shuffled_files[:train_count]
    valid_files = shuffled_files[train_count:train_count + valid_count]
    test_files = shuffled_files[train_count + valid_count:]
    
    print(f"\nDataset split results:")
    print(f"  Training set: {len(train_files)} files")
    print(f"  Validation set: {len(valid_files)} files")
    print(f"  Test set: {len(test_files)} files")
    print(f"  Total: {total} files")
    
    return {
        'train': train_files,
        'valid': valid_files,
        'test': test_files
    }

def count_labels_in_split(file_list):
    """Count label quantities in a dataset split"""
    label_counts = defaultdict(int)
    
    for filename in file_list:
        label_path = labels_dir / f"{filename}.txt"
        if label_path.exists():
            counts = count_labels_in_file(label_path)
            for class_id, count in counts.items():
                label_counts[class_id] += count
    
    return label_counts

def print_statistics(splits):
    """Print statistics information"""
    print("\n" + "=" * 80)
    print("Dataset Statistics")
    print("=" * 80)
    
    overall_label_counts = defaultdict(int)
    
    for split_name in ['train', 'valid', 'test']:
        files = splits[split_name]
        label_counts = count_labels_in_split(files)
        
        print(f"\n{split_name.upper()} Dataset:")
        print(f"  Number of images: {len(files)}")
        
        total_labels = sum(label_counts.values())
        print(f"  Total labels: {total_labels}")
        print(f"\n  Label count by category:")
        
        for class_id in sorted(label_counts.keys()):
            count = label_counts[class_id]
            class_name = class_names.get(class_id, f"Unknown_{class_id}")
            print(f"    {class_id:2d} - {class_name:30s}: {count:5d}")
            overall_label_counts[class_id] += count
    
    # Print overall statistics
    print("\n" + "=" * 80)
    print("Overall Statistics:")
    print("=" * 80)
    total_images = sum(len(splits[s]) for s in ['train', 'valid', 'test'])
    total_labels = sum(overall_label_counts.values())
    print(f"Total number of images: {total_images}")
    print(f"Total number of labels: {total_labels}")
    print(f"\nTotal labels by category:")
    
    for class_id in sorted(overall_label_counts.keys()):
        count = overall_label_counts[class_id]
        class_name = class_names.get(class_id, f"Unknown_{class_id}")
        print(f"  {class_id:2d} - {class_name:30s}: {count:5d}")

def create_directory_structure(splits):
    """Create directory structure and copy files"""
    print("\n" + "=" * 80)
    print("Creating directory structure and copying files...")
    print("=" * 80)
    
    # Create directories
    for split_name in ['train', 'valid', 'test']:
        img_dir = base_dir / split_name / 'images'
        lbl_dir = base_dir / split_name / 'labels'
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {split_name}/images and {split_name}/labels")
    
    # Copy files
    for split_name, files in splits.items():
        print(f"\nCopying {split_name} dataset files...")
        dest_img_dir = base_dir / split_name / 'images'
        dest_lbl_dir = base_dir / split_name / 'labels'
        
        for i, filename in enumerate(files, 1):
            # Find image file (could be jpg or png)
            img_file = None
            for ext in ['.jpg', '.png']:
                potential_img = images_dir / f"{filename}{ext}"
                if potential_img.exists():
                    img_file = potential_img
                    break
            
            # Copy image
            if img_file:
                dest_img = dest_img_dir / img_file.name
                shutil.copy2(img_file, dest_img)
            
            # Copy label
            label_file = labels_dir / f"{filename}.txt"
            if label_file.exists():
                dest_lbl = dest_lbl_dir / label_file.name
                shutil.copy2(label_file, dest_lbl)
            
            if i % 500 == 0:
                print(f"  Copied {i}/{len(files)} files...")
        
        print(f"  Completed copying {split_name} dataset files ({len(files)} files)")
    
    print("\n✓ All files copied successfully!")
    print(f"\nDirectory structure:")
    print(f"  {base_dir / 'train' / 'images'}")
    print(f"  {base_dir / 'train' / 'labels'}")
    print(f"  {base_dir / 'valid' / 'images'}")
    print(f"  {base_dir / 'valid' / 'labels'}")
    print(f"  {base_dir / 'test' / 'images'}")
    print(f"  {base_dir / 'test' / 'labels'}")

def save_statistics_report(splits):
    """Save statistics report to file"""
    report_file = base_dir / "dataset_statistics.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("Chemical27 Dataset Statistics Report\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Split Ratio: Training {TRAIN_RATIO*100}%, Validation {VALID_RATIO*100}%, Test {TEST_RATIO*100}%\n\n")
        
        overall_label_counts = defaultdict(int)
        
        for split_name in ['train', 'valid', 'test']:
            files = splits[split_name]
            label_counts = count_labels_in_split(files)
            
            f.write(f"{split_name.upper()} Dataset:\n")
            f.write(f"  Number of images: {len(files)}\n")
            
            total_labels = sum(label_counts.values())
            f.write(f"  Total labels: {total_labels}\n\n")
            f.write(f"  Label count by category:\n")
            
            for class_id in sorted(label_counts.keys()):
                count = label_counts[class_id]
                class_name = class_names.get(class_id, f"Unknown_{class_id}")
                f.write(f"    {class_id:2d} - {class_name:30s}: {count:5d}\n")
                overall_label_counts[class_id] += count
            f.write("\n")
        
        # Overall statistics
        f.write("=" * 80 + "\n")
        f.write("Overall Statistics:\n")
        f.write("=" * 80 + "\n")
        total_images = sum(len(splits[s]) for s in ['train', 'valid', 'test'])
        total_labels = sum(overall_label_counts.values())
        f.write(f"Total number of images: {total_images}\n")
        f.write(f"Total number of labels: {total_labels}\n\n")
        f.write(f"Total labels by category:\n")
        
        for class_id in sorted(overall_label_counts.keys()):
            count = overall_label_counts[class_id]
            class_name = class_names.get(class_id, f"Unknown_{class_id}")
            f.write(f"  {class_id:2d} - {class_name:30s}: {count:5d}\n")
    
    print(f"\n✓ Statistics report saved to: {report_file}")

def main():
    # Collect all files
    all_files = collect_dataset_files()
    
    if len(all_files) == 0:
        print("Error: No paired image and label files found!")
        return
    
    # Split dataset
    splits = split_dataset(all_files)
    
    # Print statistics
    print_statistics(splits)
    
    # Ask whether to create directory structure
    print("\n" + "=" * 80)
    response = input("Create train/valid/test directory structure and copy files? (yes/no): ")
    
    if response.lower() in ['yes', 'y', 'YES', 'Y']:
        create_directory_structure(splits)
        save_statistics_report(splits)
        print("\n" + "=" * 80)
        print("✓ Dataset splitting completed!")
        print("=" * 80)
    else:
        print("\nDirectory creation operation cancelled.")
        save_statistics_report(splits)

if __name__ == "__main__":
    main()
