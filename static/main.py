"""
Photosynthesis NPQ model — Matuszynska et al. 2016
Ported from modelbase to pure numpy/scipy for Pyodide compatibility.

State variables: P, H, E, A, Pr, V
"""

import numpy as np
from scipy.integrate import solve_ivp  # type: ignore[import-untyped]

# ---------------------------------------------------------------------------
# Default parameters (from model.py get_model())
# ---------------------------------------------------------------------------
DEFAULT_PARS = {
    # Pool sizes
    "PSIItot": 2.5,
    "PQtot": 20.0,
    "APtot": 50.0,
    "PsbStot": 1.0,
    "Xtot": 1.0,
    "O2ex": 8.0,
    "Pi": 0.01,
    # Rate constants
    "kCytb6f": 0.104,
    "kActATPase": 0.01,
    "kDeactATPase": 0.002,
    "kATPsynthase": 20.0,
    "kATPconsumption": 10.0,
    "kPQred": 250.0,
    "kH": 5e9,
    "kF": 6.25e8,
    "kP": 5e9,
    "kPTOX": 0.01,
    "pHstroma": 7.8,
    "kleak": 1000.0,
    "bH": 100.0,
    "HPR": 14.0 / 3.0,
    # Xanthophyll cycle
    "kDeepoxV": 0.0024,
    "kEpoxZ": 0.00024,
    "KphSatZ": 5.8,
    "nHX": 5.0,
    "Kzsat": 0.12,
    # PsbS protonation
    "nHL": 3.0,
    "kDeprot": 0.0096,
    "kProt": 0.0096,
    "KphSatLHC": 5.8,
    # Quencher contributions
    "gamma0": 0.1,
    "gamma1": 0.25,
    "gamma2": 0.6,
    "gamma3": 0.15,
    # Physical constants
    "F": 96.485,
    "R": 8.3e-3,
    "T": 298.0,
    # Standard potentials
    "E0QAQAm": -0.140,
    "E0PQPQH2": 0.354,
    "E0PCPCm": 0.380,
    "DG0ATP": 30.6,
    # Light (PFD) — overridden per protocol step
    "PFD": 100.0,
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _pH(H):
    return -np.log10(H * 2.5e-4)


def _pHinv(pH):
    return 4e3 * 10 ** (-pH)


def _Keqcytb6f(H, F, E0PQPQH2, RT, E0PCPCm, pHstroma):
    DG1 = -2 * F * E0PQPQH2 + 2 * RT * np.log(10) * _pH(H)
    DG2 = -F * E0PCPCm
    DG3 = RT * np.log(10) * (pHstroma - _pH(H))
    DG = -DG1 + 2 * DG2 + 2 * DG3
    return np.exp(-DG / RT)


def _KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi):
    DG = DG0ATP - np.log(10) * (pHstroma - _pH(H)) * (14.0 / 3.0) * RT
    return Pi * np.exp(-DG / RT)


def _KeqQAPQ(F, E0QAQAm, E0PQPQH2, pHstroma, RT):
    DG1 = -F * E0QAQAm
    DG2 = -2 * F * E0PQPQH2 + 2 * pHstroma * np.log(10) * RT
    DG0 = -2 * DG1 + DG2
    return np.exp(-DG0 / RT)


def _quencher(Pr, V, Xtot, PsbStot, Kzsat, gamma0, gamma1, gamma2, gamma3):
    Z = Xtot - V
    P_prot = PsbStot - Pr
    Zs = Z / (Z + Kzsat)
    Q = (
        gamma0 * (1 - Zs) * Pr
        + gamma1 * (1 - Zs) * P_prot
        + gamma2 * Zs * P_prot
        + gamma3 * Zs * Pr
    )
    return Q


def _ps2states(P, Q, light, PQtot, kPQred, KeqQAPQ, kH, kF, kP, PSIItot):
    """Solve the quasi-steady-state for PSII states B0, B1, B2, B3."""
    Pox = PQtot - P
    b0 = light + kPQred * P / KeqQAPQ
    b1 = kH * Q + kF
    b2 = kH * Q + kF + kP

    A = np.array(
        [
            [-b0, b1, kPQred * Pox, 0.0],
            [light, -b2, 0.0, 0.0],
            [0.0, 0.0, light, -b1],
            [1.0, 1.0, 1.0, 1.0],
        ]
    )
    b_vec = np.array([0.0, 0.0, 0.0, PSIItot])
    try:
        B0, B1, B2, B3 = np.linalg.solve(A, b_vec)
    except np.linalg.LinAlgError:
        B0 = B1 = B2 = B3 = 0.0
    return B0, B1, B2, B3


def _fluorescence(B0, B2, Q, kH, kF, kP):
    return kF / (kH * Q + kF + kP) * B0 + kF / (kH * Q + kF) * B2


