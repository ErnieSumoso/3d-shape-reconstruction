from PIL import Image
import numpy as np
import constants as c

# Cast our predicted voxel to boolean values first, with a threshold of 0.5
def post_process_predicted_voxel(y_pred_instance):

    return (y_pred_instance > c.VOXEL_PREDICTION_THRESH).astype(bool)

# Function to get model name from selected option in the selectbox
def get_model_name(option_selected):
    # Set model name
    model_label = option_selected.split(" - ")[0]
    model_name = c.MODEL_NAME_DICT[model_label]

    # Set model capacity by checking 2nd element
    capacity_label = option_selected.split(" - ")[1]
    capacity_label = "low-capacity" if "low" in capacity_label else "high-capacity"
    return model_name, capacity_label


# Function to preprocess image for model prediction
def preprocess_image(image: Image.Image):
    # Resize image to (128, 128) and convert to grayscale
    image = image.convert("L")  # Convert to grayscale
    image = image.resize((128, 128))  # Resize to match input shape of the model
    image_np = np.array(image)  # Convert to numpy array
    image_np = image_np.astype('float32') / 255.0  # Normalize image
    image_np = np.expand_dims(image_np, axis=-1)  # Add channel dimension (128, 128, 1)
    image_np = np.expand_dims(image_np, axis=0)  # Add batch dimension (1, 128, 128, 1)
    return image_np

# Function to save a voxel grid into an OBJ file
def save_voxel_grid_to_obj(voxel_grid, filename):
    # Set vertices and faces for an individual cube
    vertices, faces = [], []
    vertex_index = 1

    # Iterate through the 3D array, processing each voxel
    for x in range(voxel_grid.shape[0]):
        for y in range(voxel_grid.shape[1]):
            for z in range(voxel_grid.shape[2]):

                # If the current voxel is occupied
                if voxel_grid[x, y, z] != 1:
                    continue
                    
                # Add the vertices for the cube/voxel
                for dx, dy, dz in c.VERTEX_OFFSETS:
                    vertices.append((x + dx, y + dy, z + dz))

                # Add the faces for the cube/voxel
                for face in c.FACE_OFFSETS:
                    faces.append((
                        vertex_index + face[0],
                        vertex_index + face[1],
                        vertex_index + face[2],
                        vertex_index + face[3]
                    ))

                # Update the vertex index
                vertex_index += 8

    # Write vertices and faces to an OBJ file
    with open(filename, 'w') as obj_file:
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            obj_file.write(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")


def save_npy_array_from_png(png_files, image_shape, save_npy=True, npy_filename='image'):
    
    # Loop through the PNG files and initialize an empty array that will contain np arrays
    np_arrays = []
    for i, png_file in enumerate(png_files):

        # Open the image and convert into grayscale
        img = Image.open(png_file)
        img_gray = img.convert("L")
        
        # Resize the image to the desired shape and into a numpy array
        img_resized = img_gray.resize(image_shape)
        img_array = np.array(img_resized)
        
        # Reshape the array to (image shape, 1)
        new_shape = tuple(list(image_shape) + [1])
        img_array = img_array.reshape(new_shape)
        np_arrays.append(img_array)
            
    # Save the voxel matrix as an NPY file
    np_arrays_stacked = np.stack(tuple(np_arrays), axis=0)
    
    # Save the NumPy array as an NPY file
    np.save(npy_filename + ".npy", np_arrays_stacked)
