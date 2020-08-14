from .ID3_Class import ID3
from .local_API import LOCAL_API
from .ga4gh_API import GA4GH_API


class ConfusionMatrix(ID3):

    def __init__(self, api):
        """
        Creates confusion matrix with the first index (Y) as the correct population and the
        second index (X) as the predicted population. THe order of the ancestries is dictated
        by the ancestry_list within the api class

        actual is Y axis
        predicted is X axis

        Args:
            api (LOCAL_API | GA4GH_API): API object that is used to interact with the virtual API

        Attributes:
            api (LOCAL_API | GA4GH_API): API object that is used to interact with the virtual API
            root_node (Node): Creates the root node of the tree to be added upon

            length (int): length of all the ancestries
            conf_matrix (list): the confusion matrix based on the ID3 classifier
            diagonal_sum (int): sum of the diagonals within the matrix
            total (int): total sum of all values in matrix
        """
        super(ConfusionMatrix, self).__init__(api)

        # create conf_matrix and calculate useful attributes
        self.length = len(self.api.ancestry_list)
        self.conf_matrix = [[0] * self.length for _ in range(self.length)]

        for variants, popu in zip(self.api.test_variant_list, self.api.test_popu_list):
            include_variants = [self.api.variant_name_list[idx] for idx, is_variant in enumerate(variants) if is_variant == 1]

            # Actual Result
            y = self.api.ancestry_list.index(popu)
            # Predicted Result
            x = self.api.ancestry_list.index(self.predict(include_variants).most_common_ancestry)

            self.conf_matrix[y][x] += 1

        self.diagonal_sum = sum([self.conf_matrix[i][i] for i in range(self.length)])
        self.total = sum([sum(self.conf_matrix[i]) for i in range(self.length)])

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
    c = ConfusionMatrix()
    print(c)
    print(c.get_accuracy())
    print(c.get_prevalence('ESN'))
