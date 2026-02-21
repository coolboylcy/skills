# AI Governance & Responsible AI Engine

Complete framework for establishing AI governance programs, ensuring regulatory compliance (EU AI Act, NIST AI RMF, ISO 42001), managing algorithmic risk, and building trustworthy AI systems. Use when designing AI policies, conducting AI impact assessments, classifying AI system risk, building model governance, establishing AI ethics boards, or preparing for AI-specific regulation.

---

## Phase 1: Governance Maturity Assessment

Before building anything, assess where you are.

### AI Governance Maturity Model (Score 1-5 per dimension)

| Dimension | 1 — Ad Hoc | 3 — Defined | 5 — Optimized |
|-----------|-----------|------------|--------------|
| **Policy** | No AI-specific policies | Written policies, partial adoption | Living policies, automated enforcement |
| **Risk Management** | No AI risk process | Risk assessments for high-risk systems | Continuous monitoring, automated alerts |
| **Accountability** | No clear ownership | Roles defined, inconsistent execution | RACI embedded, AI ethics board active |
| **Transparency** | No documentation | Model cards for some systems | Full registry, explainability for all |
| **Fairness** | No bias testing | Ad-hoc bias checks | Systematic testing, monitoring, remediation |
| **Data Governance** | No AI data standards | Data quality rules for AI | Automated lineage, consent, quality gates |
| **Compliance** | Unaware of AI regulations | Aware, partial compliance | Proactive, audit-ready, continuous |
| **Culture** | AI literacy absent | Training for AI teams only | Organization-wide AI literacy program |

**Scoring:**
- 8-16: **Foundation** — Start with Phase 2-3 immediately
- 17-28: **Developing** — Focus on risk classification and accountability
- 29-40: **Advanced** — Optimize monitoring and continuous compliance

### Governance Brief YAML

```yaml
organization:
  name: "[Company]"
  industry: "[sector]"
  size: "[employees]"
  ai_maturity: "[foundation/developing/advanced]"

ai_landscape:
  total_ai_systems: [count]
  customer_facing: [count]
  decision_making: [count]  # Systems that make/influence decisions about people
  generative_ai: [count]
  third_party_ai: [count]   # Vendor AI embedded in your stack

regulatory_exposure:
  eu_ai_act: [yes/no]       # Serve EU customers or employees?
  nist_ai_rmf: [yes/no]     # US federal contracts or alignment?
  iso_42001: [yes/no]       # Certification target?
  sector_specific: "[HIPAA AI, FDA SaMD, SEC AI, etc.]"

current_state:
  ai_policy_exists: [yes/no]
  ai_inventory_complete: [yes/no]
  bias_testing_process: [yes/no]
  incident_response_for_ai: [yes/no]
  ai_ethics_board: [yes/no]

priority: "[compliance/risk reduction/trust building/competitive advantage]"
timeline: "[3/6/12 months]"
```

---

## Phase 2: AI System Inventory & Risk Classification

You can't govern what you don't know exists.

### AI System Registry YAML

```yaml
system:
  id: "AI-[sequential]"
  name: "[descriptive name]"
  description: "[what it does in plain language]"
  owner: "[team/person accountable]"
  
  classification:
    type: "[predictive/generative/recommendation/automation/detection/optimization]"
    eu_ai_act_risk: "[unacceptable/high/limited/minimal]"
    internal_risk_tier: "[critical/high/medium/low]"
    
  scope:
    users_affected: "[internal only/customers/public]"
    decisions_influenced: "[what decisions does this affect?]"
    autonomy_level: "[advisory/human-in-loop/human-on-loop/autonomous]"
    reversibility: "[easily reversed/difficult to reverse/irreversible]"
    
  data:
    training_data_sources: ["[list sources]"]
    personal_data: [yes/no]
    sensitive_categories: ["[race/gender/age/disability/etc. if applicable]"]
    data_freshness: "[static/periodic refresh/real-time]"
    
  technical:
    model_type: "[LLM/classifier/regression/ensemble/rule-based/hybrid]"
    vendor: "[in-house/vendor name]"
    version: "[current version]"
    last_evaluated: "[date]"
    
  governance:
    impact_assessment_completed: [yes/no]
    bias_audit_completed: [yes/no]
    explainability_method: "[SHAP/LIME/attention/rule extraction/none]"
    monitoring_active: [yes/no]
    human_override_available: [yes/no]
```

