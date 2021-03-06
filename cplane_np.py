#!/usr/bin/env python3

import abscplane as absc
import numpy as np
import pandas as pd

"""This is the Class ComplexPlaneNP.  It is built from the Abstract Class AbsComplexPlane.
This Class serves as a simplistic pan/zoom over a 2D complex plane, where each point in the
plane undergoes a transformation through the function f(), where the value at the coordinate
point is:
    value = f( x + yj )

This class uses the data structures available in numpy and pandas.  The array data structure
is used from numpy to set up the rows for the plane.  The rows are then inserted into a pandas
DataFrame and given row and column names to help identify the rows and columns in the plane.

The contents of each 'cell' in the ComplexPlaneNP is of type imaginary number.
"""
class ComplexPlaneNP(absc.AbsComplexPlane):

    def __init__(self, newXmin=-5., newXmax=5., newYmin=-5., newYmax=5., f=lambda x: x):
        """This is the creator.  It can be passed the the min/max X and Y values for the plane,
        and a transformation function (f).  There are default values if the parameters are not
        passed to the creator.
        The creator then generates a 2D plane filled with the X & Y complex number coordinates
        of the specified plane transformed by the function f().  Note that the default function
        f() for computing the values in the plane is the identity function, so the values at
        the coordinate location are the coordinates themselves.  Note also that the number of
        points in each axis is always forced to be fixed value.
        """
        self.xmin = newXmin
        self.xmax = newXmax
        self.ymin = newYmin
        self.ymax = newYmax
        self.xlen = 21
        self.ylen = 21
        #  must sub 1 to get the correct actual step size, otherwise last element does not equal x or y max
        self.xstep = (self.xmax - self.xmin)/(self.xlen - 1)
        self.ystep = (self.ymax - self.ymin)/(self.ylen - 1)
        self.f = f
        #  call refresh() to generate the the plane and its contents
        self.refresh()



    def refresh(self):
        """Regenerate complex plane.
        For every point (x + y*1j) in self.plane, replace
        the point with the value self.f(x + y*1j). 
        """
        planeArray = np.empty([self.xlen,self.ylen], dtype=complex)
        for xpos in range(self.xlen):
            for ypos in range(self.ylen):
                #  compute the value at each of the coordinate points in the plane
                planeArray[(self.ylen-ypos-1),xpos] = self.f( (xpos*self.xstep+self.xmin) + (ypos*self.ystep+self.ymin)*1j )
        ylabels = [str(self.ymax-ypos*self.ystep) for ypos in range(self.ylen)]
        xlabels = [str(xpos*self.xstep+self.xmin) for xpos in range(self.xlen)]
        self.plane = pd.DataFrame(planeArray, index=ylabels, columns=xlabels)



    def zoom(self,newXmin,newXmax,newYmin,newYmax):
        """Reset self.xmin, self.xmax, and/or self.xlen.
        Also reset self.ymin, self.ymax, and/or self.ylen.
        Zoom into the indicated range of the x- and y-axes.
        Refresh the plane as needed."""
        # note that xstep and ystep must be recalculated for the new min and max
        self.xmin = newXmin
        self.xmax = newXmax
        self.ymin = newYmin
        self.ymax = newYmax
        self.xstep = (self.xmax - self.xmin)/(self.xlen - 1)
        self.ystep = (self.ymax - self.ymin)/(self.ylen - 1)
        self.refresh()



    def set_f(self, f):
        """Reset the transformation function f.
        Refresh the plane as needed."""
        self.f = f
        self.refresh()



