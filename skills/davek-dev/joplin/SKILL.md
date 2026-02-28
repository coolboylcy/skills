---
name: joplin
description: Interact with Joplin notes via CLI. Use for reading, creating, editing notes and managing todos. Supports WebDAV sync and kanban-formatted notes.
---

# Joplin CLI Skill

Use `joplin` CLI to interact with Joplin notes.

## ⚠️ Important: Use CLI, Not SQL

**Always use the `joplin` CLI for editing notes.** Do not modify the SQLite database directly unless absolutely necessary. Direct database edits can cause sync conflicts and data loss.

## Setup

If Joplin is not configured with WebDAV, configure it:

```bash
joplin config sync.target 6
joplin config sync.6.path "https://your-webdav-server/path"
joplin config sync.6.username "your-username"
joplin config sync.6.password "your-password"
joplin sync
```

## Common Commands

### List Notebooks and Notes
```bash
joplin ls                          # List notebooks
joplin ls "Notebook Name"          # List notes in a notebook
joplin status                      # Show sync status and note counts
```

### Read Note
```bash
joplin cat <note-id>               # Display note content
joplin cat "Note Title"            # Also works with title
joplin note <note-id>              # Open note in editor
```

### Create Note
```bash
joplin mknote "Note Title"         # Create note in default notebook
joplin mknote "Note Title" --notebook "Notebook Name"
joplin mkbook "New Notebook"       # Create new notebook
```

### Edit Note
```bash
joplin edit --note <note-id>       # Edit note in editor
```

### Delete Note
```bash
joplin rmnote <note-id>            # Delete note
joplin rmbook "Notebook Name"      # Delete notebook
```

### Todos
```bash
joplin todos                       # List all todos
joplin todo <note-id>              # Toggle todo status
joplin done <note-id>              # Mark as done
joplin undone <note-id>            # Mark as not done
```

### Sync
```bash
joplin sync                        # Sync with WebDAV server
```

### Export
```bash
joplin export <note-id> --format md
joplin export <note-id> --format html
joplin export <note-id> --format pdf
```

### Search

Note: `joplin search` is only available in GUI mode. Use `joplin ls` and pipe to grep instead.

## Kanban Notes (YesYouKan Plugin)

Some notebooks use the YesYouKan kanban plugin for visual kanban boards. These notes have a specific format that **must be preserved** when editing:

### Kanban Format

```markdown
# Notebook Name

# Backlog

## Task 1

Description here

## Task 2



# In progress

## Another Task

Details



# Done

## Completed Task

Result

```kanban-settings
# Do not remove this block
```
```

### ⚠️ Kanban Formatting Rules

1. **Always include the kanban-settings block** at the end of the note with the exact format:
   ```
   ```kanban-settings
   # Do not remove this block
   ```
   ```

2. **Use `##` for task headings** (not `#`)

3. **Keep column headings** as `# Backlog`, `# In progress`, `# Done`

4. **Preserve blank lines** between tasks — these are visible in the kanban view

5. **After editing a kanban note, always run `joplin sync`** to upload changes

6. **Verify changes with `joplin cat <note-id>`** to ensure formatting is correct

### Moving Tasks Between Columns

When moving a task, simply move the `##` task section from one column to another.
