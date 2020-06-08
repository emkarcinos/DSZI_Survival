import os
from random import randint
import cv2
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np


class NN:
    def __init__(self):
        self.model = load_model('src/AI/NeuralNetwork/model.h5')
        self.IMG_SIZE = 64
        self.game_images = []
        self.CATEGORIES = ["Apple", "Pear"]
        self.X = []
        self.y = []
        self.load_images()
        self.images_used = []

    def show_picture(self, picture_id):
        plt.imshow(self.game_images[picture_id][0])
        plt.savefig("mygraph.png")
        #print("this is: " + self.CATEGORIES[self.game_images[picture_id][1]])

        show_img = cv2.imread("mygraph.png")
        cv2.imshow('image', show_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def load_images(self):
        DATADIR = "data/AI_data/Nn_images"
        for category in self.CATEGORIES:
            path = os.path.join(DATADIR, category)
            class_num = self.CATEGORIES.index(category)
            for img in os.listdir(path):
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (self.IMG_SIZE, self.IMG_SIZE))
                self.game_images.append([new_array, class_num])

        for features, label in self.game_images:
            self.X.append(features)
            self.y.append(label)
        self.X = np.array(self.X).reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 1)
        self.X = self.X / 255.0

    def predict_image(self):
        while True:
            random_num = randint(0, len(self.game_images) - 1)
            if random_num not in self.images_used:
                self.images_used.append(random_num)
                break
        self.show_picture(random_num)
        predictions = self.model.predict(self.X)
        print("this is my prediction: " + self.CATEGORIES[np.argmax(predictions[random_num])])
        if np.argmax(predictions[random_num]) == self.y[random_num]:
            return True, self.CATEGORIES[np.argmax(predictions[random_num])]
        else:
            return False, self.CATEGORIES[np.argmax(predictions[random_num])]

"""
pm = CNN()
print(pm.predict_image())
print()
print(pm.predict_image())
print()
print(pm.predict_image())
print()
print(pm.predict_image())
print()
print(pm.predict_image())
print()
print(pm.predict_image())
print()
print(pm.predict_image())
print()



"""