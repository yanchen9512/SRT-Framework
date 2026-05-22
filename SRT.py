#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SRN (Surface Radiative and Non-radiative Contribution) Framework

This framework establishes a linear relationship between total radiative contribution (R)
and total non-radiative contribution (N): N = a·R + b

The slope 'a' represents the sensitivity of non-radiative response to radiative forcing
(negative = partial offset, indicating increased warming is partially compensated by
enhanced turbulent/ground heat fluxes). The intercept 'b' is an empirical parameter
from linear regression extrapolation, retained for mathematical consistency.

Core applications:
1. Establish SRN relationship from CMIP6 multi-model ensemble
2. Decompose surface warming into radiative (R) and non-radiative (N) contributions
3. Constrain SAF using HEC (Hierarchical Emergent Constraint)
4. Propagate constraint to total warming via SRN relationship (R_atm unchanged)
5. Validate using historical period observations

Key equations:
- R = ΔT_SAF + ΔT_CRF + ΔT_SW + ΔT_LW  (total radiative contribution, K)
- N = -ΔT_(H+LE+Q)                      (total non-radiative contribution, K)
- N = a·R + b                            (SRN relationship)
- ΔT_S = R + N                           (surface energy balance)
- ΔT_S = (1+a)·R + b                     (alternative feedback-like form, for reference)

