import tensorflow as tf
import streamlit as st
from PIL import Image
import helpers as h
import constants as c
import numpy as np
import pyvista as pv

# Streamlit UI
st.title("2D Image to 3D Voxel Grid Prediction")
st.write("Upload a PNG or JPG image, and get a 3D object file as an output.")

model_selected = st.selectbox(
    "Select your model based on your object:",
    tuple(c.LOW_CAPACITY_LABELS + c.HIGH_CAPACITY_LABELS),
)

# File upload
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg"])

if uploaded_file is not None and model_selected is not None:

    # Retrieve model name from selected option
    model_name, capacity_label = h.get_model_name(model_selected)

    # Load your CNN model (replace 'model_path' with the path to your .keras model file)
    model = tf.keras.models.load_model(c.MODELS_BASE_PATH + f"/{capacity_label}/{model_name}.keras")

    # Read uploaded image
    image_upload = Image.open(uploaded_file)
    st.image(image_upload, caption='Uploaded Image', use_column_width=True)
    h.save_npy_array_from_png([uploaded_file], (128, 128), npy_filename="temp/image")
    
    # Preprocess image for the model
    image_numpy = np.load('temp/image.npy')
    
    # Model prediction
    with st.spinner("Predicting 3D object..."):
        y_pred = model.predict(image_numpy)
        del model
    
    # Save the prediction as OBJ file
    y_pred = h.post_process_predicted_voxel(y_pred[0, :, :, :, 0])
    h.save_voxel_grid_to_obj(y_pred, 'temp/predicted_output.obj')

    # Visualize result
    if st.button("Visualize"):
        # Create a sample 3D boolean NumPy array (voxel grid)
        voxel_grid = y_pred

        # Define the grid dimensions and spacing
        grid = pv.ImageData()
        grid.dimensions = np.array(voxel_grid.shape) + 1  # Add 1 for proper cell representation
        grid.spacing = (1, 1, 1)  # Optional: Set the spacing between grid cells

        # Add the boolean array as cell data (voxel representation)
        grid.cell_data["values"] = voxel_grid.flatten(order="F")  # Flatten in Fortran order

        # Apply a threshold filter to extract only filled voxels
        thresholded = grid.threshold(0.5)  # Thresholding separates True (filled) from False (empty)

        # Visualize the 3D object
        plotter = pv.Plotter()
        plotter.show_axes()
        actor = plotter.add_mesh(thresholded, color="gray", show_edges=True)
        actor.rotate_x(90)
        actor.rotate_y(-45)
        plotter.show()

    # Provide download link
    st.success("Prediction complete! You can download the 3D object below.")
    with open('temp/predicted_output.obj', "rb") as f:
        st.download_button(
            label="Download 3D OBJ file",
            data=f,
            file_name='predicted_output.obj',
            mime="application/octet-stream"
        )

st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{c.IMAGE_URL}");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