### EU AI Act Risk Classification Decision Tree

```
1. Does the system manipulate behavior, exploit vulnerabilities, 
   or enable social scoring?
   → YES: UNACCEPTABLE (banned) — Stop. Do not deploy.

2. Is it used in any of these domains?
   - Biometric identification (real-time in public)
   - Critical infrastructure (energy, transport, water)
   - Education (access, assessment)
   - Employment (recruitment, evaluation, termination)
   - Essential services (credit, insurance, benefits)
   - Law enforcement (risk assessment, evidence evaluation)
   - Migration/asylum (applications, surveillance)
   - Justice (sentencing, parole)
   → YES: HIGH-RISK — Full compliance required (Phase 3-8)

3. Does it interact directly with people?
   (Chatbots, deepfake generators, emotion recognition)
   → YES: LIMITED RISK — Transparency obligations (disclose AI)

4. None of the above?
   → MINIMAL RISK — Voluntary codes of practice encouraged
```

### Internal Risk Tier (Beyond EU Classification)

| Factor | Weight | Low (1) | Medium (3) | High (5) |
|--------|--------|---------|------------|----------|
| **People Impact** | 25% | Convenience features | Influences decisions | Determines outcomes |
| **Scale** | 20% | <100 users | 100-10K users | >10K users |
| **Reversibility** | 20% | Easy to reverse | Partial reversal | Irreversible |
| **Data Sensitivity** | 15% | Public data | Personal data | Sensitive categories |
| **Autonomy** | 10% | Advisory only | Human-in-loop | Autonomous |
| **Reputational** | 10% | Low visibility | Customer-facing | Public/media attention |

**Tier Assignment:**
- Score 1.0-2.0: **Low** — Standard development practices
- Score 2.1-3.5: **Medium** — Impact assessment + bias review required
- Score 3.6-5.0: **High/Critical** — Full governance lifecycle required

---

## Phase 3: AI Impact Assessment (AIIA)

Required for all High-Risk and Medium-Risk systems.

### Impact Assessment Template

```yaml
assessment:
  system_id: "AI-[ref]"
  assessor: "[name/team]"
  date: "[YYYY-MM-DD]"
  review_type: "[initial/periodic/triggered]"

purpose_and_necessity:
  problem_statement: "[What problem does this solve?]"
  necessity_test: "[Why AI specifically? Could rules/heuristics work?]"
  proportionality: "[Is the AI approach proportional to the problem?]"
  alternatives_considered: ["[list non-AI alternatives evaluated]"]

stakeholder_analysis:
  direct_users: "[who uses the system]"
  affected_parties: "[who is affected by system outputs]"
  vulnerable_groups: "[any vulnerable populations affected?]"
  stakeholder_consultation: "[how were affected parties consulted?]"

rights_impact:
  privacy: "[how personal data is used, consent mechanism]"
  non_discrimination: "[bias risk, protected characteristics]"
  autonomy: "[does it restrict individual choices?]"
  dignity: "[does it treat people as means or ends?]"
  due_process: "[can decisions be challenged/appealed?]"
  transparency: "[can affected parties understand the decision?]"

risk_register:
  - risk: "[description]"
    likelihood: "[rare/unlikely/possible/likely/almost certain]"
    impact: "[insignificant/minor/moderate/major/catastrophic]"
    mitigation: "[planned mitigation]"
    residual_risk: "[low/medium/high]"
    owner: "[who monitors this]"

fairness_assessment:
  protected_characteristics_tested: ["[list: age, gender, race, etc.]"]
  bias_metrics_used: ["[demographic parity, equalized odds, etc.]"]
  disparate_impact_found: [yes/no]
  remediation_plan: "[if yes, what's the plan]"

explainability:
  method: "[SHAP/LIME/counterfactual/rule extraction/attention]"
  audience: "[who needs explanations — users/affected/regulators]"
  format: "[natural language/feature importance/decision factors]"
  individual_explanations: [yes/no]

controls:
  human_oversight: "[type and frequency]"
  monitoring: "[what metrics, what frequency]"
  kill_switch: "[how to disable quickly]"
  incident_response: "[link to playbook]"
  audit_trail: "[what's logged]"

decision:
  recommendation: "[approve/approve with conditions/reject/defer]"
  conditions: ["[list any conditions for approval]"]
  review_date: "[next scheduled review]"
  approver: "[who has authority to approve]"
```

