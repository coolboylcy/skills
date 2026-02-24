---
name: validator-correlated-judgment
description: >
  Helps identify when multiple attestation validators share training data,
  model architecture, or organizational upstream — causing them to have
  correlated blind spots that make multi-validator attestation no stronger
  than single-validator attestation.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl, python3]
      env: []
    emoji: "🧠"
  agent_card:
    capabilities: [validator-correlation-analysis, epistemic-blind-spot-detection, multi-validator-independence-checking]
    attack_surface: [L2]
    trust_dimension: attack-surface-coverage
    published:
      clawhub: false
      moltbook: false
---

# You Have Three Independent Validators. They All Miss the Same Things.

> Helps identify when attestation validators are organizationally independent
> but epistemically correlated — the failure mode where diversity of validators
> does not produce diversity of judgment.

## Problem

Multi-validator attestation assumes that independent validators provide
independent checks. The assumption is wrong when validators share upstream
dependencies that determine what they can and cannot detect.

Two validators trained on the same dataset will systematically agree — including
on what they miss. Their organizational independence is real. Their epistemic
independence is not. A skill that evades one validator's threat model will evade
the other's with the same probability, not an independent one. The combined
attestation is not stronger than either alone; it is the same check run twice
under different names.

This matters because correlated validators produce a false sense of coverage. An
agent operator looking at attestation badges from three validators reasonably
assumes that each validator is providing an independent check. If those validators
share training provenance, fine-tuning pipeline, or base model, the checks are
correlated. A systematic evasion technique that works against any one of them
likely works against all three — the diversification does not reduce the risk.

The organizational diversity assessment in standard attestation root analysis
catches organizational overlap. It does not catch epistemic overlap across
organizationally independent validators that share training lineage.

## What This Analyzes

This analyzer examines validator judgment correlation across five dimensions:

1. **Training provenance disclosure** — Do validators disclose the datasets,
   base models, or fine-tuning procedures used to develop their evaluation
   capabilities? Undisclosed provenance makes correlation undetectable

2. **Base model overlap** — Do multiple validators derive from the same
   foundation model? Validators that share a base model share that model's
   systematic biases and blind spots, regardless of organizational independence

3. **Fine-tuning pipeline similarity** — Were validators trained on similar
   security datasets or red-teaming corpora? Shared training data produces
   shared detection coverage — and shared detection gaps

4. **Behavioral correlation testing** — When presented with the same edge-case
   skills, do multiple validators agree at rates that exceed what independent
   judgment would predict? High agreement on ambiguous cases is a signal of
   correlated rather than independent evaluation

5. **Systematic evasion transferability** — Does a technique that evades
   Validator A have a higher-than-expected success rate against Validator B?
   High transferability indicates shared blind spots from correlated training

## How to Use

**Input**: Provide one of:
- A list of validators with their disclosed training provenance
- Attestation results from multiple validators on the same set of edge-case skills
- A validator pair to test for behavioral correlation

**Output**: A correlation report containing:
- Training provenance overlap assessment
- Base model and fine-tuning similarity score
- Behavioral correlation coefficient (observed vs. independent baseline)
- Evasion transferability estimate
- Effective independent validator count (after correlation adjustment)
- Correlation verdict: INDEPENDENT / WEAKLY-CORRELATED / CORRELATED / MONOCULTURE

## Example

**Input**: Analyze validator correlation for `Validator-A`, `Validator-B`,
`Validator-C` attesting `data-processor` skill

```
🧠 VALIDATOR CORRELATED JUDGMENT ANALYSIS

Skill: data-processor v2.3
Validators: 3
Audit timestamp: 2025-06-10T14:00:00Z

Training provenance:
  Validator-A: base=GPT-class, fine-tuned on SecDataset-v2, org=AuditCo
  Validator-B: base=GPT-class, fine-tuned on SecDataset-v2, org=SafeCheck
  Validator-C: base=LLaMA-class, fine-tuned on internal corpus, org=TrustLab

  Validator-A and Validator-B: same base model + same fine-tuning dataset
  → Organizational independence: ✅ different orgs
  → Epistemic independence: ⚠️ correlated (shared base + fine-tune)

Behavioral correlation test (50 edge-case skills):
  A-B agreement rate: 94% (independent baseline: ~70%)
  A-C agreement rate: 71% (consistent with independence)
  B-C agreement rate: 73% (consistent with independence)

  A-B correlation exceeds independence baseline by 24 percentage points
  → Validators A and B are behaviorally correlated

Evasion transferability:
  Skills evading A: 8/50 edge cases
  Same skills evading B: 7/8 (87.5% transfer rate)
  Same skills evading C: 3/8 (37.5% transfer rate, consistent with independence)

Effective independent validator count: 2.1 (not 3)
  Validator-A and Validator-B count as ~1.1 independent validators
  Validator-C provides one genuinely independent evaluation

Correlation verdict: CORRELATED
  Three validators, two organizations, but effective independence of ~2.
  Validator-A and Validator-B provide redundant rather than independent coverage.
  Systematic evasion targeting SecDataset-v2 blind spots defeats both simultaneously.

Recommended actions:
  1. Require training provenance disclosure as attestation metadata
  2. Weight Validator-A and Validator-B as a single validator for coverage purposes
  3. Add a third genuinely independent validator (different base model + training corpus)
  4. Test candidate validators for behavioral correlation before accepting as independent
```

## Related Tools

- **attestation-root-diversity-analyzer** — Measures organizational concentration
  in the trust graph; validator-correlated-judgment measures epistemic concentration
  that organizational analysis cannot detect
- **transparency-log-auditor** — Checks whether attestation events are independently
  auditable; correlation analysis applies to the validators producing those events
- **hollow-validation-checker** — Detects structurally empty validation; correlated
  validators may all pass the same hollow validations for the same structural reason
- **observer-effect-probe** — Tests evasion of attestation; correlated validators
  are more vulnerable to systematic evasion because one technique transfers to all

## Limitations

Validator correlated judgment analysis requires training provenance disclosure
that most current validators do not provide. Where provenance is undisclosed,
behavioral correlation testing is the only available signal — and it requires
running the same edge-case skills through multiple validators, which may not
be operationally feasible. Behavioral correlation is a proxy for epistemic
correlation, not a direct measure of it; high agreement on edge cases could
reflect genuine convergence on correct answers rather than shared blind spots.
The analysis identifies correlation risk, not confirmed evasion; correlated
validators may still provide meaningful coverage even when correlated. The
independent baseline for agreement rates depends on the difficulty distribution
of the test cases, which must be calibrated carefully to avoid false positives.
