# EnvironMentors @ UC Davis — Recruitment Landing Page

Static landing page for the UC Davis EnvironMentors program. Linked from a QR code on the recruitment foam-core board used at outreach events.

Hosted on GitHub Pages. The QR code routes through bit.ly so the destination can be repointed to other pages over time without reprinting the board.

- **Live URL:** https://greymonroe.github.io/environmentors-landing/
- **Form responses:** Google Form (linked from page) feeds a Google Sheet
- **Program site:** https://environmentors.ucdavis.edu/

## Structure

- `index.html` — landing page with the **audience picker** (first thing visitors see)
- `audiences/*.html` — one tailored page per audience (Professor, Postdoc, Grad, Undergrad, Teacher, Parent, HS Student, Donor, Administrator)
- `styles.css` — shared stylesheet
- `photos/` — program photography
- `build_audiences.py` — generator script for the audience pages (regenerate after editing copy or adding an audience)

## Editing audience copy

All 9 audience pages are generated from `build_audiences.py`. To change copy, photos, or add an audience:

1. Edit the `AUDIENCES` list in `build_audiences.py`.
2. Run `python3 build_audiences.py` from the repo root.
3. Commit the regenerated `audiences/*.html` files alongside the script change.

## Form prefill / audience tagging

The Google Form (form ID `1unCGKsg9X34KCKkCYNsnGxXuja2EdPVTBLD-V0zDTpo`) has these fields:

| Field | Entry ID | Required |
|-------|----------|----------|
| Name | `entry.177589650` | yes |
| Email | `entry.442852572` | yes |
| Title | `entry.80698941` | no |
| Department / Affiliation / School | `entry.1107821996` | no |
| I am a… (checkbox, 10 roles) | `entry.33068743` | yes |
| Why are you interested? | `entry.1529740131` | no |

The "I am a…" question carries all 9 site audiences plus Staff: Professor / Faculty, Postdoc, Graduate Student, Undergraduate, Staff, Teacher, Parent / Guardian, High School Student, Donor / Supporter, Administrator / Unit Leader.

Each audience page builds a prefilled form URL that:

- Prefills the **I am a…** checkbox to the matching audience.
- Prefills the **Why are you interested?** field with a tag like `[I'm a High School Teacher]` so the segment is double-tagged in responses.

The form is owned and edited from the `grey-matter` project. To change role options, edit `update_environmentors_form.py` over there and re-run it, then update `KNOWN_ROLES` in `build_audiences.py` to match.