### Necessity Test Checklist

Before any AI deployment, answer:

- [ ] Have we clearly defined the problem AI is solving?
- [ ] Have we considered non-AI alternatives?
- [ ] Is the AI approach proportional to the risk?
- [ ] Do we have sufficient quality training data?
- [ ] Can we explain the system's decisions to affected parties?
- [ ] Is there a clear human oversight mechanism?
- [ ] Have we identified all stakeholders, including vulnerable groups?
- [ ] Can the system be disabled without business continuity failure?

**If any answer is "No"** — address before proceeding.

---

## Phase 4: AI Policy Framework

### Core Policies (Build in This Order)

#### 1. AI Acceptable Use Policy (AUP)

```markdown
# AI Acceptable Use Policy

## Purpose
Defines acceptable and prohibited uses of AI systems within [Organization].

## Scope
All employees, contractors, and vendors using or developing AI systems.

## Permitted Uses
- [List approved AI tools and their approved purposes]
- Internal productivity (with data handling rules)
- Customer-facing features (with transparency requirements)

## Prohibited Uses
- Processing sensitive data through unapproved AI tools
- Using AI to make final decisions about [employment/credit/etc.] without human review
- Generating content represented as human-created without disclosure
- Using personal/sensitive data for AI training without consent
- Deploying AI systems not registered in the AI inventory
- Using AI to profile or score individuals on protected characteristics

## Data Rules
- Never input [PII/PHI/financial data/trade secrets] into external AI tools
- All AI-generated outputs must be reviewed before external use
- Customer data used for AI must comply with privacy policy and consent

## Accountability
- Each AI system must have a designated owner
- Violations reported to [AI governance team/ethics board]
- [Consequences for violations]
```

#### 2. AI Development & Deployment Standard

```markdown
# AI Development Lifecycle Standard

## Pre-Development Gate
- [ ] Problem statement approved
- [ ] AI necessity confirmed (non-AI alternatives evaluated)
- [ ] Risk classification completed
- [ ] Data governance review passed
- [ ] Impact assessment initiated (if medium/high risk)

## Development Standards
- [ ] Training data documented (source, quality, bias assessment)
- [ ] Model selection justified and documented
- [ ] Bias testing performed on protected characteristics
- [ ] Explainability method chosen and implemented
- [ ] Performance metrics defined with minimum thresholds
- [ ] Adversarial testing / red-teaming completed

## Pre-Deployment Gate
- [ ] Impact assessment completed and approved
- [ ] Model card published to AI registry
- [ ] Human oversight mechanism tested
- [ ] Monitoring dashboards configured
- [ ] Incident response playbook reviewed
- [ ] Audit logging verified
- [ ] User disclosure/transparency implemented

## Post-Deployment
- [ ] Performance monitoring active
- [ ] Bias monitoring active (demographic metrics)
- [ ] Drift detection configured
- [ ] User feedback collection active
- [ ] Periodic review scheduled (quarterly for high-risk)
```

#### 3. AI Vendor Assessment Checklist

For any third-party AI (vendor tools, APIs, embedded AI):

- [ ] Vendor provides model documentation?
- [ ] Data handling practices documented (where data goes, retention)?
- [ ] Vendor allows bias auditing or provides bias reports?
- [ ] Contract includes AI-specific provisions (liability, IP, data use)?
- [ ] Vendor's training data doesn't include your proprietary data (without consent)?
- [ ] Exit strategy defined (data portability, model independence)?
- [ ] Vendor compliance with relevant AI regulations documented?
- [ ] Sub-processor AI tools disclosed?
- [ ] SLA covers AI-specific failures (hallucination, bias incidents)?
- [ ] Right to audit included in contract?

---

## Phase 5: Fairness & Bias Management

### Bias Testing Protocol

#### Step 1: Define Protected Characteristics

Test across ALL relevant protected characteristics:
- Age, gender/sex, race/ethnicity, disability, religion
- Plus: socioeconomic status, geographic location, language
- Industry-specific: credit history (lending), medical conditions (insurance)

#### Step 2: Select Fairness Metrics

