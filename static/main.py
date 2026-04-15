"""
Photosynthesis NPQ model — Matuszynska et al. 2016
Ported from modelbase to pure numpy/scipy for Pyodide compatibility.

State variables: P, H, E, A, Pr, V

Old plots displayed
- Fluorescence (simple readout)
- NPQ, calculated from fluorescence at peaks
- Phi PSII, also calculated from fluorescences

So we only ever need to get the fluorescence from our components readout
"""

import math
from collections.abc import Iterable
from typing import Any, Literal

import numpy as np
import pandas as pd  # type: ignore
from scipy.integrate import solve_ivp  # type: ignore
from scipy.signal import find_peaks, peak_prominences  # type: ignore

# Order: P, H, E, A, Pr, V

# _y0_ref = {
#     "atp": 1.6999999999999997,
#     "pq_ox": 4.706348349506148,
#     "pc_ox": 3.9414515288091567,
#     "fd_ox": 3.7761613271207324,
#     "protons_lumen": 7.737821100836988,
#     "lhc": 0.5105293511676007,
#     "psbs_de": 0.5000000001374878,
#     "vx": 0.09090909090907397,
# }

_y0_ref = {
    "atp": 1.6999999999999997,
    "pq_ox": 4.706348349506148,
    "pc_ox": 3.9414515288091567,
    "fd_ox": 3.7761613271207324,
    "protons_lumen": 7.737821100836988,
    "lhc": 0.5105293511676007,
    "psbs_de": 0.5000000001374878,
    "vx": 0.09090909090907397,
}

Y0 = [
    _y0_ref[i]
    for i in (
        "atp",
        "pq_ox",
        "pc_ox",
        "fd_ox",
        "protons_lumen",
        "lhc",
        "psbs_de",
        "vx",
    )
]


