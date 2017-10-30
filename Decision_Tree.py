import math
import random
import copy


class Node:
    def __init__(self,split_variable = None, left_child = None,right_child = None,classifier_set = None, label = None):
        self.split_variable = split_variable
        self.left_child = left_child
        self.right_child = right_child
        self.classifier_set = classifier_set
        self.label = label
    def get_name(self):
        return 'Node'

class Validator:

    def __init__(self):
        self.rawdata = None

    # Load the CSV file, and return the list of raw data
    def load_file(self, filename):
        file = open(filename, "r")
        data_string = file.read()
        # split data by lines
        data_list = data_string.splitlines()
        raw_data_ = data_list
        self.Attributes = []
        for i in range(0, 20):
            self.Attributes.append(i)
        self.attributeNames = data_list[0].split(',')
        for index in range(1, len(data_list)):
            raw_data_[index - 1] = data_list[index].split(',')
        # for index1 in range(1, len(data_list)):
        #     raw_data.append(new_list(index1))
        raw_data_.pop(600)
        self.rawdata = raw_data_

    #calculate the accuracy from the test dataset
    def Calculate_Accuracy(self, root):
        # it the tree does not exist or the dataset is empty, return 0
        if root == None or len(self.rawdata) == 0:
            return 0
        # Count the correct prediction
        correct = 0
        for i in range(len(self.rawdata)):
            prediction = self.predicted_value(root, self.rawdata[i])
            if prediction == self.rawdata[i][20]:
                correct += 1
        # Calculate and return the prediction accuracy
        self.accuracy = correct / len(self.rawdata)
        return self.accuracy

    #root is the root of the tree, data_row is the row of on a data
    def predicted_value(self, root, data_row):
        #base case
        # if the split variable is -1, means it is a leaf, the label is the prediction
        if root.split_variable == -1:
            return root.label
        #recursion
        # If an attribute value is 0, search in the left subtree, otherwise search the right,
        if data_row[root.split_variable] == '0':
            return self.predicted_value(root.left_child, data_row)
        else:
            return self.predicted_value(root.right_child, data_row)

    def show_accuracy(self):
        print('The accuracy of the decision tree is:')
        print(self.accuracy)