| Metric | Definition | Use When |
|--------|-----------|----------|
| **Demographic Parity** | Equal positive prediction rates across groups | Selection/approval decisions |
| **Equalized Odds** | Equal TPR and FPR across groups | Classification with known outcomes |
| **Predictive Parity** | Equal precision across groups | Risk scoring systems |
| **Individual Fairness** | Similar individuals get similar predictions | Personalization systems |
| **Counterfactual Fairness** | Changing protected attribute doesn't change prediction | Any decision system |

**Key Rule:** No single metric captures all fairness. Use at least 2 metrics. Document WHY you chose them.

#### Step 3: Testing Cadence

| System Risk | Pre-Deploy | Post-Deploy | Triggered |
|-------------|-----------|-------------|-----------|
| **High** | Full audit | Monthly | Any complaint or data change |
| **Medium** | Focused audit | Quarterly | Significant model update |
| **Low** | Basic check | Annually | Major complaint |

#### Step 4: Remediation Decision Tree

```
Bias detected (disparity > threshold)?
├── YES: Is disparity legally significant (4/5ths rule)?
│   ├── YES: STOP deployment. Remediate before any use.
│   │   Options: rebalance training data, adjust thresholds,
│   │   add fairness constraints, use different model
│   └── NO: Document finding. Monitor closely.
│       If trend worsening → escalate to YES path
└── NO: Document clean results. Schedule next review.
```

### Bias Audit Report Template

```yaml
audit:
  system_id: "AI-[ref]"
  date: "[YYYY-MM-DD]"
  auditor: "[internal/external name]"
  
characteristics_tested:
  - attribute: "[e.g., gender]"
    groups: ["[male, female, non-binary]"]
    sample_sizes: [n1, n2, n3]
    
metrics:
  - name: "[demographic_parity]"
    results:
      - group: "[group A]"
        rate: [0.XX]
      - group: "[group B]"
        rate: [0.XX]
    disparity_ratio: [0.XX]
    threshold: [0.80]  # 4/5ths rule
    pass: [yes/no]
    
findings:
  - finding: "[description]"
    severity: "[critical/high/medium/low]"
    recommendation: "[action]"
    
overall_assessment: "[pass/conditional pass/fail]"
next_review: "[date]"
```

---

## Phase 6: Transparency & Explainability

### Model Card Template

Every AI system gets a model card (adapted from Mitchell et al.).

```yaml
model_card:
  system_id: "AI-[ref]"
  version: "[X.Y.Z]"
  last_updated: "[date]"
  
overview:
  name: "[system name]"
  purpose: "[what it does, in plain language]"
  intended_users: "[who should use this]"
  out_of_scope_uses: "[explicitly, what this should NOT be used for]"
  
performance:
  primary_metric: "[metric name]: [value]"
  secondary_metrics:
    - "[metric]: [value]"
  evaluation_data: "[description of test dataset]"
  known_limitations: ["[list known failure modes]"]
  
fairness:
  tested_characteristics: ["[list]"]
  metrics_used: ["[list]"]
  results_summary: "[pass/conditional/fail with details]"
  
data:
  training_data: "[description — types, sources, size, date range]"
  preprocessing: "[key transformations applied]"
  known_data_gaps: ["[what's underrepresented]"]
  
ethical_considerations:
  risks: ["[identified risks]"]
  mitigations: ["[what was done about them]"]
  
technical:
  model_type: "[architecture]"
  training_compute: "[if relevant]"
  inference_latency: "[p50/p99]"
  
contact:
  owner: "[team/person]"
  feedback: "[how to report issues]"
```

### Explainability Selection Guide

| Audience | Need | Method | Format |
|----------|------|--------|--------|
| **End user** | "Why did I get this result?" | Counterfactual, feature highlights | Natural language, top 3 factors |
| **Affected person** | "Why was I denied?" | LIME/SHAP individual | Plain language explanation + appeal process |
| **Regulator** | "How does the system work?" | Model card + global SHAP | Technical documentation |
| **Internal audit** | "Is it working correctly?" | Full SHAP + confusion matrix | Dashboard + detailed report |
| **Developer** | "Why is it failing here?" | SHAP + attention + error analysis | Technical exploration tools |

### Transparency Obligations Checklist

- [ ] Users know they're interacting with AI (disclosure)
- [ ] AI-generated content is labeled (especially deepfakes/synthetic media)
- [ ] Affected parties can request explanation of AI-influenced decisions
- [ ] Appeals/human review process exists and is communicated
- [ ] Data sources and general logic are describable in plain language
- [ ] Model card is published internally (and externally for high-risk)
- [ ] Changes to AI systems are communicated to affected parties

