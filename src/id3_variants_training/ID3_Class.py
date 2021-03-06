import numpy
from anytree.exporter import DotExporter
from .ID3_Node import ID3_Node


class ID3:

    def __init__(self, api, verbose=True):
        """
        Initializes the ID3 class

        Args:
            api (LOCAL_API | CanDIG_API): API object that is used to interact with the virtual API

        Attributes:
            api (LOCAL_API | CanDIG_API): API object that is used to interact with the virtual API
            root_node (Node): Creates the root node of the tree to be added upon

        TODO:
            * Add logging so user can know if the classifier is working
        """
        self.api = api
        subset = self.api.get_target_set()
        self.root_node = ID3_Node('root', subset, True)
        self.verbose = verbose
        self.ID3(self.root_node, self.verbose)
        if verbose:
            print("")


    @staticmethod
    def get_subset_count(subset):
        """
        Args:
            subset (dict): A dictionary containing keys of ancestries and values of the counts for the particular ancestry

        Returns:
            ret_str: A string containing counts of the subset and the name of the most common subset
        """
        max_key = str(max(subset, key=subset.get))
        total_count = str(sum(subset.values()))
        ret_str = "most common ancestry: %s,%s | total count: %s" % (max_key, subset[max_key], total_count)
        return ret_str

    @staticmethod
    def entropy_by_count(subset):
        """
        Gets the entropy given an input of a subset

        Args:
            subset (dict): A dictionary containing keys of ancestries and values of the counts for the particular ancestry

        Returns:
            entropy (float): the entropy value of the subset used for the ID3 algorithm
        """
        values = numpy.array(list(subset.values()))
        total = values.sum()
        proportion = values[numpy.where(values > 0)]/total
        entropy = -numpy.sum(proportion * numpy.log2(proportion))
            
        return entropy

    def predict(self, include_variants):
        """
        Traverses the tree and finds the leaf node corresponding to the list of included variants
        as the input

        Args:
            include_variants (list):  list of variants that are included in the particular person

        Returns:
            node (ID3_Node): Custom object that has information about the leaf node
        """
        node = self.root_node
        # finds leaf node 
        while node.children:
            lastnode = node
            for child_node in node.children:
                # walk in in the path with the variant
                if (child_node.variant_name in include_variants) and (child_node.with_variant):
                    node = child_node
                    break
                # walk in the path without the variant
                elif (child_node.variant_name not in include_variants) and (not child_node.with_variant):
                    node = child_node
                    break

            if node == lastnode:
                return node

        return node


    def is_leaf_node(self, subset, split_path, split_index):
        """
        Checks if the node is a leaf node given a subset

        Args:
            subset (dict): A dictionary containing keys of ancestries and values of the counts for the particular ancestry
            split_path (list1, list2): 
                This is the paths of the splits before the current split. The first list
                is the list of variant names and the second list is the direction
                of the split. The direction of the second list is depicted by 1's
                and 0's. Where 1 is splitting in the direction with the variant
                and 0 is splitting in the direction without the variant. 
            split_index (int): the index for the next split to be split on

        Returns:
            (bool): the boolean value represents whether or not the node is a leaf node

        TODO:
            * Clean up leaf node if statement and ensure it is still valid
            * See why entropy by count == 0 doesn't do much


        """
        # check if all variants are of one ancestry (Essentially if all remaining variants(attributes) contains one region(value))
        attr_list = set()
        upd_var_count = { k : v for k, v in subset.items() if v != 0 }
        attr_list.update(upd_var_count.keys())
        if len(attr_list) == 1 or len(split_path[0]) >= len(self.api.variant_name_list) or split_index is None or ID3.entropy_by_count(subset) == 0:
        #if len(attr_list) == 1 or len(split_path[0]) >= 5 or split_index is None or ID3.entropy_by_count(subset) == 0:
            return True
        return False

    def print_tree(self, file_name):
        DotExporter(self.root_node, nodenamefunc=ID3_Node.name_func).to_picture(file_name)

    @staticmethod
    def calc_other_split_variant_counts(w_var_counts, subset):
        """
        Given a subset that has been split, and counts on one side of the split,
        calculate counts on the other side.

        In the normal case, this is trivial; but if the counts include differentially
        private noise, w_var_counts[ancestry1] could exceed subset[ancestry1].

        This routine prevents that by capping the counts counts in the (mutable)
        dictionary w_var_counts, then doing the subtraction.

        Args:
            w_var_counts (dict): A dictionary containing keys of ancestries and counts on one side of the split
            subset (dict): A dictionary containing keys of ancestries and counts in the parent

        Returns:
            w_var_counts(dict): A possibly updated w_var_counts, after capping
            wo_var_counts(dict): Dictionary on other side of the count
        """
        new_w_var_counts = {}
        wo_var_counts = {}
        for key, value in w_var_counts.items():
            subset_value = subset.get(key, 0)
            if value > subset_value:
                value = subset_value
            if value < 0:
                value = 0
            new_w_var_counts[key] = value
            wo_var_counts[key] = subset_value - value

        return new_w_var_counts, wo_var_counts


    def find_variant_split(self, subset, split_path):
        """
        Finds the variant to split on and returns the index where it should be split on.
        This calculation is based on which attribute gives the greatest information gain.

        Args:
            subset (dict): A dictionary containing keys of ancestries and values of the counts for the particular ancestry
            split_path (list1, list2): 
                This is the paths of the splits before the current split. The first list
                is the list of variant names and the second list is the direction
                of the split. The direction of the second list is depicted by 1's
                and 0's. Where 1 is splitting in the direction with the variant
                and 0 is splitting in the direction without the variant. 

        Returns:
            ret_index (int): index that yields the greatest information gain

        """

        variant_list = self.api.find_next_variant_counts(split_path)
        total_count = sum(subset.values())
        ret_index = 0
        final_info_gain = 0
        var_idx_list = [self.api.variant_name_list.index(var_name) for var_name in split_path[0]]

        if total_count <= 1:
            return None

        # loops through all the counts for each variant
        for idx, w_var_counts in enumerate(variant_list):
            w_var_counts, wo_var_counts = self.calc_other_split_variant_counts(w_var_counts, subset)
            w_fraction = sum(w_var_counts.values()) / total_count
            wo_fraction = sum(wo_var_counts.values()) / total_count
            if w_fraction == 0. or wo_fraction == 0.:
                continue

            # calculates info gain
