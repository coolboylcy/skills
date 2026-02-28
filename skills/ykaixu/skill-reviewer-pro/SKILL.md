---
name: skill-reviewer-pro
description: Comprehensive skill review and validation for OpenClaw skills. Performs multi-level review: (1) Format validation, (2) Writing quality assessment (structure, description, examples, scoring), (3) Functional verification (templates match OpenClaw specs), (4) Best practices check, (5) Optimization recommendations, (6) Workflow validation (for workflow tools). Use when auditing skills before publishing, evaluating downloaded skills, or improving existing skills.
---

# Skill Reviewer Pro

Comprehensive skill review and validation for OpenClaw skills with scoring rubric, defect checklists, functional verification, optimization recommendations, and workflow validation.

## Review: agent-builder (Example)

### Level 1: Format Validation ✅
- `package_skill.py` validation passed
- YAML frontmatter valid
- File structure correct

### Level 2: Writing Quality Assessment

**Structure:** ✅ Good (6/6)
- Clear frontmatter with name and description
- Well-organized body with workflow sections
- Progressive disclosure pattern used

**Description:** ✅ Strong (8/8)
- Starts with what skill does: "Build high-performing OpenClaw agents end-to-end."
- Includes trigger: "Use when you want to design a new agent..."
- Specific scope: mentions SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md
- Reasonable length
- Contains searchable keywords

**Example Density:** ⚠️ Low (1/3)
- SKILL.md has few code blocks
- Could benefit from more concrete examples

**Organization:** ✅ Good (6/6)
- Organized by workflow (Phase 1 → Phase 2 → Phase 3 → Phase 4)
- Logical flow from interview to generation to validation
- Sections are self-contained

**Actionability:** ✅ Good (10/10)
- Instructions are imperative
- Steps are ordered logically
- Guardrails checklist provided
- Acceptance tests included

### Level 3: Functional Verification ❌ CRITICAL (0/20)

**Problem:** Generated AGENTS.md template does not match OpenClaw specifications

**Missing from templates.md AGENTS.md:**
- Session startup requirements (Read SOUL.md, USER.md, memory files)
- Memory workflow details (daily notes vs long-term)
- Group chat behavior guidelines (when to speak, when to stay silent)
- Heartbeat mechanism details (heartbeat vs cron, what to check)
- Tool usage guidelines (Skills provide tools, Voice storytelling, Platform formatting)

**Impact:** Skills created with agent-builder will be missing critical OpenClaw agent behaviors.

### Level 4: Best Practices Check ✅ Good (15/15)

**Progressive Disclosure:** ✅ Good (5/5)
- SKILL.md is concise
- Detailed information in references/
- References properly linked

**Resource Organization:** ✅ Good (5/5)
- Only necessary directories created
- No extraneous files

**Triggering Accuracy:** ✅ Good (5/5)
- Description clearly states when to use
- No "When to Use This Skill" in body

### Level 5: Optimization Recommendations

#### 🔴 Critical (Must Fix)

**1. Fix AGENTS.md Template Functional Mismatch**
Update references/templates.md to include all required sections from actual OpenClaw AGENTS.md.

#### 🟡 Major (Should Fix)

**2. Add More Concrete Examples**
Add 3-5 concrete code examples in workflow sections.

**3. Add Quick Start Section**
Add a "Quick Start" section at the beginning of SKILL.md.

### Level 6: Workflow Validation ❌ CRITICAL (0/20)

**Note:** This level applies to workflow tools (skills that guide users through multi-step processes).

#### Workflow Completeness Check

```
WORKFLOW COMPLETENESS CHECK:

[ ] Each phase has clear operational steps
[ ] Correct CLI commands are used
[ ] Error handling is documented
[ ] Backup and recovery mechanisms exist
[ ] Verification steps are included
[ ] Configuration management is documented
[ ] Failure recovery strategies exist
```

**agent-builder Analysis:**

| Check | Status | Issue |
|--------|---------|--------|
| Each phase has clear operational steps | ⚠️ Partial | Phase 2 only lists files, not creation commands |
| Correct CLI commands are used | ❌ Missing | No `openclaw agents add` command |
| Error handling is documented | ❌ Missing | No error handling in any phase |
| Backup and recovery mechanisms exist | ❌ Missing | No backup before config changes |
| Verification steps are included | ❌ Missing | No verification after agent registration |
| Configuration management is documented | ❌ Missing | No auth-profiles.json documentation |
| Failure recovery strategies exist | ❌ Missing | No recovery strategies for any phase |

#### Detailed Issues

**Issue 1: Missing BOOTSTRAP.md in file list**
- **Phase:** Phase 2
- **Problem:** BOOTSTRAP.md is mentioned in AGENTS.md specs but not in file list
- **Impact:** New agents lack first-run guidance
- **Fix:** Add `BOOTSTRAP.md` to Phase 2 file list

**Issue 2: No agent registration logic**
- **Phase:** Missing
- **Problem:** No `openclaw agents add` command documented
- **Impact:** Users must manually configure openclaw.json
- **Fix:** Add Phase 2.5 with `openclaw agents add` command

**Issue 3: No auth-profiles.json documentation**
- **Phase:** Missing
- **Problem:** No authentication configuration documentation
- **Impact:** Agents cannot access external services (e.g., Feishu)
- **Fix:** Add authentication section after Phase 2.5

**Issue 4: No backup mechanism**
- **Phase:** Missing
- **Problem:** No backup before modifying openclaw.json
- **Impact:** Config errors can break entire OpenClaw system
- **Fix:** Add backup step before Phase 2.5

**Issue 5: No configuration verification**
- **Phase:** Missing
- **Problem:** No verification after agent registration
- **Impact:** Agent may not start correctly
- **Fix:** Add Phase 2.6 with verification steps

