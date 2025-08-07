# No-Free-Parameter Ledger (Audit v1)

This document lists every numeric ingredient and classifies it as:
- Derived: forced by axioms/lemmas
- Unit-anchored: SI mapping only
- Choice pending proof: plausibly derivable; uniqueness proof needed
- Free/hidden: unconstrained or inconsistent

## Core constants and structures
- φ = (1+√5)/2
  - Source: fixed point of x=1+1/x with integer k=1 (countability + minimization)
  - Class: Derived
- J(x) = ½(x + 1/x)
  - Source: dual-balance symmetry + self-similarity; higher orders diverge
  - Class: Derived (uniqueness proof to formalize)
- D = 3 (spatial)
  - Source: stable non-trivial link minimal in 3D
  - Class: Derived (topology)
- 8-beat cycle = 2^3
  - Source: complete recognition of voxel’s 8 vertices
  - Class: Derived
- Gap generator F(z)=ln(1+z/φ), g_m=(−1)^{m+1}/(m φ^m)
  - Class: Derived; Appendix M
- E_coh = φ^−5 (dimensionless)
  - Source: five minimal DOF
  - Class: Derived

## SI mapping (unit anchors)
- c, ħ, G: standards
- λ_rec=√(ħG/c^3): cost–curvature bridge

## Fine-structure constant (α)
- Seed 4π×11 (k=11=8+3)
  - Class: Choice pending proof
- Curvature subtraction δκ=−103/(102 π^5)
  - Class: Choice pending proof
- Series consistency
  - Class: Derived
  - Action: Use F(z) exclusively

## ILG and τ0
- w(k,a)=1+φ^(−3/2)[a/(k τ0)]^α, α=½(1−1/φ)
  - Class: Choice pending proof
- τ0=2π/(8 ln φ)
  - Class: Choice pending proof

## Cosmology
- V0 (inflation amplitude) set by A_s
  - Class: Unit-anchored unless derived
- Ω_dm = sin(π/12)+δ (δ≈0.0061)
  - Class: Free/hidden (inconsistent)

## Particle masses
- m_i = B_i · E_coh · φ^(r_i + f_i)
  - B_i (sector integer): Choice pending proof
  - r_i (rung integer): Choice pending proof
  - f_i (RG + F(z)): Derived

## Muon g−2
- Weights lnφ/(m·5^m), suppression 0.0451: Free/hidden until derived

## Biology / number theory
- DNA pitch residue f_bio=0.0414: Free/hidden

---
Action plan: α integers; ILG/τ0 derivations; B_i/r_i table; cosmology curves; unify via F(z).