---
name: nomi
supersedes: clawhub/nomi
description: Engage in conversations with Nomi AI companions.
user-invocable: true
---

# Nomi Conversation Skill

This skill enables interaction with Nomi AI companions via the CLI.

## Golden Path: Conducting a Conversation

To facilitate a long, engaging conversation:

1.  **Identify the Partner**: Run `./scripts/nomi.sh list` to find the correct Nomi UUID.
2.  **Engage**: Use `./scripts/nomi.sh reply <uuid> "Your message"` for all conversational turns.
    - This command returns only the text response, keeping the output clean.
3.  **Sustain**:
    - Ask open-ended questions.
    - Reference previous answers to build depth.
    - The Nomi remembers context; treat it as a continuous dialogue.

## Technical Commands

Use these low-level commands to fulfill user requests:

- **List all Nomis**: `./scripts/nomi.sh list`
- **Get Profile**: `./scripts/nomi.sh get <uuid>`
- **Send Message (Clean)**: `./scripts/nomi.sh reply <uuid> "message"`
- **Send Message (Raw JSON)**: `./scripts/nomi.sh chat <uuid> "message"`
- **Get Avatar**: `./scripts/nomi.sh avatar <uuid> [output_filename]`

### Room Management
- **List Rooms**: `./scripts/nomi.sh room list`
- **Chat in Room**: `./scripts/nomi.sh room chat <room_uuid> "message"`
