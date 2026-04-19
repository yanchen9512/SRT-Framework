#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SRT (Surface Radiative-forcing and Thermodynamic-response) Framework

This framework establishes a linear relationship between total radiative forcing (F)
and total thermodynamic response (R): R = a·F + b

The slope 'a' represents the sensitivity of surface cooling to radiative forcing
(positive = negative feedback). The intercept 'b' represents the baseline response
determined by background climate state (temperature, snow cover, soil moisture).

Core applications:
1. Constrain SAF (Surface Albedo Feedback) using HEC
2. Propagate constraint to total warming via energy budget
3. Validate using historical period observations

Author: Yan Chen
ORCID: https://orcid.org/0009-0009-9521-3386
License: MIT
"""

import numpy as np
from scipy import stats
import pandas as pd


def compute_srt_relationship(R_forcing, R_response):
    """
    Compute SRT relationship: R_response = a * R_forcing + b

    Parameters
    ----------
    R_forcing : array-like
        Total radiative forcing F (K, positive = warming)
    R_response : array-like
        Total thermodynamic response R (K, positive = cooling)

    Returns
    -------
    dict : Contains slope 'a', intercept 'b', correlation 'r', r-squared 'r2',
           p-value 'p', standard error 'std_err'
    """
    a, b, r, p, std_err = stats.linregress(R_forcing, R_response)
    return {
        'a': a,
        'b': b,
        'r': r,
        'r2': r**2,
        'p': p,
        'std_err': std_err
    }


def decompose_thermodynamic_response(S_total, SAF, a, b):
    """
    Decompose total thermodynamic response into SAF-driven and atmosphere-driven parts

    Parameters
    ----------
    S_total : array-like
        Total thermodynamic response S (K, negative = cooling)
    SAF : array-like
        SAF warming contribution (K)
    a, b : float
        SRT parameters from compute_srt_relationship

    Returns
    -------
    dict : Contains S_saf (SAF-driven) and S_atm (atmosphere-driven)
    """
    # SAF-driven response (using SRT relationship)
    S_saf = a * SAF + b

    # Atmosphere-driven response (residual)
    S_atm = S_total - S_saf

    return {
        'S_saf': S_saf,
        'S_atm': S_atm
    }


def propagate_constraint(SAF_raw, SAF_con, S_atm, a, b):
    """
    Propagate SAF constraint to total warming using SRT framework

    Parameters
    ----------
    SAF_raw : array-like
        Raw SAF warming (K)
    SAF_con : array-like
        Constrained SAF warming from HEC (K)
    S_atm : array-like
        Atmosphere-driven thermodynamic response (assumed unchanged)
    a, b : float
        SRT parameters

    Returns
    -------
    dict : Contains constrained S_saf, S_total, and temperature change
    """
    # Constrained SAF-driven response
    S_saf_con = a * SAF_con + b

    # Constrained total thermodynamic response
    S_total_con = S_atm + S_saf_con

    return {
        'S_saf_con': S_saf_con,
        'S_total_con': S_total_con
    }


def validate_srt_framework(S_total, F_forcing, a, b):
    """
    Validate that constrained system still satisfies SRT relationship

    Parameters
    ----------
    S_total : array-like
        Total thermodynamic response (K)
    F_forcing : array-like
        Total radiative forcing (K)
    a, b : float
        SRT parameters

    Returns
    -------
    dict : Contains predicted S from SRT and residual
    """
    S_pred = a * F_forcing + b
    residual = S_total - S_pred

    return {
        'S_pred': S_pred,
        'residual': residual,
        'residual_mean': np.mean(residual),
        'residual_std': np.std(residual)
    }


# ==================== Example usage with sample data ====================
if __name__ == "__main__":
    # Sample data structure (replace with actual CMIP6 data)
    # F_forcing  (total radiative forcing, K)
    # S_total  (total thermodynamic response, K, negative)
    # SAF_raw (raw SAF warming, K)
    # SAF_con (constrained SAF warming from HEC, K)

    print("SRT Framework - Core Functions")
    print("=" * 50)
    print("\nThis module provides four core functions:")
    print("1. compute_srt_relationship() - establish R = a·F + b")
    print("2. decompose_thermodynamic_response() - split into SAF/ATM parts")
    print("3. propagate_constraint() - propagate SAF constraint to total warming")
    print("4. validate_srt_framework() - verify post-constraint consistency")
