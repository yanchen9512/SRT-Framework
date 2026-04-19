# SRT-Framework

**Surface Radiative-forcing and Thermodynamic-response Framework**

A validated two-stage framework for constraining climate feedbacks and propagating constraints to total warming via surface energy budget.

## Authors

- [Yan Chen] - Conceptualization, methodology, validation, code implementation
- [Duoying Ji] - SRT relationship conceptualization

## Key Papers

- Chen et al.(2026) GRL under review - Framework development and validation
- Chen et al. (2022) JGR - Observational constraint on SAF over Tibetan Plateau

## Core Concept

The SRT framework establishes a linear relationship:

**R = a·F + b**

where:
- **F** = total radiative forcing , positive = warming
- **R** = total thermodynamic response, positive = cooling
- **a** = sensitivity of cooling to forcing (positive = negative feedback)
- **b** = baseline response determined by background climate state

## Framework Workflow

1. **Establish SRT relationship** from CMIP6 multi-model ensemble
2. **Decompose** total response into SAF-driven and atmosphere-driven parts
3. **Constrain SAF** using HEC (Hierarchical Emergent Constraint) with observed γ
4. **Propagate** constraint to total warming via SRT (assuming S_atm unchanged)
5. **Validate** using historical period independent data

## Key Findings

- Historical period: a = 0.54, b = -0.15 K (r² = 0.80)
- SSP2-4.5: a = 0.48, b = -0.57 K
- SSP5-8.5: a = 0.47, b = -1.01 K
- Positive slope indicates robust negative feedback
- Decreasing slope with forcing reveals nonlinear saturation of cooling efficiency

## Independent Validation

Using historical CMIP6 simulations (1982-2014) + Chen et al. (2022) observations:
- Predicted ΔTS = 1.23 ± 0.38 K
- Observed ΔTS = 1.12 ± 0.61 K
- ✓ All three validation methods passed

## Repository Structure
