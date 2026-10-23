"""Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
Simulador mínimo de vector de estado (numpy) para circuitos de pocos cúbits.
Referencia: Nielsen M.A., Chuang I.L. (2010/2012), Quantum Computation and Quantum Information, doi:10.1017/CBO9780511976667.
"""
import numpy as np

H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])


class Circuit:
    def __init__(self, n):
        self.n = n
        self.state = np.zeros(2**n, complex)
        self.state[0] = 1

    def _apply1(self, U, q):
        psi = self.state.reshape([2] * self.n)
        psi = np.moveaxis(np.tensordot(U, psi, axes=([1], [q])), 0, q)
        self.state = psi.reshape(-1)
        return self

    def h(self, q): return self._apply1(H, q)
    def x(self, q): return self._apply1(X, q)
    def z(self, q): return self._apply1(Z, q)

    def cx(self, c, t):
        psi = self.state.reshape([2] * self.n).copy()
        idx = [slice(None)] * self.n
        idx[c] = 1
        sub = psi[tuple(idx)]
        tt = t if t < c else t - 1
        psi[tuple(idx)] = np.flip(sub, axis=tt)
        self.state = psi.reshape(-1)
        return self

    def probabilities(self):
        return np.abs(self.state) ** 2

    def sample(self, shots=1000, seed=0):
        rng = np.random.default_rng(seed)
        k = rng.choice(2**self.n, size=shots, p=self.probabilities())
        return {format(i, f"0{self.n}b"): int((k == i).sum()) for i in np.unique(k)}
