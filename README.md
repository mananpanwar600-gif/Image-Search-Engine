# YOLO-Powered Image Search

A computer vision project that uses YOLO (You Only Look Once) for object detection, classification, and searching for specific objects across multiple images.

## Overview

Manually searching through hundreds or thousands of images to find a particular object can be time-consuming. This project automates the process by detecting objects in images, storing their metadata, and retrieving relevant images based on the user's search query.

The system provides object class labels, confidence scores, and bounding-box coordinates to help users inspect and validate predictions.

## Features

- **Object Detection:** Detect multiple objects in images using a YOLO-based model.
- **Object Classification:** Identify the predicted class of each detected object.
- **Confidence Scores:** Display confidence scores for model predictions.
- **Bounding Boxes:** Visualize the locations of detected objects.
- **Image Search:** Search across an image collection using a selected object class.
- **Prediction Validation:** Inspect detection results and identify incorrect predictions.
- **Metadata Extraction:** Store image paths, class labels, confidence scores, and bounding-box coordinates.
- **JSON Export:** Export filtered detection results and metadata in JSON format.
- **Dataset Management:** Support data collection, annotation, review, and dataset versioning.

## Problem Statement

To develop a YOLO-powered image search system that detects and classifies objects across multiple images, enables users to search for specific objects, and retrieves matching images with their corresponding detection metadata. The system also supports prediction validation and JSON export for further analysis.

## Use Cases

- **Photographers:** Find images containing specific objects.
- **E-commerce:** Search product image collections using object categories.
- **Computer Vision Engineers:** Inspect and validate model predictions.
- **Data Annotators:** Review object labels and bounding boxes.
- **General Users:** Search large image collections without manually opening every image.

## System Workflow

1. **Input:** Upload an image or provide a collection of images.
2. **Preprocessing:** Validate images and prepare them for inference.
3. **Object Detection:** Run the YOLO model on the input images.
4. **Metadata Extraction:** Extract object classes, confidence scores, and bounding-box coordinates.
5. **Indexing:** Store detection metadata for efficient searching.
6. **Query:** Select or enter the object class to search for.
7. **Retrieval:** Find images containing the requested object.
8. **Output:** Display matching images and detection information.
9. **Export:** Save selected results as a JSON file.

## Dataset Annotation and Review

The dataset preparation workflow consists of:

1. **Data Collection:** Collect images relevant to the required object classes.
2. **Data Cleaning:** Remove corrupted, duplicate, or unsuitable images.
3. **Data Annotation:** Label objects and their bounding boxes.
4. **Annotation Review:** Check labels and bounding-box accuracy.
5. **Dataset Finalization:** Save the reviewed dataset as a versioned dataset.

If a pretrained model is used only for inference, custom annotation is not mandatory. Annotation is required when preparing labelled data for custom training or ground-truth evaluation.

## Technology Stack

- **Programming Language:** Python
- **Object Detection:** YOLO
- **Image Processing:** OpenCV, Pillow
- **Data Storage:** JSON
- **Development Environment:** Jupyter Notebook / Python
- **Interface:** Command-line interface or web interface, depending on implementation

## Project Structure