---

## Phase 7: AI Incident Response

### AI-Specific Incident Types

| Incident Type | Example | Severity Guide |
|---------------|---------|----------------|
| **Bias incident** | System discriminates against protected group | SEV-1 if customer-facing |
| **Hallucination** | Generates false information acted upon | SEV-2 if causes harm |
| **Data leak** | Training data contains/reveals PII | SEV-1 always |
| **Adversarial attack** | Prompt injection, model manipulation | SEV-2, SEV-1 if data exfiltrated |
| **Drift degradation** | Model accuracy drops below threshold | SEV-3, SEV-2 if decision-making |
| **Unintended behavior** | System operates outside intended scope | Depends on impact |
| **Consent violation** | Data used without proper consent | SEV-1 if regulatory exposure |

### AI Incident Response Playbook

```
DETECTION
├── Automated: monitoring alert, drift detection, bias threshold breach
├── User report: complaint, feedback, support ticket
└── External: media report, regulator inquiry, researcher disclosure

TRIAGE (within 1 hour)
├── Classify severity (SEV-1 to SEV-4)
├── Identify affected population and scale
├── Determine: is the system still causing harm?
│   └── YES → proceed to immediate containment
└── Assign incident commander

CONTAINMENT (SEV-1: immediate, SEV-2: <4 hours)
├── Option A: Disable AI system entirely (kill switch)
├── Option B: Revert to previous model version
├── Option C: Add human-in-loop gate
├── Option D: Restrict to subset of users/use cases
└── Document containment decision and rationale

INVESTIGATION
├── Root cause analysis (model? data? deployment? adversarial?)
├── Impact quantification (how many affected, how severely)
├── Timeline reconstruction
├── Bias audit if discrimination suspected
└── Preserve all evidence (model version, data, logs)

REMEDIATION
├── Fix root cause (retrain, patch, redesign)
├── Validate fix with held-out test including affected demographic
├── Update model card and documentation
├── Re-run impact assessment if significant change
└── Get approval before redeployment

COMMUNICATION
├── Internal: stakeholders, leadership, legal
├── Affected parties: notification if required by law or policy
├── Regulators: if required (EU AI Act: 72-hour notification for serious incidents)
└── Public: if media attention or significant impact

POST-INCIDENT
├── Blameless post-mortem (focus on systemic fixes)
├── Update AI risk register
├── Update monitoring to catch similar incidents
├── Share lessons learned across AI teams
└── Schedule follow-up review (30 days)
```

### Communication Templates

**Internal Escalation (SEV-1):**
```
🚨 AI INCIDENT — [System Name] — SEV-1

What happened: [Brief description]
Impact: [Who affected, how many, what harm]
Current status: [Contained/Active/Investigating]
Containment action: [What was done]
Next steps: [Immediate actions]
Incident commander: [Name]
War room: [Link/channel]
```

**Affected Party Notification:**
```
Subject: Important notice about [service/decision]

We identified an issue with [system/service] that may have affected 
[your application/recommendation/score].

What happened: [Plain language, no jargon]
Who was affected: [Scope]
What we've done: [Containment + fix]
What this means for you: [Practical impact]
Your options: [Appeal, review, contact]

We take this seriously and have [actions taken to prevent recurrence].

Contact: [dedicated email/phone for questions]
```

---

## Phase 8: Regulatory Compliance Deep Dives

### EU AI Act Compliance Program (Effective August 2025)

**For High-Risk AI Systems (Article 6-51):**

| Requirement | What You Need | Evidence |
|------------|---------------|----------|
| **Risk Management** (Art 9) | Continuous risk identification and mitigation | Risk management plan + register + review records |
| **Data Governance** (Art 10) | Training data quality, relevance, representativeness | Data documentation + quality metrics + bias testing |
| **Technical Documentation** (Art 11) | Detailed system description | Model card + architecture + test results |
| **Record-Keeping** (Art 12) | Automatic logging of system operation | Audit logs + retention policy |
| **Transparency** (Art 13) | Instructions for use, capabilities, limitations | User documentation + model card |
| **Human Oversight** (Art 14) | Effective human oversight measures | Oversight design + training records |
| **Accuracy & Robustness** (Art 15) | Appropriate accuracy, resilience to errors | Performance benchmarks + adversarial testing |
| **Conformity Assessment** (Art 43) | Pre-market assessment (self or third-party) | Assessment report + CE marking |
| **Registration** (Art 49) | EU database registration | Registration confirmation |
| **Post-Market Monitoring** (Art 61) | Ongoing monitoring plan | Monitoring plan + incident reports |
| **Serious Incident Reporting** (Art 62) | Report to authorities within [timeframe] | Incident reports + notification records |