Author: Yan Chen
ORCID: https://orcid.org/0009-0009-9521-3386
License: MIT
"""

import numpy as np
import pandas as pd
from scipy import stats


def compute_srn_relationship(R_radiative, N_nonradiative):
    """
    Compute SRN relationship: N = a·R + b

    Parameters
    ----------
    R_radiative : array-like
        Total radiative contribution R (K, positive = warming)
    N_nonradiative : array-like
        Total non-radiative contribution N (K, positive = cooling in spring)

    Returns
    -------
    dict : Contains slope 'a', intercept 'b', correlation 'r', r-squared 'r2',
           p-value 'p', standard error 'std_err'
    
    Notes
    -----
    The slope a is negative for the Tibetan Plateau in spring (typically -0.48 to -0.47),
    indicating that increased radiative warming is partially offset by enhanced
    non-radiative cooling (turbulent + ground heat fluxes).
    """
    # Remove NaN values
    mask = ~(np.isnan(R_radiative) | np.isnan(N_nonradiative))
    R_clean = np.array(R_radiative)[mask]
    N_clean = np.array(N_nonradiative)[mask]
    
    if len(R_clean) < 2:
        raise ValueError("Need at least 2 valid data points for regression")
    
    a, b, r, p, std_err = stats.linregress(R_clean, N_clean)
    
    return {
        'a': a,
        'b': b,
        'r': r,
        'r2': r**2,
        'p': p,
        'std_err': std_err,
        'n': len(R_clean)
    }


def compute_radiative_contributions(SAF, CRF, SW, LW):
    """
    Compute total radiative contribution R = ΔT_SAF + ΔT_CRF + ΔT_SW + ΔT_LW

    Parameters
    ----------
    SAF : array-like
        Surface albedo feedback contribution (K)
    CRF : array-like
        Cloud radiative forcing contribution (K)
    SW : array-like
        Clear-sky shortwave contribution (K)
    LW : array-like
        Clear-sky longwave contribution (K)

    Returns
    -------
    array-like : Total radiative contribution R (K)
    """
    return SAF + CRF + SW + LW


def compute_nonradiative_contribution(FLUX, Q):
    """
    Compute total non-radiative contribution N = -ΔT_(H+LE+Q)

    Parameters
    ----------
    FLUX : array-like
        Turbulent heat flux contribution (H+LE, K, negative = cooling)
    Q : array-like
        Ground heat storage contribution (K, negative = cooling)

    Returns
    -------
    array-like : Total non-radiative contribution N (K)
                 Positive = cooling (spring over Tibetan Plateau)
    """
    return -(FLUX + Q)


def decompose_nonradiative_contribution(N_total, SAF, a, b):
    """
    Decompose total non-radiative contribution into SAF-driven and atmosphere-driven parts

    Parameters
    ----------
    N_total : array-like
        Total non-radiative contribution N (K)
    SAF : array-like
        SAF radiative contribution (ΔT_SAF, K)
    a, b : float
        SRN parameters from compute_srn_relationship

    Returns
    -------
    dict : Contains N_SAF (SAF-driven) and N_ATM (atmosphere-driven)
    
    Notes
    -----
    This decomposition assumes that each radiative component has the same efficacy
    in driving non-radiative changes (sharing the same slope a). The partition of
    b between N_SAF and N_ATM is a matter of convention; it does not affect the
    calculation of changes in ΔT_S induced by the SAF constraint.
    """
    # SAF-driven non-radiative contribution
    N_SAF = a * SAF + b
    
    # Atmosphere-driven non-radiative contribution (residual)
    N_ATM = N_total - N_SAF
    
    return {
        'N_SAF': N_SAF,
        'N_ATM': N_ATM
    }


def propagate_constraint(SAF_raw, SAF_con, N_ATM, a, b, R_atm=None):
    """
    Propagate SAF constraint to total warming using SRN relationship

    Parameters
    ----------
    SAF_raw : array-like
        Raw (unconstrained) SAF contribution (ΔT_SAF_raw, K)
    SAF_con : array-like
        Constrained SAF contribution from HEC (ΔT_SAF_con, K)
    N_ATM : array-like
        Atmosphere-driven non-radiative contribution (assumed unchanged)
    a, b : float
        SRN parameters from compute_srn_relationship
    R_atm : array-like, optional
        Atmospheric radiative contribution (ΔT_CRF + ΔT_SW + ΔT_LW, K)
        If provided, also returns constrained total warming.

    Returns
    -------
    dict : Contains constrained N_SAF, N_total, and optionally constrained total warming
    
    Propagation chain:
        ΔT_SAF_con → R_con = ΔT_SAF_con + R_atm → N_con = a·R_con + b → ΔT_S_con = R_con + N_con
    
    Notes
    -----
    The atmosphere-driven non-radiative contribution (N_ATM) and atmospheric
    radiative components (R_atm) are assumed unchanged because the constraint
    directly targets SAF and due to the linear independence of radiative
    components in the perturbed surface energy budget framework.
    """
    # Constrained SAF-driven non-radiative contribution
    N_SAF_con = a * SAF_con + b
    
    # Constrained total non-radiative contribution
    N_total_con = N_ATM + N_SAF_con
    
    result = {
        'N_SAF_con': N_SAF_con,
        'N_total_con': N_total_con
    }
    
    # If R_atm provided, compute constrained total warming
    if R_atm is not None:
        # Total radiative contribution with constrained SAF
        R_con = SAF_con + R_atm
        
        # Constrained total warming
        delta_T_S_con = R_con + N_total_con
        
        result['R_con'] = R_con
        result['delta_T_S_con'] = delta_T_S_con
    
    return result


def compute_total_warming(R_radiative, N_nonradiative):
    """
    Compute total surface warming from energy balance

    Parameters
    ----------
    R_radiative : array-like
        Total radiative contribution R (K)
    N_nonradiative : array-like
        Total non-radiative contribution N (K)

    Returns
    -------
    array-like : Total surface warming ΔT_S (K)
    
    Notes
    -----
    Based on surface energy balance: ΔT_S = R + N
    """
    return R_radiative + N_nonradiative


def feedback_parameter(a):
    """
    Convert SRN slope to effective feedback parameter (alternative form, for reference)

    Parameters
    ----------
    a : float
        SRN slope from compute_srn_relationship

    Returns
    -------
    float : Effective feedback parameter λ = 1 + a
    
    Notes
    -----
    This is derived from: ΔT_S = R + N = R + (a·R + b) = (1+a)·R + b
    The effective feedback parameter λ ≈ 0.5 for the Tibetan Plateau in spring,
    indicating that about half of the radiative warming is offset by enhanced
    non-radiative cooling.
    
    This form is not used in the main analysis but provided for conceptual reference
    and comparison with classical TOA feedback frameworks.
    """
    return 1 + a


def validate_srn_framework(N_total, R_radiative, a, b):
    """
    Validate that constrained system still satisfies SRN relationship

    Parameters
    ----------
    N_total : array-like
        Total non-radiative contribution N (K)
    R_radiative : array-like
        Total radiative contribution R (K)
    a, b : float
        SRN parameters from compute_srn_relationship

    Returns
    -------
    dict : Contains predicted N from SRN and residual statistics
    """
    N_pred = a * R_radiative + b
    residual = N_total - N_pred
    
    return {
        'N_pred': N_pred,
        'residual': residual,
        'residual_mean': np.mean(residual),
        'residual_std': np.std(residual),
        'residual_max_abs': np.max(np.abs(residual)),
        'r2_validation': 1 - np.var(residual) / np.var(N_total) if len(N_total) > 1 else np.nan
    }


def get_framework_parameters(scenario='ssp245'):
    """
    Return pre-computed SRN parameters for each scenario

    Parameters
    ----------
    scenario : str
        One of 'historical', 'ssp245', 'ssp585'

    Returns
    -------
    dict : Contains a, b, r2, and other scenario-specific parameters
    """
    parameters = {
        'historical': {
            'a': -0.54,
            'b': -0.15,
            'r2': 0.80,
            'R_atm': None,  # Not used in historical validation
            'SAF_raw': None,
            'SAF_con': None,
            'T_raw': 1.23,
            'T_std_raw': 0.38,
            'T_obs': 1.12,
            'T_obs_std': 0.61
        },
        'ssp245': {
            'a': -0.48,
            'b': 0.57,
            'r2': 0.92,
            'R_atm': 3.70,
            'R_atm_std': 0.60,
            'SAF_raw': 2.59,
            'SAF_std_raw': 1.18,
            'SAF_con': 1.41,
            'SAF_std_con': 0.75,
            'T_raw': 3.16,
            'T_std_raw': 0.83,
            'T_con': 2.57,
            'T_std_con': 0.66
        },
        'ssp585': {
            'a': -0.47,
            'b': 1.01,
            'r2': 0.92,
            'R_atm': 7.15,
            'R_atm_std': 1.20,
            'SAF_raw': 4.71,
            'SAF_std_raw': 2.27,
            'SAF_con': 2.63,
            'SAF_std_con': 1.61,
            'T_raw': 5.86,
            'T_std_raw': 1.54,
            'T_con': 4.85,
            'T_std_con': 1.31
        }
    }
    
    if scenario not in parameters:
        raise ValueError(f"Unknown scenario: {scenario}. Choose from 'historical', 'ssp245', 'ssp585'")
    
    return parameters[scenario]


# ==================== Example usage ====================
if __name__ == "__main__":
    print("SRN Framework - Core Functions")
    print("=" * 60)
    print("\nThis module provides eight core functions:")
    print("1. compute_srn_relationship()       - establish N = a·R + b")
    print("2. compute_radiative_contributions() - calculate R from components")
    print("3. compute_nonradiative_contribution() - calculate N from FLUX+Q")
    print("4. decompose_nonradiative_contribution() - split into SAF/ATM parts")
    print("5. propagate_constraint()          - propagate SAF constraint to total warming")
    print("6. compute_total_warming()         - calculate ΔT_S = R + N")
    print("7. feedback_parameter()            - compute λ = 1 + a (for reference)")
    print("8. validate_srn_framework()        - verify post-constraint consistency")
    print("9. get_framework_parameters()      - get pre-computed parameters")
    
    print("\n" + "=" * 60)
    print("Example: SRN relationship for SSP2-4.5")
    print("=" * 60)
    
    # Get pre-computed parameters
    params = get_framework_parameters('ssp245')
    
    print(f"\nSRN parameters (SSP2-4.5):")
    print(f"  a = {params['a']:.2f}")
    print(f"  b = {params['b']:.2f} K")
    print(f"  r² = {params['r2']:.2f}")
    print(f"\nPhysical interpretation:")
    print(f"  Negative slope ({params['a']:.2f}) indicates that increased radiative")
    print(f"  warming is partially offset by enhanced non-radiative cooling.")
    print(f"\nSAF constraint results:")
    print(f"  ΔT_SAF: {params['SAF_raw']:.2f} ± {params['SAF_std_raw']:.2f} → {params['SAF_con']:.2f} ± {params['SAF_std_con']:.2f} K")
    print(f"  Total warming: {params['T_raw']:.2f} ± {params['T_std_raw']:.2f} → {params['T_con']:.2f} ± {params['T_std_con']:.2f} K")
    
    # Demonstrate propagation
    print(f"\nPropagation using SRN relationship:")
    print(f"  R_atm (unchanged) = {params['R_atm']:.2f} K")
    print(f"  R_raw = SAF_raw + R_atm = {params['SAF_raw']:.2f} + {params['R_atm']:.2f} = {params['SAF_raw'] + params['R_atm']:.2f} K")
    print(f"  R_con = SAF_con + R_atm = {params['SAF_con']:.2f} + {params['R_atm']:.2f} = {params['SAF_con'] + params['R_atm']:.2f} K")
    print(f"  N_raw = a·R_raw + b = {params['a']:.2f} × {params['SAF_raw'] + params['R_atm']:.2f} + {params['b']:.2f} = {params['a'] * (params['SAF_raw'] + params['R_atm']) + params['b']:.2f} K")
    print(f"  N_con = a·R_con + b = {params['a']:.2f} × {params['SAF_con'] + params['R_atm']:.2f} + {params['b']:.2f} = {params['a'] * (params['SAF_con'] + params['R_atm']) + params['b']:.2f} K")
    
    print("\n" + "=" * 60)
    print("All functions loaded successfully!")
    print("=" * 60)