class Decision_Tree:


    def __init__(self):

        # for i in range(0, 19):
        #     self.decision_attribute_map.append(-1)
        self.root = Node()
        self.root.split_variable = -1
        self.Attributes = None
        self.attributeNames = None





    # Load the CSV file, and return the list of raw data
    def load_file(self,filename):
        file = open(filename, "r")
        data_string = file.read()
        # split data by lines
        data_list = data_string.splitlines()
        raw_data = data_list
        self.Attributes=[]
        for i in range(0,20):
            self.Attributes.append(i)
        self.attributeNames = data_list[0].split(',')
        for index in range(1, len(data_list)):
            raw_data[index - 1] = data_list[index].split(',')
        # for index1 in range(1, len(data_list)):
        #     raw_data.append(new_list(index1))
        raw_data.pop(600)
        return raw_data

    #calculate impurity
    def impurity(self, dataset):
        # number of class 1 and number of class0
        count_class1 = 0
        count_class0 = 0
        total = len(dataset)
        # get the number of class 1 and class 0
        for index in range(0, len(dataset)):
            if (dataset[index][20] == '1'):
                count_class1 += 1
            if (dataset[index][20] == '0'):
                count_class0 += 1
        # if 0 == total:
        #     impurity = 0
        else:
            impurity = count_class1*count_class0/(total*total)
        return impurity

    #calculate impurity gain, x is the index of the attribute
    def info_impurity_gain(self, dataset, x):
        # initiate index for x attribute being 0 and 1
        dataset1 = []
        dataset0 = []
        total = len(dataset)
        for index in range(0, len(dataset)):
            if (dataset[index][x] == '1'):
                dataset1.append(dataset[index])
            if (dataset[index][x] == '0'):
                dataset0.append(dataset[index])
        if (len(dataset0)==0 or len(dataset1)==0):
            return 0, dataset0, dataset1
        else:
            parent_impurity = self.impurity(dataset)
            children_impurity_fraction0 = len(dataset0)/total * self.impurity(dataset0)
            children_impurity_fraction1 = len(dataset1)/total * self.impurity(dataset1)
            gain = parent_impurity-(children_impurity_fraction0+children_impurity_fraction1)
        return gain, dataset0, dataset1
        # calculate the split point, which is of the greatest information gain, and returns two dataset of 0 and 1 for that attribute

    #split info by using impurity gain
    def impurity_split_info(self, dataset, Attributes):
        max = 0
        dataset1 = []
        dataset0 = []
        split_point = -1
        for attribute in Attributes:
            # if there is 0 gain found, means it cannot be splited ,return split point being -1
            info = self.info_impurity_gain(dataset, attribute)
            if (info[0] != 0):
                if (info[0] > max):
                    max = info[0]
                    split_point = attribute
                    dataset0 = info[1]
                    dataset1 = info[2]
        return split_point, dataset0, dataset1


    #Calculate entropy
    def entropy(self, dataset):
        #number of class 1 and number of class0
        count_class1 = 0
        count_class0 = 0
        total = len(dataset)
        #get the number of class 1 and class 0
        for index in range(0, len(dataset)):
            if(dataset[index][20] == '1'):
                count_class1+=1
            if(dataset[index][20] =='0'):
                count_class0+=1
        if(count_class0==0):
            entro_0 = 0
        else:
            entro_0 = -count_class0*math.log2(count_class0/total)/total
        if(count_class1==0):
            entro_1 = 0
        else:
            entro_1 = -count_class1*math.log2(count_class1/total)/total

        #calculate the entropy in the data set
        data_entropy = entro_0+entro_1
        return data_entropy

    #calculate gain, x is the index of attribute to split, and sub datase for attribute to 0 and 1
    def info_gain(self,dataset, x):
        #initiate index for x attribute being 0 and 1
        index_dataset1=0
        index_dataset0=0
        dataset1=[]
        dataset0=[]
        for index in range(0, len(dataset)):
            if(dataset[index][x]=='1'):
                dataset1.append(dataset[index])
            if(dataset[index][x]=='0'):
                dataset0.append(dataset[index])
        if(len(dataset0)==0 or len(dataset1)==0):
            return 0, dataset0, dataset1
        else:
            gain = self.entropy(dataset) - (len(dataset0)*self.entropy(dataset0)/len(dataset)+len(dataset1)*self.entropy(dataset1)/len(dataset))
            return gain,dataset0,dataset1

    # calculate the split point, which is of the greatest information gain, and returns two dataset of 0 and 1 for that attribute
    def split_info(self,dataset, Attributes):
        max = 0
        dataset1 = []
        dataset0 = []
        split_point = -1
        for attribute in Attributes:
            #if there is 0 gain found, means it cannot be splited ,return split point being -1
            info = self.info_gain(dataset, attribute)
            if(info[0]!=0):
                if (info[0] > max):
                    max = info[0]
                    split_point = attribute
                    dataset0 = info[1]
                    dataset1 = info[2]
        return split_point,dataset0,dataset1

    #decide value
    def decide_value(self,dataset):
        # number of class 1 and number of class0
        count_class1 = 0
        count_class0 = 0
        total = len(dataset)
        # get the number of class 1 and class 0
        for index in range(0, len(dataset)):
            if (dataset[index][20] == '1'):
                count_class1 += 1
            if (dataset[index][20] == '0'):
                count_class0 += 1
        if count_class0 >count_class1:
            return '0'
        else:
            return '1'



    # build tree by impurity gain
    def build_impurity_gain(self, dataset):
        self.root = self.split_impurity(dataset, self.Attributes)

    #build tree by information gain
    def build(self,dataset):
        self.root = self.split(dataset,self.Attributes)


    #split by impurity gain
    def split_impurity(self, dataset, Attributes):
        # If dataset is empty, return null
        if len(dataset) == 0:
            return None
        # Create a root node for the tree
        root = Node(-1)
        # Let the label of the  node be the most populat target value
        root.label = self.decide_value(dataset)
        if len(Attributes) == 0:
            return root
        else:
            splitpoint_info = self.impurity_split_info(dataset, Attributes)
            splitpoint = splitpoint_info[0]
            # it it cannot be furthur split, return root
            if splitpoint == -1:
                return root

            # Otherwise, let bestAttribute be the decision attribute for Root
            root.split_variable = splitpoint

            # get the remaining attribute
            newAttributes = []
            for attribute in Attributes:
                if attribute != splitpoint:
                    newAttributes.append(attribute)
            Attributes = newAttributes

            # Add a subtree below each branch
            root.left_child = self.split(splitpoint_info[1], Attributes)
            root.right_child = self.split(splitpoint_info[2], Attributes)

            return root
    #split by information gain
    def split(self, dataset, Attributes):
        # If dataset is empty, return null
        if len(dataset) == 0:
            return None
        # Create a root node for the tree
        root = Node(-1)
        # Let the label of the  node be the most populat target value
        root.label = self.decide_value(dataset)
        if len(Attributes) == 0:
            return root
        else:
            splitpoint_info = self.split_info(dataset, Attributes)
            splitpoint = splitpoint_info[0]
            # it it cannot be furthur split, return root
            if splitpoint == -1:
                return root

            # Otherwise, let bestAttribute be the decision attribute for Root
            root.split_variable = splitpoint

            # get the remaining attribute
            # Attributes - bestAttribute
            newAttributes = []
            for attribute in Attributes:
                if attribute != splitpoint:
                    newAttributes.append(attribute)
            Attributes = newAttributes

            # Add a subtree below each branch
            root.left_child = self.split(splitpoint_info[1], Attributes)
            root.right_child = self.split(splitpoint_info[2], Attributes)

            return root

    def Prunning(self,L, K, datafile):

        prunedTree = self.root

        # Create to test accuracy
        validator = Validator()
        validator.load_file(datafile)

        for i in range(1, L + 1):

            # Copy the tree
            dup_Tree = copy.deepcopy(prunedTree)
            node_list = []
            node_list = self.node_reorder(dup_Tree, node_list)
            nodes_count = len(node_list)
            M = random.randint(1, K)  # A random number between 1 and K.

            for j in range(1, M + 1):


                # randomly pick a node index, and assign split_variable =-1 to make it a leaf
                P = random.randint(1, nodes_count)
                randomNode = node_list[P-1]
                randomNode.split_variable = -1
                randomNode.left_child = None
                randomNode.right_child = None

            # Evaluate the accuracy of new tree on the validation set
            Accuracy = validator.Calculate_Accuracy(prunedTree)
            newAccuracy = validator.Calculate_Accuracy(dup_Tree)

            # If new tree is more accurate than D_Best, replace D_Best by D'
            if newAccuracy >= Accuracy:
                prunedTree = dup_Tree

        # Update the decision tree to be best tree and return prunned tree
        self.root = prunedTree
        return prunedTree

    #recursively find all none leaf nodes, and put it a list, and return the list
    def node_reorder(self, root, node_list):
        node_list.append(root)
        if((root.left_child != None) and (root.right_child != None)):
            self.node_reorder(root.left_child,node_list)
            self.node_reorder(root.right_child,node_list)
        return node_list



    #override
    def __str__(self):
        return self.ToString(self.root, 0, self.attributeNames)

    # toString
    def ToString(self, root, level, attributeNames):

        # Initia String
        string = ''
        if root.left_child is None and root.right_child is None:
            string += str(root.label) + '\n'
            return string
        # If root is none, return
        if root is None:
            return ''

        # Get the attribute name of the current node
        currNode = attributeNames[root.split_variable]
        levelBars = ''
        for i in range(0, level):
            levelBars += '| '

        # Append the level information to the front of attribute name
        string += levelBars
        if root.left_child.left_child is None and root.left_child.right_child is None:
            string += currNode + "= 0 :"
        else:
            string += currNode + "= 0 :\n"
        string += self.ToString(root.left_child, level + 1, attributeNames)

        # Append the level information to the front of attribute name
        string += levelBars

        if root.right_child.left_child is None and root.right_child.right_child is None:
            string += currNode + "= 1 :"
        else:
            string += currNode + "= 1 :\n"
        string += self.ToString(root.right_child, level + 1, attributeNames)

        # Return the tree
        return string