**For General-Purpose AI (GPAI) Models:**
- Technical documentation on training and testing
- Copyright policy compliance
- Training data summary
- Systemic risk assessment (for GPAI with systemic risk)

### NIST AI Risk Management Framework (AI RMF 1.0)

Four core functions — Map, Measure, Manage, Govern:

**GOVERN:**
- [ ] AI governance structure established
- [ ] Roles and responsibilities defined
- [ ] Policies reflect organizational values
- [ ] Risk tolerances established for AI
- [ ] Legal/regulatory requirements mapped

**MAP:**
- [ ] AI system purposes documented
- [ ] Stakeholders and affected communities identified
- [ ] Benefits, costs, and risks characterized
- [ ] Risk context established (operational environment)

**MEASURE:**
- [ ] Metrics identified for trustworthiness characteristics
- [ ] Systems evaluated for bias, security, privacy
- [ ] Feedback mechanisms from affected communities
- [ ] Metrics tracked over time (drift)

**MANAGE:**
- [ ] Risks prioritized and documented
- [ ] Risk treatment plans implemented
- [ ] Responses to identified risks tested
- [ ] Continuous improvement process active

### ISO 42001 (AI Management System) Overview

Key clauses for certification:
- **Clause 4:** Context — AI-specific interested parties and scope
- **Clause 5:** Leadership — Top management commitment to responsible AI
- **Clause 6:** Planning — AI risk assessment and treatment
- **Clause 7:** Support — Resources, competence, awareness for AI
- **Clause 8:** Operation — AI system lifecycle management
- **Clause 9:** Performance evaluation — Monitoring AI effectiveness
- **Clause 10:** Improvement — Corrective action for AI issues

---

## Phase 9: AI Ethics Board Design

### Board Structure

```yaml
ai_ethics_board:
  name: "AI Ethics Advisory Board"
  charter: "[link to charter document]"
  
  composition:  # Diverse perspectives required
    - role: "Chair"
      background: "[senior leader with ethics/compliance background]"
    - role: "Technical Lead"
      background: "[ML/AI engineering expertise]"
    - role: "Legal/Compliance"
      background: "[regulatory, privacy law]"
    - role: "Product/Business"
      background: "[understands use cases and customers]"
    - role: "External Ethicist"
      background: "[academic or independent ethics expert]"
    - role: "Affected Community Representative"
      background: "[represents those impacted by AI decisions]"
    - role: "Data/Privacy"
      background: "[data governance, privacy engineering]"
  
  mandate:
    - Review all high-risk AI impact assessments
    - Advise on ethical edge cases
    - Review AI incident post-mortems
    - Recommend policy updates
    - Annual AI governance program review
    
  authority: "[advisory/approval required for high-risk/veto power]"
  
  cadence:
    regular_meetings: "Monthly"
    urgent_review: "Within 48 hours for SEV-1 incidents"
    annual_review: "Full program assessment"
    
  decision_process:
    quorum: "[minimum members for decisions]"
    voting: "[consensus preferred, majority if needed]"
    conflicts: "[recusal process for conflicts of interest]"
    documentation: "[all decisions documented with rationale]"
```

### Escalation to Ethics Board

| Trigger | Response Time | Board Action |
|---------|--------------|-------------|
| New high-risk AI system | Next meeting | Review impact assessment, approve/reject |
| Bias incident (SEV-1) | 48 hours | Emergency review, remediation guidance |
| Regulatory inquiry | 48 hours | Review response, advise legal |
| Novel use case (no precedent) | Next meeting | Ethical assessment, set precedent |
| Employee/public ethical concern | 2 weeks | Investigate, recommend action |
| Annual program review | Scheduled | Comprehensive governance health check |

---

## Phase 10: Monitoring & Continuous Governance