#            info_gain = ID3.entropy_by_count(subset) - ( sum(wo_var_counts.values()) / total_count * ID3.entropy_by_count(wo_var_counts) + sum(w_var_counts.values()) / total_count * ID3.entropy_by_count(w_var_counts) )
            info_gain = ID3.entropy_by_count(subset) - (wo_fraction * ID3.entropy_by_count(wo_var_counts) + 
                                                        w_fraction * ID3.entropy_by_count(w_var_counts))
            # finds max info gain and checks if the index is not in excluded variants list
            if final_info_gain < info_gain and idx not in var_idx_list:
                final_info_gain = info_gain
                ret_index = idx
        # checks if there is any info gain
        if final_info_gain <= 0.1:
            return None
        return ret_index

    # note: variant list must be same length as count list
    def ID3(self, node, verbose=True):
        """
        A recursive function that creates a tree given the root node and a subset

        Note: variant list must be same length as count list

        Args:
            node (Node): A node object from the anytree library
            split_path (list1, list2): 
                This is the paths of the splits before the current split. The first list
                is the list of variant names and the second list is the direction
                of the split. The direction of the second list is depicted by 1's
                and 0's. Where 1 is splitting in the direction with the variant
                and 0 is splitting in the direction without the variant. 

        TODO:
            * Clean up if statements that check if the subset values are greater than 0 (should be taken care of in leaf node calc)

        """
        # find the attrivute to split on and adds that variant to exclude variant list
        self.verbose = verbose
        if self.verbose:
            print('.', end='', flush=True)
        subset = node.subset
        split_index = self.find_variant_split(subset, node.split_path)
        if split_index is None:
            return
        if not self.is_leaf_node(subset, node.split_path, split_index):
            var_name = self.api.variant_name_list[split_index]

            w_subset, wo_subset = self.api.split_subset(node, var_name)
            w_split_path, wo_split_path = self.api.create_split_path(node.split_path, var_name)


            if sum(w_subset.values()) > 0:
                self.ID3(ID3_Node(var_name, dict(w_subset), with_variant=True, split_path=w_split_path, parent=node), self.verbose)
            if sum(wo_subset.values()) > 0:
                self.ID3(ID3_Node(var_name, dict(wo_subset), with_variant=False, split_path=wo_split_path, parent=node), self.verbose)