def julia(c, max=100):
    """This method creates and returns a function, f.  The parameters passed to julia are:
    c - an imagery valued constant that is used in the function f.
    max - an optional argument that sets the maximum loop count within f.  Default is 100.

    The function f requires a single parameter:
    z - an imaginary number

    f then performs the operation z = z**2 + c on the z passed to f along with the c value passed to julia.
    The operation is performed up to max times.
    The function f returns:
    1 - if the magnitude of the imagiary number (z) passed in exceeds 2
    n - count of the number of times the operation can be done *before* the magnitude of z exceeds 2
    0 - if the max iterations through the loop is reached without the magnitude of z reaching 2

    Note that f's return value of 1 is ambiguous:  it could be because the initial z was too large,
    or because the operation could be performed once successfully.
    """
    def f(z):
        # check to see if the input is already too big
        if abs( z ) <= 2:
            n = 0
            while abs(z)<=2:
                #  perform the operation
                z = z**2 + c
                print( z, abs(z), n )
                #  have we exceeded our max loop count-1?
                if n >= max:
                    n = 1
                    break
                #  count the number of times through the loop
                n+=1
            n -= 1  # subtract one to count the total loops *before* exceeding 2, also reports 0 if max loop reached
        else:
            #  report input too big
            n = 1
        return n

    #  return the function pointer to the caller of the julia() method
    return f





#  unit testing functions beyond this point

def _do_julia( c, z, loop_max = 100 ):
    """This private function is for testing julia only"""
    f = julia( c, loop_max )
    return f( z )


def test_julia_1():
    """Test the julia function for returning the correct count"""
    success  = False
    expected = 3

    #  perform the julia test and check the return value
    actual = _do_julia( 0.2 + 0.2j, 0.7 + 0.7j ) 
    if expected == actual:
        success = True

    message = 'Julia function did not return expected count:  actual %d expected %d' % (actual, expected)
    assert success, message


def test_julia_2():
    """Test the julia function for returning the zero if the loop count is exceeded"""
    success  = False
    expected = 0

    #  perform the julia test and check the return value
    actual = _do_julia( 0.1 + 0.1j, 0.1 + 0.1j, 10 )
    if expected ==  actual:
        success = True

    message = 'Julia function was expected to exceed the loop count:  actual %d expected %d' % (actual, expected)
    assert success, message


def test_julia_3():
    """Test the julia function for returning that the magnitude of the starting value is too large"""
    success  = False
    expected = 1

    #  perform the julia test and check the return value
    actual = _do_julia( 2 + 2j, 7 + 7j )
    if expected == actual:
        success = True

    message = 'Julia function did not report the z magnitude already too big:  actual %d expected %d' % (actual, expected)
    assert success, message


def test_julia_4():
    """Test the julia function to make sure a subsequent call to julia does not change the parameters and
    operation of the first call to julia"""
    success  = False

    #  make the first julia function
    f1 = julia( 0.2 + 0.2j, 10 )
    #  make the results from this call the expected outcome
    expected = f1( 0.7 + 0.7j )

    # make the second julia function
    f2 = julia( -0.2 + -0.2j, 2 )

    #  call the first julia function again and make sure the output matches the first call
    actual = f1( 0.7 + 0.7j )

    # how'd we do??
    if expected == actual:
        success = True

    message = 'Julia function internals changed between indpendent instatiations:  actual %d expected %d' % (actual, expected)
    assert success, message


def test_julia_5():
    """Test the julia function to make sure two different function instantiations yield two different results
    even with the same z value passed to the returned functions"""
    success  = False

    #  make the first julia function
    f1 = julia( 0.2 + 0.2j, 10 )

    # make the second julia function
    f2 = julia( -0.2 + -0.2j, 2 )

    #  call the first julia function again and make sure the output matches the first call
    #  make the results from this call the expected outcome
    expected = f1( 0.7 + 0.7j )
    actual = f2( 0.7 + 0.7j )

    # how'd we do??
    if expected != actual:
        success = True

    message = 'Different julia functions constants returned the same value:  f1 %d f2 %d' % (actual, expected)
    assert success, message


def test_init_no_params():
    """Test the creator by passing no parameters.  Since default values are used in place of missing parameters
       this should *not* cause a TypeError exception"""
    success = True

    try:
        testPlane = ComplexPlaneNP()
    except TypeError:
        """test passes"""
        success = False

    message = 'Creator should not have generated a TypeError exception, as all unpassed parameters have default values'
    assert success, message