### AI Governance Dashboard YAML

```yaml
dashboard:
  period: "[month]"
  
  inventory_health:
    total_ai_systems: [count]
    fully_documented: [count]
    impact_assessments_current: [count]
    overdue_reviews: [count]
    
  compliance_status:
    high_risk_systems: [count]
    fully_compliant: [count]
    gaps_identified: [count]
    remediation_in_progress: [count]
    
  fairness:
    systems_with_active_monitoring: [count]
    bias_incidents_this_period: [count]
    open_bias_remediation: [count]
    
  incidents:
    total_ai_incidents: [count]
    sev1: [count]
    mean_time_to_contain: "[hours]"
    post_mortems_completed: [count]
    
  transparency:
    model_cards_published: "[X of Y]"
    user_disclosures_active: "[X of Y]"
    explanation_requests_fulfilled: [count]
    
  governance_health_score: "[0-100]"
```

### Governance Health Score (0-100)

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| **Inventory completeness** | 15% | % of AI systems documented and classified |
| **Impact assessments** | 20% | % of required assessments completed and current |
| **Bias management** | 20% | % of systems with active fairness monitoring |
| **Transparency** | 15% | % of systems with model cards + user disclosure |
| **Incident readiness** | 15% | Response time + post-mortem completion rate |
| **Policy compliance** | 15% | % of systems meeting all policy requirements |

### Review Cadence

| Activity | Frequency | Owner |
|----------|-----------|-------|
| AI inventory update | Monthly | AI governance team |
| High-risk system monitoring review | Monthly | System owners |
| Bias audit (high-risk) | Quarterly | Data science + ethics |
| Impact assessment refresh | Annually (or on major change) | System owners |
| Policy review | Annually | AI governance + legal |
| Full governance program audit | Annually | AI ethics board |
| Regulatory landscape scan | Quarterly | Legal + compliance |
| AI literacy training refresh | Annually | HR + AI governance |

---

## Phase 11: Generative AI Governance (Special Section)

GenAI introduces unique governance challenges.

### GenAI-Specific Risks

| Risk | Mitigation |
|------|-----------|
| **Hallucination** | Grounding (RAG), fact-checking layers, confidence scoring, human review for high-stakes |
| **Copyright infringement** | Training data provenance, output filtering, indemnification clauses with vendors |
| **Data leakage** | Input sanitization, DLP filters, enterprise deployments (no data retention) |
| **Prompt injection** | Input validation, system prompt hardening, output filtering |
| **Deepfakes/synthetic media** | Watermarking, content provenance (C2PA), detection tools |
| **Over-reliance** | Training on limitations, mandatory human review for decisions |
| **Environmental impact** | Efficiency monitoring, right-sizing models, carbon tracking |

### GenAI Acceptable Use Matrix

| Use Case | Risk Level | Requirements |
|----------|-----------|-------------|
| Internal drafting/brainstorming | Low | No sensitive data input |
| Code generation/review | Medium | Security review of output, no secrets in prompts |
| Customer-facing chatbot | High | Guardrails, monitoring, disclosure, escalation path |
| Content creation (marketing) | Medium | Human review, fact-check, no false claims |
| Decision support (HR/legal) | High | Human-in-loop mandatory, bias testing, audit trail |
| Autonomous agents | Critical | Full governance lifecycle, kill switch, continuous monitoring |
| Synthetic data generation | Medium | Privacy review, quality validation |

### GenAI Vendor Assessment (Additional Questions)

- [ ] Where does input data go? Is it used for training?
- [ ] Can data retention be disabled / custom retention set?
- [ ] What content filtering/safety measures are in place?
- [ ] What is the provider's approach to copyright?
- [ ] Does the provider offer indemnification for AI outputs?
- [ ] Can the model be customized with guardrails/system prompts?
- [ ] What's the provider's incident response for model issues?
- [ ] Is there an enterprise agreement with data processing addendum?

---

## Phase 12: AI Literacy & Culture

### AI Literacy Program Design

| Audience | Content | Duration | Frequency |
|----------|---------|----------|-----------|
| **All employees** | AI basics, AUP, data rules, reporting concerns | 1 hour | Annual + onboarding |
| **Managers** | AI decision-making, oversight responsibilities, bias awareness | 2 hours | Annual |
| **AI/Data teams** | Full governance lifecycle, fairness metrics, documentation standards | 4 hours | Semi-annual |
| **Leadership** | Strategic AI governance, regulatory landscape, risk appetite | 2 hours | Annual |
| **Ethics board** | Deep dives on emerging issues, case studies, framework updates | Ongoing | Monthly reading + quarterly workshop |

