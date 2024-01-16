import numpy as np
import numpy.typing as nptype
from typing import Union

class Airfoil:

    def __init__(self, x: nptype.ArrayLike, y: nptype.ArrayLike=None) -> None:

        if y is not None:
            self._x = x
            self._y = y
        else:
            if len(x.shape) == 2 and x.shape[0] == 2:
                self._x = x[0]
                self.y = x[1]
            else:
                if len(x.shape) != 2:
                    raise ValueError("single input to '{}' must have 2 dimensions.")
                elif x.shape[0] != 2:
                    raise ValueError("single input to '{}' has leading axis of\
                                      length {} instead of 2.".format(x.shape[0]))
        
        self._Npt = len(self._x)
        
        self._LE = np.argmin(x)

        self.transform = Transform(self)


    def split(self, idx:int=None):

        if idx is None:
            idx = self._LE

        x_upper = self._x[:idx]
        y_upper = self._y[:idx]
        x_lower = self._x[idx:]
        y_lower = self._y[idx:]

        return  np.vstack((x_lower, y_lower)), np.vstack((x_upper, y_upper))

    def _interpy(self, other: "Airfoil"):

        # Interpolate y values so x values align (using self as master)
        
        # Split into LE and TE
        L_self, U_self = self.split()
        L_other, U_other = other.split()

        # Flip direction of lower surface
        L_y_other = np.interp(L_self[0, :], L_other[0, :], L_other[1, :])
        U_y_other = np.interp(U_self[0, ::-1], U_other[0, ::-1], U_other[1, ::-1])

        # Recombine slave airfoil y coord

        y_other = np.concatenate(( U_y_other[::-1], L_y_other))

        return y_other

    
    def __len__(self):
        return self._Npt
    
    def __getitem__(self, indicies) -> nptype.ArrayLike:
        xy = np.column_stack((self._x, self._y))
        return xy[indicies]
    
    def __setitem__(self, indicies, value: nptype.ArrayLike) -> None:    
        raise NotImplementedError    
    
    
    def __add__(self, other: "Airfoil") -> "Airfoil":

        # Add the y coordinates of two airfoils

        # Interpolate y coordinates to master (self) x coordinates
        y_other = self._interpy(other)

        # Add y coords
        y_new = self._y + y_other

        return Airfoil(self._x, y_new)
    
    def __sub__(self, other: "Airfoil") -> "Airfoil":

        # Subtract the y coordinates of two airfoils

        # Interpolate y coordinates to master (self) x coordinates
        y_other = self._interpy(other)

        # Add y coords
        y_new = self._y - y_other

        return Airfoil(self._x, y_new)
    
    def __mul__(self, other: Union[int, float, "Airfoil"]) -> "Airfoil":

        # Multiply the y coordinates of an airfoil, either by a numerical
        # value, numpy array or another aerofoil's y coordinates elementwise.

        if isinstance(other, int) or isinstance(other, float):

            y_new = self._y * other

        elif isinstance(other, Airfoil):

            raise NotImplementedError

        else:

            raise TypeError("unsupported operand type(s) for *: '{}' and {}".format(type(self), type(other)))

        return Airfoil(self._x, y_new)
    
    def __truediv__(self, other: Union[int, float, "Airfoil"] ) -> "Airfoil":

        # Divide the y coordinates of an airfoil, either by a numerical
        # value, numpy array or another aerofoil's y coordinates elementwise.

        if isinstance(other, int) or isinstance(other, float):

            y_new = self._y / other

        elif isinstance(other, Airfoil):

            raise NotImplementedError

        else:

            raise TypeError("unsupported operand type(s) for /: '{}' and {}".format(type(self), type(other)))

        return Airfoil(self._x, y_new)

    # spline tools for refinement
        

# Transform subclass for airfoil class. Methods should return a new airfoil.

class Transform():

    def __init__(self, airfoil: Airfoil) -> None:
        
        self.airfoil = airfoil

    def translate(self) -> Airfoil:
        raise NotImplementedError
    
    def scale(self) -> Airfoil:
        raise NotImplementedError
    
    def rotate(self) -> Airfoil:
        raise NotImplementedError