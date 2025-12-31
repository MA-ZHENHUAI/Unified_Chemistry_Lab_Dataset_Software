Abstract

This dataset, named UCLD (Unified Chemical Laboratory Dataset), is designed to advance computer vision research in the field of autonomous robotic chemists and laboratory automation. It addresses critical challenges in unstructured laboratory environments, including the detection of transparent glassware, fine-grained equipment classification (e.g., distinguishing between 1-neck, 2-neck, and 3-neck flasks), and robustness against severe occlusion during human-object interactions.

The dataset contains 9,677 high-quality images covering 27 categories of common chemistry lab equipment. It is constructed from two complementary sources:

Source D1 (Static): High-fidelity images focusing on geometric details for affordance learning. 
( https://doi.org/10.1038/s41597-025-05952-3)

Source D2 (Dynamic): Frames captured from experiment videos featuring complex backgrounds, liquid manipulation, and hand occlusions.
(https://doi.org/10.17632/8p2hvgdvpn.1)

Key Features 

Fine-Grained Categories: distinguish topological differences among glassware (e.g., Round_Bottom_Flask_1_Neck vs. 2_Neck vs. 3_Neck).

Human-Interaction Aware: Includes a specific class for "Hand" to facilitate human-in-the-loop perception and occlusion handling.

Challenging Conditions: Contains transparent objects, reflective surfaces, and dense clutter typical of real-world chemistry labs.

Scale: 9,677 images with approx. 21257 annotated instances.

Format: Annotated in standard YOLO (TXT) format and COCO (JSON) format.

Categories 

The dataset includes 27 classes:

 0: 'Hand', 1: 'Eggplant_Shaped_Flask', 2: 'Beaker', 3: 'Conical_Flask', 4: 'Reagent_Bottle', 5: 'Pipette', 6: 'Separating_Funnel', 7: 'Buchner_Funnel', 8: 'Burette_Stands', 9: 'Calorimeter', 10: 'Funnel', 11: 'Glass_Rod', 12: 'Measuring_Cylinder', 13: 'Mechanical_Balance_Scale', 14: 'Nessler_Reagent_Bottle', 15: 'Porcelain_Mortar_Pestle', 16: 'Precision_Weight_Scale', 17: 'Round_Bottom_Flask_1_Neck', 18: 'Round_Bottom_Flask_2_Neck', 19: 'Round_Bottom_Flask_3_Neck', 20: 'Spirit_Lamp', 21: 'TestTube_Holder', 22: 'Test_Tube', 23: 'Volumetric_Flask', 24: 'Volumetric_Pipet', 25: 'Wash_Bottle', 26: 'Weighing_Bottle'

Dataset Structure 

The dataset is organized as follows:



UCLD_Dataset/
├── Coco_format_labels/  
│   ├── train_coco.json
│   ├── val_coco.json
│   └── test_coco.json
├── train/     
│   ├── images/  (6,774 images)
│   └── labels/     (YOLO format .txt files)
├── valid/     
│   ├── imagesl/    (1,935 images)
│   └── test/           (YOLO format .txt files)
├── test/     
│   ├── images/   (968 images)
│   └── labels/      (YOLO format .txt files)
├── Output_Data/
├── Dataset Structure .txt
├── Readme.txt
├── UCLD.yaml   (Configuration file for YOLO training)
└── dataset_statistics.txt (Unified Chemistry Lab Dataset Statistics Report)




Data Collection & Annotation 

Data Sources: Collected from real-world chemistry laboratories using DSLR cameras and HD video streams.

Annotation: Manually annotated using LabelImg with strict quality control to ensure tight bounding boxes around transparent boundaries.

Splitting: Randomly split into Train (70%), Validation (20%), and Test (10%).

Usage 

This dataset is suitable for training and evaluating object detection models (e.g., YOLO, Faster R-CNN, DETR) for:

Laboratory Automation: Robot grasping and manipulation planning.

Safety Monitoring: Detecting hazardous operations or missing equipment.

Fine-Grained Visual Recognition: Benchmarking models on similar-looking objects.

Citation 

If you use this dataset in your research, please cite our paper:

[Zhenhuai Ma], "Research on Laboratory Object Detection and Fine-Grained Classification for Robot Autonomous Experiments," [Journal Name], [Year].

License 

CC BY 4.0 (Creative Commons Attribution 4.0 International)