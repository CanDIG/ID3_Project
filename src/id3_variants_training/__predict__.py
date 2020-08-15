from .ConfusionMatrix import ConfusionMatrix
import pickle


def predict():
    id3_tree_file = open('id3_tree', 'rb')
    id3_tree = pickle.load(id3_tree_file)
    id3_tree_file.close()

    conf_matrix = ConfusionMatrix(id3_tree)
    print(conf_matrix)


if __name__ == '__main__':
    predict()