def components(
    time: float, variables: Iterable[float], args: tuple[float, ...]
) -> float:
    atp, pq_ox, pc_ox, fd_ox, protons_lumen, lhc, psbs_de, vx = variables
    PPFD, kDeepoxV, kEpoxZ = args

    pH = 7.9
    F = 96.485
    R = 0.0083
    T = 298.0
    Carotenoids_tot = 1.0
    PSBS_tot = 1.0
    gamma0 = 0.1
    gamma1 = 0.25
    gamma2 = 0.6
    gamma3 = 0.15
    kZSat = 0.12
    E_0_QA = -0.14
    E_0_PQ = 0.354
    PQ_tot = 17.5
    staticAntII = 0.1
    staticAntI = 0.37
    PSII_total = 2.5
    kH0 = 500000000.0
    kPQred = 250.0
    k2 = 5000000000.0
    kH = 5000000000.0
    kF = 625000000.0
    RT = R * T
    dG_pH = 2.30258509299405 * R * T
    zx = Carotenoids_tot - vx
    psbs_pr = PSBS_tot - psbs_de
    Q = (
        gamma0 * psbs_de * vx
        + gamma1 * psbs_pr * vx
        + gamma2 * psbs_pr * zx / (kZSat + zx)
        + gamma3 * psbs_de * zx / (kZSat + zx)
    )
    keq_pq_red = math.exp((2.0 * E_0_PQ * F - 2.0 * E_0_QA * F - 2.0 * dG_pH * pH) / RT)
    pq_red = PQ_tot - pq_ox
    PSII_cross_section = lhc * (-staticAntI - staticAntII + 1.0) + staticAntII
    B0 = (
        PSII_total
        * kPQred
        * keq_pq_red
        * pq_ox
        * (
            Q * k2 * kH
            + 2.0 * Q * kF * kH
            + 2.0 * Q * kH * kH0
            + Q**2.0 * kH**2.0
            + k2 * kF
            + k2 * kH0
            + 2.0 * kF * kH0
            + kF**2.0
            + kH0**2.0
        )
        / (
            PPFD * PSII_cross_section * Q * k2 * kH * keq_pq_red
            + PPFD * PSII_cross_section * Q * kH * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * Q * kH * kPQred * pq_red
            + PPFD * PSII_cross_section * k2 * kF * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kH0 * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kPQred * pq_red
            + PPFD * PSII_cross_section * kF * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * kF * kPQred * pq_red
            + PPFD * PSII_cross_section * kH0 * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * kH0 * kPQred * pq_red
            + PPFD**2.0 * PSII_cross_section**2.0 * k2 * keq_pq_red
            + Q * k2 * kH * kPQred * keq_pq_red * pq_ox
            + Q * k2 * kH * kPQred * pq_red
            + 2.0 * Q * kF * kH * kPQred * keq_pq_red * pq_ox
            + 2.0 * Q * kF * kH * kPQred * pq_red
            + 2.0 * Q * kH * kH0 * kPQred * keq_pq_red * pq_ox
            + 2.0 * Q * kH * kH0 * kPQred * pq_red
            + Q**2.0 * kH**2.0 * kPQred * keq_pq_red * pq_ox
            + Q**2.0 * kH**2.0 * kPQred * pq_red
            + k2 * kF * kPQred * keq_pq_red * pq_ox
            + k2 * kF * kPQred * pq_red
            + k2 * kH0 * kPQred * keq_pq_red * pq_ox
            + k2 * kH0 * kPQred * pq_red
            + 2.0 * kF * kH0 * kPQred * keq_pq_red * pq_ox
            + 2.0 * kF * kH0 * kPQred * pq_red
            + kF**2.0 * kPQred * keq_pq_red * pq_ox
            + kF**2.0 * kPQred * pq_red
            + kH0**2.0 * kPQred * keq_pq_red * pq_ox
            + kH0**2.0 * kPQred * pq_red
        )
    )
    B2 = (
        PSII_total
        * (
            PPFD * PSII_cross_section * Q * k2 * kH * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kF * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kH0 * keq_pq_red
            + Q * k2 * kH * kPQred * pq_red
            + 2.0 * Q * kF * kH * kPQred * pq_red
            + 2.0 * Q * kH * kH0 * kPQred * pq_red
            + Q**2.0 * kH**2.0 * kPQred * pq_red
            + k2 * kF * kPQred * pq_red
            + k2 * kH0 * kPQred * pq_red
            + 2.0 * kF * kH0 * kPQred * pq_red
            + kF**2.0 * kPQred * pq_red
            + kH0**2.0 * kPQred * pq_red
        )
        / (
            PPFD * PSII_cross_section * Q * k2 * kH * keq_pq_red
            + PPFD * PSII_cross_section * Q * kH * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * Q * kH * kPQred * pq_red
            + PPFD * PSII_cross_section * k2 * kF * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kH0 * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kPQred * pq_red
            + PPFD * PSII_cross_section * kF * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * kF * kPQred * pq_red
            + PPFD * PSII_cross_section * kH0 * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * kH0 * kPQred * pq_red
            + PPFD**2.0 * PSII_cross_section**2.0 * k2 * keq_pq_red
            + Q * k2 * kH * kPQred * keq_pq_red * pq_ox
            + Q * k2 * kH * kPQred * pq_red
            + 2.0 * Q * kF * kH * kPQred * keq_pq_red * pq_ox
            + 2.0 * Q * kF * kH * kPQred * pq_red
            + 2.0 * Q * kH * kH0 * kPQred * keq_pq_red * pq_ox
            + 2.0 * Q * kH * kH0 * kPQred * pq_red
            + Q**2.0 * kH**2.0 * kPQred * keq_pq_red * pq_ox
            + Q**2.0 * kH**2.0 * kPQred * pq_red
            + k2 * kF * kPQred * keq_pq_red * pq_ox
            + k2 * kF * kPQred * pq_red
            + k2 * kH0 * kPQred * keq_pq_red * pq_ox
            + k2 * kH0 * kPQred * pq_red
            + 2.0 * kF * kH0 * kPQred * keq_pq_red * pq_ox
            + 2.0 * kF * kH0 * kPQred * pq_red
            + kF**2.0 * kPQred * keq_pq_red * pq_ox
            + kF**2.0 * kPQred * pq_red
            + kH0**2.0 * kPQred * keq_pq_red * pq_ox
            + kH0**2.0 * kPQred * pq_red
        )
    )
    Fluo = B0 * PSII_cross_section * kF / (
        Q * kH + k2 + kF
    ) + B2 * PSII_cross_section * kF / (Q * kH + kF)
    return Fluo


