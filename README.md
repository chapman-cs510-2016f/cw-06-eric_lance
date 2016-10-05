# CS510 CW 6

**Author(s):** _Eric & Lance_

[![Build Status](https://travis-ci.org/chapman-cs510-2016f/cw-06-eric_lance.svg?branch=master)](https://travis-ci.org/chapman-cs510-2016f/cw-06-eric_lance)

**Due date:** 2016/10/11

## Specification

**Note: Remember to use Python 3.**

Complete the following exercises, saving your solutions in the indicated files. For Python files that include test functions, GitHub will automatically run your tests with ```python -m "nose"``` on every commit, indicating any failures via the Travis framework in the build status image above.

1. Find another group: link each other your latest CW05, so that you can evaluate each other's code.  
    * Open a Jupyter notebook: ```critique-YOURGROUP-THEIRGROUP.ipynb```
    * Constructively critique their code in your Jupyter notebook. Use the following questions as a guideline: Is it clear how the code is organized? Is the code properly documented with both docstrings and supplementary comments according to industry standards? Can you follow the algorithm of the code, i.e., what it is doing, and how? Do you see any suggestions for how to improve the code? Discuss your critique with the members of the other group.
    * Send each other your respective critiques. Commit both your critique and their critique to your repository.
1. Work through the [Numpy/Pandas slides](http://slides.com/profdressel/numpy-and-pandas-overview) carefully. Be sure to use ```ipython3``` in a terminal to test how things work. Discuss amongst yourselves anything that is new or unclear.
1. Create a python module ```cplane-np.py```. Import the module ```abscplane.py``` in the repository. Create a new class ```ComplexPlaneNP``` that subclasses the abstract base class ```AbsComplexPlane```. Provide implementations for the requested methods using ```numpy``` arrays augmented with ```pandas``` labels. Be sure to set all attributes properly during the ```__init__``` constuctor.
1. In a Jupyter notebook ```cw06-cplane-np.ipynb``` provide a demonstration of how your class works. Be sure to switch the default kernel to Python 3 instead of the default Python 2 used by Sage. Include a detailed discussion comparing this implementation with your previous implementation using vanilla python lists.
1. In your python module create a function ```julia(c, max=100)``` that takes a complex parameter ```c``` and an optional positive integer ```max```, and returns a function specified by the following: 
    * The function should take one complex parameter ```z``` as an input, and return a positive integer ```n```.
    * The returned integer ```n``` should count how many times the complex parameter ```z``` can be transformed as ```z = z**2 + c``` before the resulting magnitude ```|z|``` exceeds 2. 
    * If the number ```max``` is reached before the magnitude of ```z``` exceeds 2, the function should return the number 0. 
    * If the number ```z``` already has a magnitude larger than 2, the function should return 1.
1. Explain in your notebook how to test whether your function ```julia``` is producing correct results. Write test functions for ```nose``` that verify that your implementation is correct.
1. After your notebooks are complete, spell-checked, and professionally formatted properly, add and commit them to GitHub. Note that managing conflicts with Jupyter notebooks can be a pain, so I recommend having only one person from your edit the notebooks at a time, being sure to pull all changes before you start editing yourself.


## Assessment

Analyze in this section what you found useful about this assignment in your own words. Include any lingering questions or comments that you may have.

**CHANGEME**

## Honor Pledge

I pledge that all the work in this repository is my own with only the following exceptions:

* Content of starter files supplied by the instructor;
* Code borrowed from another source, documented with correct attribution in the code and summarized here.

Signed,

Eric & Lance