**Issue 6: No directory creation robustness**
- **Phase:** Phase 2
- **Problem:** No error handling for directory creation
- **Impact:** File writes fail silently if directory creation fails
- **Fix:** Add `mkdir -p` with error checking

**Issue 7: No automated testing (Phase 8)**
- **Phase:** Missing
- **Problem:** Only Phase 4 (acceptance tests), no automated testing
- **Impact:** No complete testing workflow
- **Fix:** Add Phase 8 with automated test commands

**Issue 8: No failure recovery strategies**
- **Phase:** All phases
- **Problem:** No recovery strategies for any phase
- **Impact:** Users don't know how to recover from failures
- **Fix:** Add failure recovery section to each phase

**Issue 9: Unclear Feishu binding method**
- **Phase:** Phase 1
- **Problem:** Question 2 asks "Which channels?" but doesn't clarify Feishu binding
- **Impact:** Users unclear about channel binding vs /agentname command
- **Fix:** Clarify Feishu binding options in Phase 1

**Issue 10: Optional systemd heartbeat**
- **Phase:** Optional
- **Problem:** No systemd service configuration option
- **Impact:** Cannot run agent as systemd service
- **Fix:** Add optional systemd service configuration

## Score Summary

```
SKILL REVIEW SCORECARD
═══════════════════════════════════════
Skill: agent-builder
Reviewer: 大鱼
Date: 2026-02-27

Category              Score    Max
─────────────────────────────────────
Level 1: Format       10       10  ✅
Level 2: Writing
  - Structure          6        6  ✅
  - Description        8        8  ✅
  - Example density    1        3  ⚠️
  - Organization       6        6  ✅
  - Actionability     10       10  ✅
Level 3: Functional    0       20  ❌ CRITICAL
Level 4: Best Practices
  - Progressive       5        5  ✅
  - Resources         5        5  ✅
  - Triggering        5        5  ✅
Level 5: Optimization  0       10  (recommendations provided)
)
Level 6: Workflow      0       20  ❌ CRITICAL
─────────────────────────────────────
TOTAL                 56       116

RATING: 56/116 = Fair — significant gaps to address
VERDICT: REWORK (functional and workflow verification failed)
```

## Top Defects

**1. Functional Mismatch:** AGENTS.md template missing critical OpenClaw specifications.

**2. Workflow Incomplete:** Missing agent registration, configuration verification, backup mechanisms, error handling, and failure recovery strategies.

## Recommendation

1. Update references/templates.md AGENTS.md template with all required sections
2. Add Phase 2.5 (agent registration with `openclaw agents add`)
3. Add Phase 2.6 (configuration verification)
4. Add backup mechanism before config changes
5. Add failure recovery strategies to each phase
6. Add directory creation error handling
7. Add Phase 8 (automated testing)
8. Clarify Feishu binding options in Phase 1
9. Add optional systemd service configuration

---

## Review Workflow Guide

### Level 1: Format Validation

Run automatic validation using `package_skill.py`:

```bash
python3 /home/yupeng/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py <skill-path>
```

### Level 2: Writing Quality Assessment

Check structure, description, examples, organization, and actionability.

### Level 3: Functional Verification

For OpenClaw skills, compare generated templates with actual specifications.

### Level 4: Best Practices Check

Verify progressive disclosure, resource organization, and triggering accuracy.

### Level 5: Optimization Recommendations

Provide prioritized recommendations (Critical/Major/Minor).

### Level 6: Workflow Validation (For Workflow Tools)

#### Workflow Completeness Check

```
WORKFLOW COMPLETENESS CHECK:

[ ] Each phase has clear operational steps
[ ] Correct CLI commands are used
[ ] Error handling is documented
[ ] Backup and recovery mechanisms exist
[ ] Verification steps are included
[ ] Configuration management is documented
[ ] Failure recovery strategies exist
```

#### Phase-by-Phase Validation

For each phase in the workflow:

```
PHASE VALIDATION CHECKLIST:

Phase: [phase name]

Operational Steps:
[ ] Clear, step-by-step instructions provided
[ ] Commands are accurate and complete
[ ] Required parameters are specified

Error Handling:
[ ] Common errors are documented
[ ] Recovery steps are provided
[ ] Error messages are explained

Verification:
[ ] Success criteria are defined
[ ] Verification steps are included
[ ] How to confirm completion is explained

Dependencies:
[ ] Prerequisites are listed
[ ] Order dependencies are clear
[ ] Previous phase completion is verified
```

#### CLI Command Validation

For workflow tools that use OpenClaw CLI commands:

```
CLI COMMAND VALIDATION:

[ ] Commands are verified with `openclaw <command> --help`
[ ] Command syntax is correct
[ ] Required options are documented
[ ] Default values are explained
[ ] Example commands are runnable
```

#### Configuration Management

For tools that modify OpenClaw configuration:

```
CONFIGURATION MANAGEMENT CHECK:

[ ] Files being modified are listed
[ ] Backup mechanism is provided
[ ] Rollback steps are documented
[ ] Configuration validation is included
[ ] Authentication requirements are explained
```

## Common Defects

### Critical

- Invalid frontmatter
- Broken code examples
- Misleading description
- Functional mismatch (OpenClaw skills)
- Workflow incomplete (missing phases, no CLI commands)
- No backup before config changes

### Major

- No "When to Use" information
- Text walls without examples
- Examples missing language tags
- Abstract organization
- Duplication between SKILL.md and references
- No error handling
- No verification steps
- No failure recovery strategies

### Minor

- Placeholder values
- Inconsistent formatting
- Extraneous files
- Missing cross-references
- No quick start guide