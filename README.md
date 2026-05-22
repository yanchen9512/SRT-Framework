SRN-Framework
Surface Radiative and Non-radiative Contribution Framework

A validated two-stage framework for constraining surface albedo feedback (SAF) and propagating constraints to total warming via surface energy budget decomposition.

Authors
Yan Chen - Conceptualization, methodology, validation, code implementation

Key Papers
Chen et al. (2026) - Manuscript under review - Framework development, HEC-SRN integration, and CMIP6 constraint

Chen et al. (2022) JGR - Observational constraint on SAF over Tibetan Plateau (historical validation)

Core Concept
The SRN framework establishes a linear relationship between the total radiative contribution (R) and the total non-radiative contribution (N):

N = a·R + b

where:

R = total radiative contribution (ΔT_SAF + ΔT_CRF + ΔT_SW + ΔT_LW), positive = warming

N = total non-radiative contribution (-ΔT_H+LE+Q), positive = cooling (in spring)

a = sensitivity of non-radiative response to radiative forcing (negative = partial offset)

b = intercept from linear regression; treated as empirical parameter without physical interpretation (arises from extrapolation beyond observed R range)

Alternative feedback-like form (not used in main text, for conceptual reference):

ΔT_S = (1+a)·R + b, with effective feedback parameter λ = 1 + a (≈ 0.5 for TP spring)

Framework Workflow
Establish SRN relationship (N = a·R + b) from CMIP6 multi-model ensemble (Fig. 1b)

Decompose surface warming into radiative contributions (R) and non-radiative contribution (N) (Fig. 1a)

Constrain SAF using HEC (Hierarchical Emergent Constraint) with multi-source observational benchmark γ_obs = -0.63 ± 0.07 % K⁻¹ (Fig. 2)

Propagate constraint through SRN relationship: R_con = ΔT_SAF_con + R_atm (R_atm unchanged) → N_con = a·R_con + b → ΔT_S_con = R_con + N_con

Validate using historical period independent data (Chen et al., 2022)

Key Findings
Parameter	Historical (1982-2014)	SSP2-4.5 (2080-2099)	SSP5-8.5 (2080-2099)
a (slope)	-0.54	-0.48	-0.47
b (intercept, K)	-0.15	0.57	1.01
r²	0.80	0.92	0.92
SAF reduction	—	46% (2.59→1.41 K)	44% (4.71→2.63 K)
Total warming reduction	—	21% (3.16→2.57 K)	15% (5.86→4.85 K)
Uncertainty reduction (SAF)	—	36%	29%
Uncertainty reduction (Total)	—	21%	15%
Key physical insights:

Negative slope (-0.48 to -0.47) indicates increased radiative warming is partially offset by enhanced non-radiative cooling (turbulent + ground heat fluxes)

Near-identical slopes across scenarios reveal cross-scenario robustness of SRN relationship

Decreasing slope magnitude (|a|: 0.54 → 0.48 → 0.47) suggests nonlinear saturation of cooling efficiency under higher forcing

Independent Validation
Using historical CMIP6 simulations (1982-2014) constrained by Chen et al. (2022) observations:

Validation method	Result	Status
Predicted ΔT_S	1.23 ± 0.38 K	✓
Observed ΔT_S (Chen et al., 2022)	1.12 ± 0.61 K	✓
HEC constraint validation	γ_season → γ_climate (r = 0.71-0.76)	✓
SRN relationship validation	N = a·R + b (r ≈ -0.96)	✓
All three validation methods passed.

Framework Advantages
Aspect	SRN Framework	TOA Feedback Framework
Perspective	Surface energy budget	Top-of-atmosphere radiation
Process resolution	Explicitly resolves turbulent + ground heat fluxes	Aggregates all non-radiative processes
Constraint target	Observable γ (albedo sensitivity)	Individual feedback parameters
Compensation mechanism	Directly visible (N = a·R + b)	Requires decomposition
Applicability	Regional (e.g., Tibetan Plateau)	Global mean
