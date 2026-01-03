import os
from pathlib import Path

# Configure paths
base_dir = Path(r"../Unified_Chemistry_Lab_Dataset")

print("=" * 80)
print("Dataset File Reorganization Tool")
print("=" * 80)
print("Will reorganize file numbering to make it sequential")
print("=" * 80)

def reorganize_split(split_name):
    """Reorganize files in a dataset split to have sequential numbering"""
    images_dir = base_dir / split_name / 'images'
    labels_dir = base_dir / split_name / 'labels'
    
    if not images_dir.exists():
        print(f"Warning: {images_dir} does not exist, skipping...")
        return
    
    # Get all image files and sort
    all_images = sorted(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")))
    
    print(f"\nReorganizing {split_name.upper()} dataset...")
    print(f"Found {len(all_images)} image files")
    
    if len(all_images) == 0:
        return
    
    # Step 1: Rename to temporary file names
    print(f"  Step 1: Renaming to temporary file names...")
    temp_mappings = []
    
    for idx, img_path in enumerate(all_images):
        old_stem = img_path.stem
        img_ext = img_path.suffix
        
        # Temporary file name
        temp_img_name = f"__reorg_{idx:06d}{img_ext}"
        temp_label_name = f"__reorg_{idx:06d}.txt"
        
        # Rename image
        temp_img_path = images_dir / temp_img_name
        img_path.rename(temp_img_path)
        
        # Rename label
        old_label_path = labels_dir / f"{old_stem}.txt"
        temp_label_path = None
        if old_label_path.exists():
            temp_label_path = labels_dir / temp_label_name
            old_label_path.rename(temp_label_path)
        
        temp_mappings.append((temp_img_path, temp_label_path, img_ext))
        
        if (idx + 1) % 1000 == 0:
            print(f"    Processed {idx + 1}/{len(all_images)} files...")
    
    # Step 2: Rename to final sequential numbering
    print(f"  Step 2: Renaming to final numbering...")
    
    for idx, (temp_img_path, temp_label_path, img_ext) in enumerate(temp_mappings):
        new_name = f"{split_name}_{idx:04d}"
        new_img_name = f"{new_name}{img_ext}"
        new_label_name = f"{new_name}.txt"
        
        # Rename image
        new_img_path = images_dir / new_img_name
        temp_img_path.rename(new_img_path)
        
        # Rename label
        if temp_label_path and temp_label_path.exists():
            new_label_path = labels_dir / new_label_name
            temp_label_path.rename(new_label_path)
        
        if (idx + 1) % 1000 == 0:
            print(f"    Renamed {idx + 1}/{len(temp_mappings)} files...")
    
    print(f"✓ Completed {split_name} dataset reorganization")
    print(f"  New file range: {split_name}_0000 to {split_name}_{len(temp_mappings)-1:04d}")

def main():
    print("\nStarting file reorganization...")
    
    for split in ['train', 'valid', 'test']:
        reorganize_split(split)
    
    print("\n" + "=" * 80)
    print("✓ All files reorganization completed!")
    print("=" * 80)
    
    # Display file count for each dataset
    print("\nDataset file statistics:")
    for split in ['train', 'valid', 'test']:
        images_dir = base_dir / split / 'images'
        if images_dir.exists():
            count = len(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")))
            print(f"  {split.upper()}: {count} files ({split}_0000 to {split}_{count-1:04d})")

if __name__ == "__main__":
    print("\n⚠️  Warning: This operation will reorganize all file numbering!")
    print("   All files will be renamed to sequential numbers")
    
    response = input("\nContinue? (yes/no): ")
    
    if response.lower() in ['yes', 'y', 'YES', 'Y']:
        main()
    else:
        print("\nOperation cancelled.")
