# 📝 Notes App — Core Domain Specification

_(No technical details — domain models & business logic only)_

---

## 1️⃣ Purpose of the System

The Notes App is a **personal information management system** that allows users to:

- capture ideas, tasks, and information
- organize notes meaningfully
- retrieve notes quickly using filters and search
- manage the lifecycle of notes from creation to archival

The system is **private by default** — every user owns and manages their own data.

---

## 2️⃣ Core Domain Models

### 🔹 User

A **User** represents a single individual using the system.

A user:

- owns notes
- owns tags
- can only view and modify their own data

**Rules**:

- Users are isolated from each other
- No user can access another user’s notes or tags

---

### 🔹 Note

A **Note** is the primary unit of information.

A note:

- belongs to exactly one user
- represents an idea, task, reminder, or reference
- may be simple or detailed

A note contains:

- a title (short summary)
- optional content (details)
- a status (lifecycle state)
- optional tags

---

### 🔹 Note Status (Lifecycle)

Each note exists in **one lifecycle state at a time**:

1. **Todo**
   - active
   - requires attention or action

2. **Done**
   - completed
   - kept for reference

3. **Archived**
   - inactive
   - retained for history

**Rules**:

- Status reflects progress, not deletion
- A note must always have exactly one status

---

### 🔹 Tag

A **Tag** is a reusable label created by a user to describe notes.

A tag:

- belongs to one user
- can be attached to multiple notes
- represents a theme, topic, or context

Examples:

- work
- personal
- urgent
- learning
- finance

**Purpose**:

- organization
- filtering
- mental categorization

---

### 🔹 Note–Tag Relationship

- A note may have zero or more tags
- A tag may be linked to multiple notes
- Tags do not change note content or status

Tags are **descriptive only**, not behavioral.

---

## 3️⃣ Core Behaviors (Business Logic)

### 🧾 Creating Notes

- A user can create a note at any time
- Every new note starts in the **Todo** state
- Tags may be added during or after creation

---

### ✏️ Updating Notes

A user can:

- edit the title
- edit the content
- change the note’s status
- add or remove tags

---

### 🗑️ Deleting Notes (Soft Delete)

- Deleting a note hides it from normal usage
- Deleted notes:
  - are not visible
  - are not searchable
  - still exist internally

**Rule**:

- Deletion does not permanently remove the note

---

### 🔍 Viewing Notes

Users can:

- view a list of notes
- view a single note

Only **non-deleted** notes are visible.

---

### 🔎 Searching & Filtering Notes

Users can:

- filter notes by status
- filter notes by tag
- search notes by keywords
- combine filters

**Rules**:

- Results always include only the user’s own notes
- Deleted notes never appear

---

## 4️⃣ Tag Rules

- Tags are user-specific
- Tag names must be unique per user
- Different users may use the same tag name
- Removing a tag:
  - removes it from notes
  - does not delete notes

---

## 5️⃣ What the System Does NOT Do

- No sharing between users
- No global tags
- No hard deletion by default
- No automatic categorization
- No version history

---

## 6️⃣ System Invariants (Always True)

- Every note has exactly one owner
- A user only sees their own notes
- A note has exactly one status
- Deleted notes are never returned
- Tags do not affect note lifecycle

---

## 7️⃣ One‑Line Mental Model

> A private notebook where each user manages notes that move through a lifecycle and can be labeled with reusable tags for organization and retrieval.
