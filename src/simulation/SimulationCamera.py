import numpy as np
from .CoherentLightSource import *
from .Reference import Reference, reference_parameters, A, α
from ..shared import ISU_value
from copy import deepcopy


c = 299792458  # Speed of light [m/s]

μ0 = 4 * np.pi * 1e-7  # Vacuum permeability [H/m]

ε0 = 1 / (μ0 * c**2)  # Vacuum permitivity [F/m]


def interference_term(source, spectrometer, sample, reference):
    s, r = sample, reference
    λ, k = spectrometer.λ(), spectrometer.k()
    return lambda t: 2 * A(s, source)(λ) * A(r, source)(λ) * np.cos(k * (α(s, t) - α(r, t)))


def irradiance(source, spectrometer, references, t):
    I = np.zeros_like(spectrometer.k())
    for r in references:
        I += ε0 * c * (A(r, source)(spectrometer.λ()))**2
    for i, s in enumerate(references[:-1]):
        for r in references[i:]:
            I += ε0 * c * (interference_term(source, spectrometer, s, r)(t))
    return I


class SimulationCamera():

    def __init__(self):

        self.source = CoherentLightSource()

        self.reference = Reference(deepcopy(reference_parameters))

        self.references = []

        self.data = None

    def I(self, spectrometer, t):
        return irradiance(self.source, spectrometer, self.references, t)

    def add_reference(self):
        self.references.append(deepcopy(self.reference.parameters))

    def acquire(self, acq_interface, cam_interface, spectrometer):
        T = acq_interface.T()
        dt = cam_interface.dt()
        nframes = int(T / dt)
        n = T / nframes
        N = spectrometer.N()

        def irr(t):
            return self.I(spectrometer, t)

        # self.data = np.array([irr(np.linspace(i*n, (i+1)*n-1, N))
        #                     for i in range(nframes)])
        self.data = np.array([irr(i*n*np.ones(N))
                              for i in range(nframes)])
        np.save(f"{acq_interface.acq_name}.npy", self.data)
        return
