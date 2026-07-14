# Submission

## Summary of changes

1. Added sorting in the **Active queue** by `customer_tier` and `assigned_reviewer`.
2. Added colour coding for the highest-priority tasks.
3. Improved error handling for resolved and unassigned tasks.
4. Disabled the **Claim** button for already claimed items.
5. Added functionality for the current reviewer to release a claimed item.
6. Added a **Resolved tasks** list.

## Bugs fixed

1. Disabled the **Claim** button for already claimed items.
2. Extended the `active_only` filtering in the `list_review_items` endpoint to exclude all terminal states.
3. Fixed an issue that allowed actions on unassigned items.
4. Fixed an issue that allowed actions on items already in a terminal state.
5. Fixed an issue that allowed users to resolve tasks assigned to other reviewers.

## Product / UX decisions

### 1. Sorting in the Active queue

The Active queue is now sorted by `customer_tier` and `assigned_reviewer`.

* Higher-priority tasks are surfaced first.
* Already assigned tasks are moved below unassigned tasks, making it easier for reviewers to identify work that still needs to be picked up.

### 2. Priority colour coding

High-priority tasks are visually highlighted, allowing reviewers to identify urgent work more quickly.

### 3. Release task functionality

Reviewers can release a claimed task if they are unable to complete it, allowing another reviewer to pick it up.

### 4. Resolved tasks list

A separate list of resolved tasks provides better visibility into completed work and the final resolution of each task.

## Tests added

* `test_unassigned_items_cannot_be_resolved`
* `test_resolved_items_cannot_be_resolved_again`
* `test_assigned_reviewer_can_release_task`
* `test_unassigned_reviewer_cannot_release_task`
* `test_cannot_resolve_other_reviewer_task`

## Known gaps

* The release action currently follows the existing API style and could be further refined.
* Additional end-to-end/frontend tests would be valuable in a production codebase.

## Files changed

### `test_smoke.py`

* Added tests covering new business rules.

### `styles.css`

* Added styling for priority highlighting and UI improvements.

### `api.ts`

* Improved API error handling.
* Added support for the `activeOnly` filter.
* Extended `ReviewAction` with the `release` action.

### `App.vue`

* Updated frontend business logic and UI.

### `main.py`

* Implemented backend business rules and validation.

## AI assistance used

I used Codex to accelerate implementation by generating boilerplate and suggesting code, with all generated code reviewed and adapted by me before being committed.

All product and UX decisions were my own. I intentionally did not use AI to suggest product improvements, as I wanted to demonstrate my own reasoning and prioritisation. In a production environment, I would use AI more extensively during the planning and design phase to explore implementation options before writing code.