### Culture Health Indicators

Positive signals:
- Teams voluntarily register AI experiments early
- Bias concerns raised proactively (not after incidents)
- "Should we use AI for this?" is a normal question
- Impact assessments seen as valuable, not bureaucratic
- Ethics board consulted for edge cases (not avoided)

Warning signals:
- Shadow AI (unregistered systems discovered)
- "Move fast, govern later" attitudes
- Bias testing skipped "because we're in a hurry"
- No questions or concerns raised (silence ≠ compliance)
- Ethics board bypassed for "urgent" deployments

---

## Quality Rubric (0-100)

| Dimension | Weight | 0 | 50 | 100 |
|-----------|--------|---|----|----|
| **Inventory** | 15% | No AI registry | Partial registry | Complete, current, classified |
| **Risk Assessment** | 15% | No impact assessments | Ad-hoc assessments | Systematic, current for all medium+ |
| **Fairness** | 20% | No bias testing | Pre-deploy only | Continuous monitoring + remediation |
| **Transparency** | 15% | No documentation | Model cards for some | Full cards + user disclosure + appeals |
| **Incident Response** | 10% | No AI-specific process | Basic playbook | Tested, exercised, post-mortems |
| **Compliance** | 15% | Unaware of regulations | Partial compliance | Audit-ready, proactive |
| **Culture** | 10% | No AI literacy | Training for AI teams | Organization-wide, proactive reporting |

---

## Edge Cases

### Startup / Small Company
- Start with AI inventory + acceptable use policy — even if informal
- Use this framework scaled down: brief impact assessments, not 50-page documents
- Designate ONE person as AI governance owner (often CTO or Head of Product)
- Focus on customer-facing AI first

### Regulated Industry (Financial Services, Healthcare)
- Layer AI governance ON TOP of existing compliance (don't duplicate)
- Map AI risks to existing risk taxonomy
- Engage sector-specific regulators early (many have AI guidance)
- Consider external AI audits for high-risk systems

### Heavy Third-Party AI Usage
- Vendor assessment is your primary governance tool
- Maintain inventory of ALL vendor AI (including embedded AI in SaaS tools)
- Contractual protections are critical (data use, liability, audit rights)
- Monitor vendor compliance continuously (not just at procurement)

### Rapid AI Adoption / "AI Everywhere" Initiative
- Don't let governance become a bottleneck — tiered approach is key
- Low-risk: fast-track with self-service checklist
- Medium-risk: standard review (1-2 weeks)
- High-risk: full assessment (4-6 weeks)
- Build governance INTO the development process, not as a gate

### Multi-National Operations
- Map regulatory requirements per jurisdiction
- Default to strictest standard (usually EU AI Act)
- Document jurisdiction-specific adaptations
- Consider data localization requirements for AI

### Acquired AI Systems (M&A)
- Immediate AI inventory of acquired entity
- Risk classify all inherited AI systems within 90 days
- Integrate into governance program within 6 months
- Priority: customer-facing and decision-making systems first

---

## Natural Language Commands

1. **"Assess our AI governance maturity"** → Run Phase 1 maturity model, generate scores and priorities
2. **"Classify this AI system"** → Walk through EU AI Act + internal risk tier classification
3. **"Run an AI impact assessment for [system]"** → Generate full AIIA using Phase 3 template
4. **"Draft our AI acceptable use policy"** → Generate AUP using Phase 4 template
5. **"Audit [system] for bias"** → Design and execute bias testing protocol from Phase 5
6. **"Create a model card for [system]"** → Fill Phase 6 model card template
7. **"We had an AI incident"** → Activate Phase 7 incident response playbook
8. **"Map our EU AI Act compliance"** → Run Phase 8 compliance checklist
9. **"Design our AI ethics board"** → Generate charter using Phase 9 template
10. **"Generate our AI governance dashboard"** → Build Phase 10 dashboard with health score
11. **"Review our GenAI policies"** → Audit against Phase 11 GenAI governance framework
12. **"Plan AI literacy training"** → Design program using Phase 12 audience matrix