# ---------------------------------------------------------------------------
# ODE right-hand side
# ---------------------------------------------------------------------------


def _npq_ode(_t, y, pars, PFD):
    P, H, E, A, Pr, V = y

    # Unpack parameters
    PSIItot = pars["PSIItot"]
    PQtot = pars["PQtot"]
    APtot = pars["APtot"]
    PsbStot = pars["PsbStot"]
    Xtot = pars["Xtot"]
    O2ex = pars["O2ex"]
    Pi = pars["Pi"]
    kCytb6f = pars["kCytb6f"]
    kActATPase = pars["kActATPase"]
    kDeactATPase = pars["kDeactATPase"]
    kATPsynthase = pars["kATPsynthase"]
    kATPconsumption = pars["kATPconsumption"]
    kPQred = pars["kPQred"]
    kH = pars["kH"]
    kF = pars["kF"]
    kP = pars["kP"]
    kPTOX = pars["kPTOX"]
    pHstroma = pars["pHstroma"]
    kleak = pars["kleak"]
    bH = pars["bH"]
    kDeepoxV = pars["kDeepoxV"]
    kEpoxZ = pars["kEpoxZ"]
    KphSatZ = pars["KphSatZ"]
    nHX = pars["nHX"]
    Kzsat = pars["Kzsat"]
    nHL = pars["nHL"]
    kDeprot = pars["kDeprot"]
    kProt = pars["kProt"]
    KphSatLHC = pars["KphSatLHC"]
    gamma0 = pars["gamma0"]
    gamma1 = pars["gamma1"]
    gamma2 = pars["gamma2"]
    gamma3 = pars["gamma3"]
    F_const = pars["F"]
    RT = pars["R"] * pars["T"]
    E0QAQAm = pars["E0QAQAm"]
    E0PQPQH2 = pars["E0PQPQH2"]
    E0PCPCm = pars["E0PCPCm"]
    DG0ATP = pars["DG0ATP"]

    # Clamp state variables to avoid domain errors
    P = max(P, 0.0)
    H = max(H, 1e-15)
    E = max(min(E, 1.0), 0.0)
    A = max(A, 0.0)
    Pr = max(min(Pr, PsbStot), 0.0)
    V = max(min(V, Xtot), 0.0)

    # Derived equilibrium constants
    KeqQAPQ = _KeqQAPQ(F_const, E0QAQAm, E0PQPQH2, pHstroma, RT)

    # Algebraic modules
    Q = _quencher(Pr, V, Xtot, PsbStot, Kzsat, gamma0, gamma1, gamma2, gamma3)
    _B0, B1, _B2, _B3 = _ps2states(
        P, Q, PFD, PQtot, kPQred, KeqQAPQ, kH, kF, kP, PSIItot
    )

    # Rates
    # vps2: reduction of PQ by PSII
    vps2 = kP * 0.5 * B1

    # vPQox: oxidation of PQ by cyt b6f + PTOX
    kPFD_cytb6f = kCytb6f * PFD
    kPTOX_eff = kPTOX * O2ex
    Keqcytb6f = _Keqcytb6f(H, F_const, E0PQPQH2, RT, E0PCPCm, pHstroma)
    a1 = kPFD_cytb6f * Keqcytb6f / (Keqcytb6f + 1)
    a2 = kPFD_cytb6f / (Keqcytb6f + 1)
    vPQox = (a1 + kPTOX_eff) * P - a2 * (PQtot - P)

    # vATPsynthase
    KeqATP = _KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi)
    vATPsynthase = E * kATPsynthase * (APtot - A - A / KeqATP)

    # vATPactivity
    switch = 1.0 if PFD > 0 else 0.0
    vATPactivity = kActATPase * switch * (1 - E) - kDeactATPase * (1 - switch) * E

    # vLeak
    vLeak = kleak * (H - _pHinv(pHstroma))

    # vATPcons
    vATPcons = kATPconsumption * A

    # vXcyc: xanthophyll cycle
    a_xcyc = H**nHX / (H**nHX + _pHinv(KphSatZ) ** nHX)
    vXcyc = kDeepoxV * a_xcyc * V - kEpoxZ * (Xtot - V)

    # vPsbSP: PsbS protonation
    a_psbs = H**nHL / (H**nHL + _pHinv(KphSatLHC) ** nHL)
    vPsbSP = kProt * a_psbs * Pr - kDeprot * (PsbStot - Pr)

    # Stoichiometries (from model.py add_reaction_from_args)
    dP_dt = vps2 - vPQox
    dH_dt = (
        (2.0 / bH) * vps2
        - (4.0 / bH) * vPQox
        - (14.0 / 3.0) / bH * vATPsynthase
        - (1.0 / bH) * vLeak
    )
    dE_dt = vATPactivity
    dA_dt = vATPsynthase - vATPcons
    dPr_dt = -vPsbSP
    dV_dt = -vXcyc

    return [dP_dt, dH_dt, dE_dt, dA_dt, dPr_dt, dV_dt]