def test_init():
    """Test the creator by passing the required parameters.  The passed in values should match the object's values"""
    success = True

    try:
        xmin = 2
        xmax = 6
        ymin = -6
        ymax = -2
        testPlane = ComplexPlaneNP( xmin, xmax, ymin, ymax )

        #  this line is to force an error to prov the test can fail
        # xmin = xmin + 1

        #  check that the parameters are all correctly stored
        if testPlane.xmin != xmin or testPlane.xmax != xmax or testPlane.ymin != ymin or testPlane.ymax != ymax:
           message = 'Init parameter mismatch: expected %d %d %d %d, actual %d %d %d %d' % (xmin, xmax, ymin, ymax, testPlane.xmin, testPlane.xmax, testPlane.ymin, testPlane.ymax)
           success = False

    except TypeError:
        """Test fails, should not have generated an exception"""
        message = 'Creator generated an exception when correct number of parameters were passed in'
        success = False

    assert success, message


def f2x(x):
    """function is only used for testing purposes"""
    return( 2*x )

def itest_setf1():
    """Test that setting the function to a new function updates the plane with the new transformation values"""
    #  create a plane
    tp = ComplexPlaneNP( 0, 10, 0, 10 )
    #  set the function to be f(x) = 2*x
    tp.set_f( f2x )

    # set up the expected plane
    xmin = 0
    xmax = 10
    xstep = 0.5
    xlen = 21
    ymin = 0
    ymax = 10
    ystep = 0.5
    ylen = 21
    eplane = [[2*(( j*xstep + xmin ) + ( i*ystep + ymin )*1j) for i in range(ylen)] for j in range(xlen)]

    #  this line is to force an error to prove the test can fail
    #eplane[1][1] = 5

    #  do the expected and actual planes match?
    success = tp.plane == eplane
    message = 'set_f() did not correctly transform the plane to double the coordinate values'
    assert success, message



def test_setf2():
    """Set the transformation function to be something other than a function(), which should fail,
    meaning the test was successful"""
    #  create a plane
    tp = ComplexPlaneNP( 1, 10, 1, 10 )

    try:
        #  set the function to be f(x) = 2*x
        tp.set_f( tp )
        message = 'Test Failed, succeeded in setting function to a non-function value'
        success = False
    except TypeError:
        """Test succeeds, exception generated"""
        success = True

    assert success, message

def itest_zoom1():
    """Test the zoom function with valid values.  Zoom should move/reset the 2D plane to a known configuration"""
    # set up the expected plane
    xmin = 0
    xmax = 10
    xstep = 0.5
    xlen = 21
    ymin = 0
    ymax = 10
    ystep = 0.5
    ylen = 21
    eplane = [[(( j*xstep + xmin ) + ( i*ystep + ymin )*1j) for i in range(ylen)] for j in range(xlen)]

    #  create a plane
    tp = ComplexPlaneNP( 100, 200, -100, 0 )
    tp.zoom(xmin, xmax, ymin, ymax)

    #  do the expected and actual planes match?
    success = tp.plane == eplane
    message = 'zoom() did not correctly transform the plane to the new coordinate values'
    assert success, message

def test_zoom2():
    """Test the zoom function with invalid values.  Zoom should generate an exception"""
    #  create a plane
    tp = ComplexPlaneNP( 100, 200, -100, 0 )
    try:
        tp.zoom( "one", 100, -1, 3)
        message = 'Test Failed, zoom did not catch use of an invalid parameter'
        success = False
    except TypeError:
        """Test succeeds, exception generated"""
        success = True

    assert success, message



def itest_refresh1():
    """Test the refresh function.  Create a plane, corrupt the data in the plane, refresh and verify the data is once again correct"""
    #  create a plane
    tp = ComplexPlaneNP( 100, 200, -100, 0 )
    #  create a duplicate plane
    ep = ComplexPlaneNP( 100, 200, -100, 0 )

    #  corrupt the original test plane
    tp.plane = [[(-1 +  -1j) for i in range(tp.ylen)] for j in range(tp.xlen)]

    # refresh the plane
    tp.refresh()

    #  this line is to force an error to prove the test can fail
    #ep.plane[1][1] = -1

    #  do the expected and actual planes match?
    success = tp.plane == ep.plane
    message = 'refresh() did not correctly retore the plane to the expected coordinate values'
    assert success, message

