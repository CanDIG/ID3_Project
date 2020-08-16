import pickle
from .local_API import LOCAL_API
import numpy

class ConfusionMatrix:

    def __init__(self, id3_tree, api):
        """
        Creates confusion matrix with the first index (Y) as the correct population and the
        second index (X) as the predicted population. THe order of the ancestries is dictated
        by the ancestry_list within the api class

        actual is Y axis
        predicted is X axis

        Args:
            id3_tree (ID3):

        Attributes:
            id3_tree (ID3):
            api (LOCAL_API): API object that is used to interact with the virtual API
            length (int): length of all the ancestries
            conf_matrix (list): the confusion matrix based on the ID3 classifier
            diagonal_sum (int): sum of the diagonals within the matrix
            total (int): total sum of all values in matrix
        """
        self.api = api
        self.id3_tree = id3_tree

        # create conf_matrix and calculate useful attributes
        self.length = len(self.api.ancestry_list)
        self.conf_matrix = numpy.zeros((self.length, self.length), dtype=numpy.int)

        for variants, popu in zip(self.api.variant_list, self.api.popu_list):
            include_variants = [self.api.variant_name_list[idx] for idx, is_variant in enumerate(variants) if is_variant == 1]

            # Actual Result
            y = self.api.ancestry_list.index(popu)
            # Predicted Result
            x = self.api.ancestry_list.index(self.id3_tree.predict(include_variants).most_common_ancestry)

            self.conf_matrix[y,x] += 1

        self.diagonal_sum = self.conf_matrix.diagonal().sum()
        self.total = self.conf_matrix.sum()

    def get_accuracy(self):
        """
        How often the classifier is correct

        Returns:
            (float): a number between 0 and 1
        """
        return self.diagonal_sum / self.total

    def get_misclassification_rate(self):
        """
        How often is the classifier wrong

        Returns:
            (float): a number between 0 and 1
        """
        return 1 - self.get_accuracy()

    def get_hit_rate(self, ancestry):
        """
        For a particular ancestry, how often does it predict the correct ancestry

        Args:
            ancestry (string): a three character code depicting populations of people

        Returns:
            (float): a number between 0 and 1
        """
        if ancestry not in self.api.ancestry_list:
            print("Not a valid ancestry")
            return None

        popu_i = self.api.ancestry_list.index(ancestry)
        true_anc = self.conf_matrix[popu_i][popu_i]
        sum_actual_anc = sum(self.conf_matrix[popu_i])

        return true_anc / sum_actual_anc

    def get_miss_rate(self, ancestry):
        """
        For a particular ancestry, how often does it predict the incorrect ancestry

        Args:
            ancestry (string): a three character code depicting populations of people

        Returns:
            (float): a number between 0 and 1
        """
        hit_rate = self.get_hit_rate(ancestry)
        if not hit_rate:
            return None

        return 1 - hit_rate

    def get_precision(self, ancestry):
        """
        For a particular ancestry, how often is the prediction correct

        Args:
            ancestry (string): a three character code depicting populations of people

        Returns:
            (float): a number between 0 and 1
        """
        if ancestry not in self.api.ancestry_list:
            print("Not a valid ancestry")
            return None

        popu_i = self.api.ancestry_list.index(ancestry)
        true_anc = self.conf_matrix[popu_i][popu_i]
        sum_pred_anc = sum([self.conf_matrix[i][popu_i] for i in range(self.length)])

        return true_anc / sum_pred_anc

    def get_prevalence(self, ancestry):
        """
        How often does the ancestry appear in the sample relative to the sum of all ancestries

        Args:
            ancestry (string): a three character code depicting populations of people

        Returns:
            (float): a number between 0 and 1
        """
        if ancestry not in self.api.ancestry_list:
            print("Not a valid ancestry")
            return None

        popu_i = self.api.ancestry_list.index(ancestry)
        sum_actual_anc = sum(self.conf_matrix[popu_i])

        return sum_actual_anc / self.total

    def __str__(self):
        return '\n'.join([str(self.conf_matrix[i]) for i in range(len(self.conf_matrix))])


if __name__ == "__main__":
    l_api = LOCAL_API('./test_cases/case1/config.json', False)
    with open('case1.id3') as model_file:
        id3_model = pickle.load(model_file)
    conf_matrix = ConfusionMatrix(id3_model, l_api)
    print(conf_matrix)