from .airfoil import Airfoil

import numpy as np
import numpy.typing as nptype

class AirfoilNACA4(Airfoil):

    def __init__(self, M: float, P: float, T: float, npt: int = 299) -> None:

        self.M = M
        self.P = P
        self.T = T

        x, y = _generateNACA4(M/100, P/10, T/100, npt)

        super().__init__(x, y)

    def __repr__(self):

        return "AirfoilNACA4({},{}},{})".format(self.M, self.P, self.T)




def _generateNACA4(M, P, T, npt, cosine=True):

    # Remove division by zero
    if P == 0.0:
            P = 0.1

    if cosine == True:
        lsp_max = np.pi
    else:
        lsp_max = 1.0

    # This ensures LE point at x = 0.0 on upper surface
    if npt % 2 == 1: # if npt is odd
        beta_u = np.linspace(0.0, lsp_max, int(np.ceil(npt/2)))
        beta_l = np.linspace(0.0, lsp_max, int(np.floor(npt/2) + 1))[1:]
    else:
        beta_u = np.linspace(0.0, lsp_max, npt/2 + 1)
        beta_l = np.linspace(0.0, lsp_max, npt/2)[1:]

    if cosine == True:
        xc_l = (1 - np.cos(beta_l))/2
        xc_u = (1 - np.cos(beta_u))/2
    else:
        xc_l = beta_l
        xc_u = beta_u


    def camber(xc):

        yc = np.where(xc < P, 
                      M/P**2 * (2*P*xc -xc**2), 
                      M/(1-P)**2 * (1 - 2*P + 2*P*xc - xc**2))

        dyc = np.where(xc < P, 
                       2*M/P**2 * (P - xc), 
                       2*M/(1-P)**2 * (P - xc))
        
        th = np.arctan(dyc)

        return yc, th

    def thickness(xc):

        a0 = 0.2969
        a1 = -0.126
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1036

        return  T/0.2 * (a0*xc**0.5 + a1*xc + a2*xc**2 + a3*xc**3 + a4*xc**4)

    # Upper surface
    yc_u, th_u = camber(xc_u)
    yt_u = thickness(xc_u)

    xu = xc_u - yt_u*np.sin( th_u )
    yu = yc_u + yt_u*np.cos( th_u )

    # Lower surface
    yc_l, th_l = camber(xc_l)
    yt_l = thickness(xc_l)

    xl = xc_l + yt_l*np.sin( th_l )
    yl = yc_l - yt_l*np.cos( th_l )


    xu = np.flip(xu)
    yu = np.flip(yu)

    x = np.concatenate((xu, xl))
    y = np.concatenate((yu, yl))

    return x, y