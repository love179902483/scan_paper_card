from keras.models import load_model
import matplotlib.pyplot as plt
from keras.datasets import mnist
import os 

def loadImg(datas):
    InventoryPath = os.path.join(os.getcwd(), 'inventory', 'kerasStandard', 'keras_03.h5') 
    print(InventoryPath)
    model = load_model(InventoryPath)
    test = datas
    # plt.imshow(test[9])
    # plt.show()
    # print(type(test))
    # print(test.shape)
    # print(test)
    # print(datas)
    img_rows, img_cols = 28, 28

    x_test = test.reshape(test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

    print(x_test.shape)
    print(model.predict(x_test))


    # filters = 32
    # # size of pooling area for max pooling
    # pool_size = 2