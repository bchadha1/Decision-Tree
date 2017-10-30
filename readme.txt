Run the Decision_tree.py with command-line or IDE.
It will prompt user to input arguments.
Input format should be like: (L and K are integers that is used in post-pruning, it will iterate L times, and the prunning factor is a random number between 1 to K.)
L K training-set validation-set test-set to-print.
Files should be with directories, or just the file name if you put files in the program folder.
Sample data sets:
https://drive.google.com/open?id=0B7ncKnfbc0qTeWJoWnpvZVlobUU
https://drive.google.com/open?id=0B7ncKnfbc0qTVndFWklDckZSXzA

Example1:
20 15 F:\\Decision_Tree_Data_set\\data1\\training_set.csv F:\\Decision_Tree_Data_set\\data1\\validation_set.csv F:\\Decision_Tree_Data_set\\data1\\test_set.csv yes
Example2:
20 15 training_set.csv validation_set.csv test_set.csv no

Description:
Implemented decision tree learning algorithm without library.
It uses two heuristics:
1: Information gain heuristic(See Mitchell Chapter 3)
2: Variance impurity heuristic

After implementing the two heuristics, applies the post-prunning algorithm to reduce overfitting. It cuts down some branches therefore the decision tree
becomes more generic therefore fits better in predictive model.
