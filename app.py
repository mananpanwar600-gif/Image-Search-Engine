import streamlit as st
import sys
from src.inference import YOLOv11Inference
from src.utils import save_metadata,load_metadata,get_unique_classes_counts
from pathlib import Path
## Add project root to system path


sys.path.append(str(Path(__file__).parent))

def init_session_state():
    session_defaults = {
        'metadata' : None,
        'unique_classes' : [],
        'count_options' : {},
        "search_results" : [],
        "search_params" : {
            'search_mode' : "Any of selected classes (OR)",
            'select_classes':[],
            "thresholds" : {}
        }
    }

    for key,value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()     

st.set_page_config(page_title="Yolov11 Search App",layout="wide")
st.title("Computer Vision Powered Search Application")

option = st.radio("Choose a option:",
                  ("Process new images","Load existing metadata"),horizontal=True)

if option == "Process new images":
    with st.expander("Process new images",expanded=True):
        col1,col2 = st.columns(2)
        with col1:
            image_dir = st.text_input("Image directory path:",placeholder="path/to/images")

        with col2:
            model_path = st.text_input("Model weights path:","yolo11m.pt")

        if st.button("Start Inference"):
            if image_dir:
                try:
                    with st.spinner("Running object detection"):
                       inferencer = YOLOv11Inference(model_path)
                       metadata = inferencer.process_directory(image_dir)
                       metadata_path=save_metadata(metadata,image_dir)
                       st.success(f"Processed {len(metadata)} images. Metadata saved to:")
                       st.code(str(metadata_path))
                
                       st.session_state.metadata = metadata
                       st.session_state.unique_classes,st.session_state.count_options = get_unique_classes_counts(metadata)

                except Exception as e:
                    st.error(f"Error during inference: {str(e)}")
            else:
                st.warning(f"Please enter a image directory path")
else:
    with st.expander("Load existing metadata",expanded=True):
       metadata_path = st.text_input("Metadata file path:",placeholder="path/to/metadata.json")
       if st.button("Load Metadata"):
            if metadata_path:
                try:
                    with st.spinner("Loading metadata..."):
                        metadata = load_metadata(metadata_path)
                        st.session_state.metadata = metadata
                        st.session_state.unique_classes,st.session_state.count_options = get_unique_classes_counts(metadata)

                        st.success(f"Successfully loaded metadata for {len(metadata)} images.")
                except Exception as e:
                    st.error(f"Error loading metadata: {str(e)}")
            else:
                st.warning(f"Please enter metadata file path")

## Search Functionality

if st.session_state.metadata:
    st.header("🔍 Search Engine")

    with st.container():
        st.session_state.search_params["search_mode"] = st.radio(
            "Search mode:",
            (
                "Any of selected classes (OR)",
                "All selected classes (AND)"
            ),
            horizontal=True
        )

        unique_classes = st.session_state.unique_classes

        selected_classes = st.multiselect(
            "Classes to select:",
            options=unique_classes,
            key="selected_classes"
        )

        typed_classes = st.text_input(
            "Or search particular object:",
            placeholder="e.g. person, car, bicycle"
        )

        # Split comma-separated class names
        text_classes = list(dict.fromkeys(
            cls.strip()
            for cls in typed_classes.split(",")
            if cls.strip()
        ))

        # Case-insensitive validation
        class_lookup = {
            cls.lower(): cls for cls in unique_classes
        }

        valid_classes = []
        invalid_classes = []

        for cls in text_classes:
            if cls.lower() in class_lookup:
                valid_classes.append(class_lookup[cls.lower()])
            else:
                invalid_classes.append(cls)

        # Display validation errors
        if invalid_classes:
            st.error(
                f"Class(es) not found: {', '.join(invalid_classes)}. "
                "Please enter valid class names or select them "
                "from the dropdown."
            )

        # Combine selected and valid typed classes
        all_classes = list(dict.fromkeys(
            selected_classes + valid_classes
        ))

        st.session_state.search_params["select_classes"] = all_classes

        if all_classes:
            st.caption(f"Selected classes: {', '.join(all_classes)}")

        # Set threshold
        if st.session_state.search_params["select_classes"]:
            st.subheader("Count Threshold(optional)")
            cols = st.columns(len(st.session_state.search_params["select_classes"]))

            for i, cls in enumerate(st.session_state.search_params["select_classes"]):
                with cols[i]:
                    st.session_state.search_params["thresholds"][cls] = st.selectbox(
                        f"Max count for {cls}",
                        options=["None"] + st.session_state.count_options[cls]
                    )

        if st.button("Search Images", type="primary") and st.session_state.search_params["select_classes"]:
            results = []
            search_params = st.session_state.search_params

            for item in st.session_state.metadata:
                matches = False
                class_matches = {}

                for cls in search_params["select_classes"]:
                    class_detections = [d for d in item['detections'] if d['class'] == cls]

                    class_count = len(class_detections)
                    class_matches[cls] = False

                    threshold = search_params["thresholds"].get(cls,"None")

                    if threshold=="None":
                        class_matches[cls]=(class_count>=1)
                    else:
                        class_matches[cls]=(class_count>=1 and class_count<= int(threshold))

                if search_params["search_mode"] == "Any of selected classes (OR)":
                    matches=any(class_matches.values())
                else:
                    matches = all(class_matches.values())


                if matches:
                    results.append(item)

            st.session_state.search_results = results
