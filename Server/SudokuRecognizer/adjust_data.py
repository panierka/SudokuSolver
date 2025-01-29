import os
from PIL import Image

def load_blank_paths(path):
    return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

def augment_image(img, path, dir_path):
    img = img.resize((28,28))
    base_name = os.path.splitext(os.path.basename(path))[0]
    for index, angle in enumerate([0, 90, 180, 270]):
        rotated_image = img.rotate(angle, expand=True)
        output_path = os.path.join(dir_path, f"{base_name}_rotated_{index}.jpg")
        rotated_image.save(output_path)

def execute_process(dir_path, output_path):
    paths = load_blank_paths(dir_path)
    for path in paths:
        image = Image.open(dir_path + '/' + path)
        augment_image(image, path, output_path)

def main():
    execute_process('data/train_data', 'data/augmented_train_data')
    execute_process('data/test_data', 'data/augmented_test_data')

if __name__ == '__main__':
    main()