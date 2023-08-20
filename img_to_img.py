import tensorflow
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from numpy.linalg import norm
import os
from tqdm import tqdm
import pickle
from PIL import Image


model = ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
model.trainable = False

model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])


def extract_features(img_path, model):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
    except Image.UnidentifiedImageError:
        print(f"Skipping unreadable image: {img_path}")
        return None
    except OSError:
        print(f"Corrupted image: {img_path}")
        return None
    
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result


filenames = []
for i, file in enumerate(os.listdir('fashionIQ_dataset\images')):
    if i >= 1000:  # Break the loop after 1000 iterations
        break
    filenames.append(os.path.join('fashionIQ_dataset\images', file))


feature_list = []

for file in tqdm(filenames):
    normalized_result = extract_features(file, model)
    if normalized_result is not None:  # Skip None values
        feature_list.append(normalized_result)

feature_list = np.array(feature_list)  # Convert the list to a NumPy array


pickle.dump(feature_list,open('embeddings.pkl','wb'))
pickle.dump(filenames,open('filenames.pkl','wb'))