# ---------------------------------------------------------------------------
# Public integrate function
# ---------------------------------------------------------------------------


class ModelFunctions:
    def integrate(self, protocol, y0_list, pars_override_dict):
        """
        Run piecewise integration over a PAM protocol.

        Parameters
        ----------
        protocol : list of dicts  [{"t_end": float, "PFD": float}, ...]
        y0_list  : list of 6 floats  [P, H, E, A, Pr, V]
        pars_override_dict : dict of parameter overrides

        Returns
        -------
        (time_list, values_list, err)
            time_list   : flat list of floats
            values_list : list of lists [n_points x 7] (P,H,E,A,Pr,V,Fluo)
            err         : None or error string
        """
        # Build parameter dict
        pars = dict(DEFAULT_PARS)
        if pars_override_dict:
            try:
                # Support both Pyodide JsProxy and plain dict
                items = (
                    pars_override_dict.items()
                    if hasattr(pars_override_dict, "items")
                    else pars_override_dict.to_py().items()
                )
                for k, v in items:
                    pars[k] = float(v)
            except Exception:
                pass

        # Convert protocol from Pyodide JsProxy to plain Python list of dicts
        try:
            proto_py = (
                protocol.to_py() if hasattr(protocol, "to_py") else list(protocol)
            )
        except Exception:
            proto_py = list(protocol)

        # Convert y0
        try:
            y0 = list(y0_list.to_py() if hasattr(y0_list, "to_py") else y0_list)
        except Exception:
            y0 = list(y0_list)

        # Compute KeqQAPQ once (constant for fixed physical params)
        RT = pars["R"] * pars["T"]

        all_time = []
        all_values = []
        err = None

        t_start = 0.0
        y_current = list(y0)

        for step in proto_py:
            # Support both plain dicts and Pyodide JsProxy objects
            if isinstance(step, dict):
                t_end = float(step["t_end"])
                PFD = float(step["PFD"])
            else:
                t_end = float(step.t_end)  # type: ignore[union-attr]
                PFD = float(step.PFD)  # type: ignore[union-attr]

            if t_end <= t_start:
                continue

            try:
                sol = solve_ivp(
                    fun=lambda t, y: _npq_ode(t, y, pars, PFD),
                    t_span=(t_start, t_end),
                    y0=y_current,
                    method="LSODA",
                    dense_output=False,
                    max_step=0.1,
                    rtol=1e-6,
                    atol=1e-9,
                )
                if not sol.success:
                    err = f"Integration failed at step t={t_start}..{t_end}: {sol.message}"
                    # Still use partial results if available
                    if sol.t.size == 0:
                        t_start = t_end
                        continue

                t_arr = sol.t
                y_arr = sol.y  # shape (6, n_points)

                # Compute Fluo at each time point
                KeqQAPQ = _KeqQAPQ(
                    pars["F"], pars["E0QAQAm"], pars["E0PQPQH2"], pars["pHstroma"], RT
                )
                fluo_arr = []
                for i in range(y_arr.shape[1]):
                    P_i, H_i, _E_i, _A_i, Pr_i, V_i = y_arr[:, i]
                    P_i = max(P_i, 0.0)
                    H_i = max(H_i, 1e-15)
                    Pr_i = max(min(Pr_i, pars["PsbStot"]), 0.0)
                    V_i = max(min(V_i, pars["Xtot"]), 0.0)
                    Q_i = _quencher(
                        Pr_i,
                        V_i,
                        pars["Xtot"],
                        pars["PsbStot"],
                        pars["Kzsat"],
                        pars["gamma0"],
                        pars["gamma1"],
                        pars["gamma2"],
                        pars["gamma3"],
                    )
                    B0_i, _B1_i, B2_i, _B3_i = _ps2states(
                        P_i,
                        Q_i,
                        PFD,
                        pars["PQtot"],
                        pars["kPQred"],
                        KeqQAPQ,
                        pars["kH"],
                        pars["kF"],
                        pars["kP"],
                        pars["PSIItot"],
                    )
                    fluo_arr.append(
                        _fluorescence(
                            B0_i, B2_i, Q_i, pars["kH"], pars["kF"], pars["kP"]
                        )
                    )

                # Combine: [P, H, E, A, Pr, V, Fluo]
                for i in range(y_arr.shape[1]):
                    row = list(y_arr[:, i]) + [fluo_arr[i]]
                    all_values.append(row)

                all_time.extend(t_arr.tolist())
                y_current = list(y_arr[:, -1])
                t_start = float(t_arr[-1])

            except Exception as e:
                err = str(e)
                break

        return (all_time, all_values, err)


model_functions = ModelFunctions()
model_functions  # type: ignore # noqa: B018 — Pyodide captures the last expression as the module return value