# training_data1 = 'F:\\Decision_Tree_Data_set\\data1\\training_set.csv'
# test_data1 = 'F:\\Decision_Tree_Data_set\\data1\\test_set.csv'
# validation_data1 = 'F:\\Decision_Tree_Data_set\\data1\\validation_set.csv'
# training_data2 = 'F:\\Decision_Tree_Data_set\\data2\\training_set.csv'
# test_data2 = 'F:\\Decision_Tree_Data_set\\data2\\test_set.csv'
# validation_data2 = 'F:\\Decision_Tree_Data_set\\data2\\validation_set.csv'

print("Please input arguments like this: L K training-set validation-set test-set to-print.")
print('Files include directories, or just the file name if they are in the program folder.')
print('Example: 20 15 F:\\Decision_Tree_Data_set\\data1\\training_set.csv F:\\Decision_Tree_Data_set\\data1\\validation_set.csv F:\\Decision_Tree_Data_set\\data1\\test_set.csv yes')
print('Or example: 20 15 training_set.csv validation_set.csv test_set.csv no')
input = input()
input = input.split(' ')
L = int(input[0])
K = int(input[1])
training_set = input[2]
validation_set = input[3]
test_set = input[4]
to_print = input[5]



# mocking data
# L = 30
# K = 30
# training_set = 'F:\\Decision_Tree_Data_set\\data1\\training_set.csv'
# validation_set = 'F:\\Decision_Tree_Data_set\\data1\\validation_set.csv'
# test_set = 'F:\\Decision_Tree_Data_set\\data1\\test_set.csv'
# to_print = 'yes'