def model(
    time: float,
    variables: Iterable[float],
    PPFD: float,
    kf_violaxanthin_deepoxidase: float,
    kf_zeaxanthin_epoxidase: float,
) -> Iterable[float]:
    atp, pq_ox, pc_ox, fd_ox, protons_lumen, lhc, psbs_de, vx = variables

    pH = 7.9
    nadph = 0.6
    O2_lumen = 8.0
    bH = 100.0
    F = 96.485
    E_0_PC = 0.38
    E_0_P700 = 0.48
    E_0_FA = -0.55
    E_0_Fd = -0.43
    E_0_NADP = -0.113
    NADP_ = 0.8
    R = 0.0083
    T = 298.0
    A_P = 2.55
    Carotenoids_tot = 1.0
    Fd_ = 5.0
    PC_tot = 4.0
    PSBS_tot = 1.0
    LHC_tot = 1.0
    gamma0 = 0.1
    gamma1 = 0.25
    gamma2 = 0.6
    gamma3 = 0.15
    kZSat = 0.12
    E_0_QA = -0.14
    E_0_PQ = 0.354
    PQ_tot = 17.5
    staticAntII = 0.1
    staticAntI = 0.37
    kf_atp_synthase = 20.0
    HPR = 4.666666666666667
    Pi_mol = 0.01
    DeltaG0_ATP = 30.6
    kcat_b6f = 2.5
    kh_lhc_protonation = 3.0
    kf_lhc_protonation = 0.0096
    ksat_lhc_protonation = 5.8
    kf_lhc_deprotonation = 0.0096
    kf_cyclic_electron_flow = 1.0
    kh_violaxanthin_deepoxidase = 5.0
    ksat_violaxanthin_deepoxidase = 5.8
    E0_fnr = 3.0
    kcat_fnr = 500.0
    km_fnr_fd_red = 1.56
    km_fnr_nadp = 0.22
    kf_ndh = 0.002
    PSII_total = 2.5
    PSI_total = 2.5
    kH0 = 500000000.0
    kPQred = 250.0
    kPCox = 2500.0
    kFdred = 250000.0
    k2 = 5000000000.0
    kH = 5000000000.0
    kF = 625000000.0
    kf_proton_leak = 10.0
    kPTOX = 0.01
    kStt7 = 0.0035
    km_lhc_state_transition_12 = 0.2
    n_ST = 2.0
    kPph1 = 0.0013
    kf_ex_atp = 10.0
    nadp = NADP_ - nadph
    RT = R * T
    adp = A_P - atp
    dG_pH = 2.30258509299405 * R * T
    pH_lumen = -math.log(0.00025 * protons_lumen) / math.log(10)
    zx = Carotenoids_tot - vx
    fd_red = Fd_ - fd_ox
    pc_red = PC_tot - pc_ox
    psbs_pr = PSBS_tot - psbs_de
    lhc_prot = LHC_tot - lhc
    Q = (
        gamma0 * psbs_de * vx
        + gamma1 * psbs_pr * vx
        + gamma2 * psbs_pr * zx / (kZSat + zx)
        + gamma3 * psbs_de * zx / (kZSat + zx)
    )
    keq_pq_red = math.exp((2.0 * E_0_PQ * F - 2.0 * E_0_QA * F - 2.0 * dG_pH * pH) / RT)
    pq_red = PQ_tot - pq_ox
    PSII_cross_section = lhc * (-staticAntI - staticAntII + 1.0) + staticAntII
    keq_atp_synthase = Pi_mol * math.exp(
        (-DeltaG0_ATP + HPR * dG_pH * (pH - pH_lumen)) / RT
    )
    keq_b6f = math.exp(
        (
            2.0 * E_0_PC * F
            - 2.0 * E_0_PQ * F
            + 2.0 * dG_pH * pH_lumen
            - 2.0 * dG_pH * (pH - pH_lumen)
        )
        / RT
    )
    keq_fnr = math.exp((-2.0 * E_0_Fd * F + 2.0 * E_0_NADP * F - dG_pH * pH) / RT)
    vmax_fnr = E0_fnr * kcat_fnr
    keq_PCP700 = math.exp((E_0_P700 * F - E_0_PC * F) / RT)
    keq_ferredoxin_reductase = math.exp((-E_0_FA * F + E_0_Fd * F) / RT)
    B1 = (
        PPFD
        * PSII_cross_section
        * PSII_total
        * kPQred
        * keq_pq_red
        * pq_ox
        * (Q * kH + kF + kH0)
        / (
            PPFD * PSII_cross_section * Q * k2 * kH * keq_pq_red
            + PPFD * PSII_cross_section * Q * kH * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * Q * kH * kPQred * pq_red
            + PPFD * PSII_cross_section * k2 * kF * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kH0 * keq_pq_red
            + PPFD * PSII_cross_section * k2 * kPQred * pq_red
            + PPFD * PSII_cross_section * kF * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * kF * kPQred * pq_red
            + PPFD * PSII_cross_section * kH0 * kPQred * keq_pq_red * pq_ox
            + PPFD * PSII_cross_section * kH0 * kPQred * pq_red
            + PPFD**2.0 * PSII_cross_section**2.0 * k2 * keq_pq_red
            + Q * k2 * kH * kPQred * keq_pq_red * pq_ox
            + Q * k2 * kH * kPQred * pq_red
            + 2.0 * Q * kF * kH * kPQred * keq_pq_red * pq_ox
            + 2.0 * Q * kF * kH * kPQred * pq_red
            + 2.0 * Q * kH * kH0 * kPQred * keq_pq_red * pq_ox
            + 2.0 * Q * kH * kH0 * kPQred * pq_red
            + Q**2.0 * kH**2.0 * kPQred * keq_pq_red * pq_ox
            + Q**2.0 * kH**2.0 * kPQred * pq_red
            + k2 * kF * kPQred * keq_pq_red * pq_ox
            + k2 * kF * kPQred * pq_red
            + k2 * kH0 * kPQred * keq_pq_red * pq_ox
            + k2 * kH0 * kPQred * pq_red
            + 2.0 * kF * kH0 * kPQred * keq_pq_red * pq_ox
            + 2.0 * kF * kH0 * kPQred * pq_red
            + kF**2.0 * kPQred * keq_pq_red * pq_ox
            + kF**2.0 * kPQred * pq_red
            + kH0**2.0 * kPQred * keq_pq_red * pq_ox
            + kH0**2.0 * kPQred * pq_red
        )
    )
    A1 = PSI_total / (
        PPFD * (1.0 - PSII_cross_section) / (fd_ox * kFdred)
        + (1.0 + fd_red / (fd_ox * keq_ferredoxin_reductase))
        * (
            PPFD * (1.0 - PSII_cross_section) / (kPCox * pc_red)
            + pc_ox / (keq_PCP700 * pc_red)
        )
        + 1.0
    )
    atp_synthase = kf_atp_synthase * (adp - atp / keq_atp_synthase)
    b6f = max(
        -kcat_b6f, kcat_b6f * (pc_ox**2.0 * pq_red - pc_red**2.0 * pq_ox / keq_b6f)
    )
    lhc_protonation = (
        kf_lhc_protonation
        * protons_lumen**kh_lhc_protonation
        * psbs_de
        / (
            protons_lumen**kh_lhc_protonation
            + (4000.0 * 10.0 ** (-ksat_lhc_protonation)) ** kh_lhc_protonation
        )
    )
    lhc_deprotonation = kf_lhc_deprotonation * psbs_pr
    cyclic_electron_flow = fd_red**2.0 * kf_cyclic_electron_flow * pq_ox
    violaxanthin_deepoxidase = (
        kf_violaxanthin_deepoxidase
        * protons_lumen**kh_violaxanthin_deepoxidase
        * vx
        / (
            protons_lumen**kh_violaxanthin_deepoxidase
            + (4000.0 * 10.0 ** (-ksat_violaxanthin_deepoxidase))
            ** kh_violaxanthin_deepoxidase
        )
    )
    zeaxanthin_epoxidase = kf_zeaxanthin_epoxidase * zx
    fnr = (
        vmax_fnr
        * (
            nadp * (fd_red / km_fnr_fd_red) ** 2.0 / km_fnr_nadp
            - nadph * (fd_ox / km_fnr_fd_red) ** 2.0 / (keq_fnr * km_fnr_nadp)
        )
        / (
            (1.0 + nadp / km_fnr_nadp)
            * (fd_red / km_fnr_fd_red + (fd_red / km_fnr_fd_red) ** 2.0 + 1.0)
            + (1.0 + nadph / km_fnr_nadp)
            * (fd_ox / km_fnr_fd_red + (fd_ox / km_fnr_fd_red) ** 2.0 + 1.0)
            - 1.0
        )
    )
    ndh = kf_ndh * pq_ox
    PSII = 0.5 * B1 * k2
    PSI = A1 * PPFD * (1.0 - PSII_cross_section)
    proton_leak = kf_proton_leak * (protons_lumen - 4000.0 * 10.0 ** (-pH))
    PTOX = O2_lumen * kPTOX * pq_red
    lhc_state_transition_12 = (
        1.0
        * kStt7
        * lhc
        / ((pq_ox / (PQ_tot * km_lhc_state_transition_12)) ** n_ST + 1.0)
    )
    lhc_state_transition_21 = kPph1 * lhc_prot
    ex_atp = atp * kf_ex_atp
    datpdt = atp_synthase - ex_atp
    dprotons_lumendt = (
        -HPR * atp_synthase / bH + 2.0 * PSII / bH + 4.0 * b6f / bH - proton_leak / bH
    )
    dpc_oxdt = PSI - 2 * b6f
    dpq_oxdt = -PSII + PTOX + b6f - cyclic_electron_flow - ndh
    dpsbs_dedt = lhc_deprotonation - lhc_protonation
    dfd_oxdt = -PSI + 2 * cyclic_electron_flow + 2 * fnr
    dvxdt = -violaxanthin_deepoxidase + zeaxanthin_epoxidase
    dlhcdt = -lhc_state_transition_12 + lhc_state_transition_21
    return (
        datpdt,
        dpq_oxdt,
        dpc_oxdt,
        dfd_oxdt,
        dprotons_lumendt,
        dlhcdt,
        dpsbs_dedt,
        dvxdt,
    )