#instantiate the trees for information gain and variance impurity
decision_tree_info_gain = Decision_Tree()
training_data1 = decision_tree_info_gain.load_file(training_set)
decision_tree_info_gain.build(training_data1)

decision_tree_variance_impurity = Decision_Tree()
training_data2 = decision_tree_variance_impurity.load_file(training_set)
decision_tree_variance_impurity.build_impurity_gain(training_data2)

#print the tree
if to_print == 'yes':
    print('Decision tree by using information gain heuristic:')
    print(decision_tree_info_gain)

    print('Decision tree by using variance impurity heuristic:')
    print(decision_tree_variance_impurity)

#instantiate the validator
validator = Validator()
validator.load_file(test_set)

#accuracy for info gain algorithm
print('accuracy for info gain algorithm:')
validator.Calculate_Accuracy(decision_tree_info_gain.root)
validator.show_accuracy()

#accuracy for variance impurity algorithm
print('accuracy for variance impurity algorithm:')
validator.Calculate_Accuracy(decision_tree_variance_impurity.root)
validator.show_accuracy()

#tree prunning
decision_tree_info_gain.Prunning(L, K, validation_set)
decision_tree_variance_impurity.Prunning(L, K, validation_set)

#new Accuracy
print('After prunning, the decision tree accuracy for infomation gain is:')
validator.Calculate_Accuracy(decision_tree_info_gain.root)
validator.show_accuracy()

print('After prunning, the decision tree accuracy for variance impurity is:')
validator.Calculate_Accuracy(decision_tree_variance_impurity.root)
validator.show_accuracy()