def ts(t_end: float, n: int) -> dict[str, tuple[int, float] | np.ndarray]:
    return {"t_span": (0, t_end), "t_eval": np.linspace(0, t_end, n)}


def integrate_ppfd_protocol(
    protocol: list[dict[str, float]],  # (t_end, ppfd)
    pars: Iterable[float],
    n: int = 100,
    method: Literal["RK45", "LSODA", "BDF"] = "LSODA",
    # Return structure given by pyWorker.ts
) -> tuple[dict[str, Any], str | None]:
    traces: list[pd.DataFrame] = []

    kDeepoxV, kEpoxZ = pars

    t_start = 0
    y0 = Y0
    for step in protocol:
        ppfd = step["PFD"]
        t_end = step["t_end"]
        print(t_end, ppfd, n)
        res = solve_ivp(
            model,
            y0=y0,
            args=(ppfd, kDeepoxV, kEpoxZ),
            method=method,
            t_span=(t_start, t_end),
            t_eval=np.linspace(t_start, t_end, n),
            rtol=1e-8,  # manually set
            atol=1e-8,  # manually set
        )
        t_start = t_end

        t_sim = res.t
        y_sim = res.y.T
        y0 = y_sim[-1]

        if not res.success:
            return {}, "err"

        # Let's check if broadcasting works in web assembly
        fluo = np.atleast_2d(components(t_sim, y_sim.T, (ppfd, kDeepoxV, kEpoxZ))).T
        _res = pd.DataFrame(
            np.concat((y_sim, fluo), axis=1),
            index=t_sim,
            columns=[
                "atp",
                "pqOx",
                "pcOx",
                "fdOx",
                "hLumen",
                "lhc",
                "psbsDe",
                "vX",
                "fluo",
            ],
        )
        if len(traces) > 0:
            _res = _res.iloc[1:]
        traces.append(_res)
    print("n_traces", len(traces))

    results = pd.concat(traces)
    print("Results", results.shape)
    time = results.index.to_numpy()

    abs_fluo: pd.Series = results["fluo"]
    rel_fluo: pd.Series = results["fluo"] / results["fluo"].max()
    peaks = find_peaks(rel_fluo, height=0)[0]
    print("peals", time[peaks])
    npq: pd.Series = (abs_fluo.iloc[peaks[0]] - abs_fluo.iloc[peaks]) / abs_fluo.iloc[
        peaks
    ]

    prominences_left = peak_prominences((rel_fluo), peaks)[1]
    Fo = np.array([rel_fluo.iloc[i] for i in prominences_left])
    phi_psii: pd.Series = (abs_fluo.iloc[peaks] - Fo) / abs_fluo.iloc[peaks]

    print("npq", npq.to_numpy())
    print("phiPSII", phi_psii.to_numpy())

    final = {
        "time": time,
        "fluo": rel_fluo.to_numpy(),
        "npqTime": time[peaks],
        "npq": npq.to_numpy(),
        "phiPsii": phi_psii.to_numpy(),
    }
    return final, None


class ModelFunctions: ...


model_functions = ModelFunctions()
model_functions.integrate = integrate_ppfd_protocol  # type: ignore
model_functions  # type: ignore # noqa: B018 — Pyodide captures the last expression as the module return value
