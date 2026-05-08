#!/usr/bin/env python3
"""Generate audience-specific landing pages from a single template.

Run from the repo root:
    python3 build_audiences.py

Outputs into ./audiences/.
"""
from pathlib import Path
from urllib.parse import quote

# Google Form prefill setup
FORM_BASE = "https://docs.google.com/forms/d/e/1FAIpQLSe3fdZ-yH0klDL1bemUlo8f9IML4VVD8XwCSvVxNgeBMHHSXA/viewform"
ROLE_FIELD = "entry.33068743"   # multiple choice
WHY_FIELD = "entry.1529740131"  # paragraph

# Roles available in the form's "I am a…" question (kept in sync with update_environmentors_form.py)
KNOWN_ROLES = {
    "Professor / Faculty", "Postdoc", "Graduate Student", "Undergraduate", "Staff",
    "Teacher", "Parent / Guardian", "High School Student",
    "Donor / Supporter", "Administrator / Unit Leader",
}

AUDIENCES = [
    {
        "slug": "professor",
        "label": "Professor",
        "eyebrow": "For UC Davis faculty",
        "tag": "Professor / Faculty PI",
        "role": "Professor / Faculty",
        "hero_photo": "poster-mentor.jpg",
        "side_photo": "lab-team.jpg",
        "h1_html": "Help a high schooler<br><span class=\"hilite\">do real research.</span>",
        "lede": "EnvironMentors pairs UC Davis labs with Sacramento-area high school students for a year of mentored environmental research. Most pairings run through a grad student or postdoc in the lab.",
        "body_h2": "How a lab actually plugs in.",
        "body": [
            "We match Sacramento-area high schoolers with UC Davis mentors each fall. They scope a research project they pick, meet with their mentor every other week, and present at the UC Davis Science Fair in spring. A top cohort flies to the GCSE International Science Fair as a group.",
            "From a PI seat, the most common arrangement is putting a grad student or postdoc forward as the mentor. It's the kind of structured, year-long teaching experience that's hard for them to get otherwise, and it shows up well in faculty applications, teaching statements, and chalk talk Q&amp;A.",
            "If you have NSF, USDA, or NIH broader-impact obligations, the program documentation slots into reports cleanly. We can help with that. But the actual reason most PIs stay involved year after year is the work itself.",
        ],
        "cards": [
            ("Lab leadership", "Your grad student or postdoc gets to run their own mentee for a school year. They'll be better for it."),
            ("A real partner", "We're a chapter of a national program. Mentees come pre-screened and ready to work."),
        ],
    },
    {
        "slug": "postdoc",
        "label": "Postdoc",
        "eyebrow": "For postdoctoral researchers",
        "tag": "Postdoc",
        "role": "Postdoc",
        "hero_photo": "lab-team.jpg",
        "side_photo": "poster-mentor.jpg",
        "h1_html": "Mentorship that's<br><span class=\"hilite\">actually mentorship.</span>",
        "lede": "Take on a one-on-one mentee for the school year. Structured, scoped, and built around the academic calendar.",
        "body_h2": "What a year of this looks like.",
        "body": [
            "You're paired with a Sacramento-area high school student. You meet every other week, help them frame a research question they actually care about, and walk them through designing it, running it, and presenting at the UC Davis Science Fair in May.",
            "It does what 'mentorship' on a CV is supposed to do: gives you something specific to write about in a teaching statement and something concrete a search committee can ask you about. After a year you'll have shepherded someone through their first independent research project, and you'll know exactly how that went.",
            "Summer is yours. Your PI just needs to be on board; most happily are.",
        ],
        "cards": [
            ("On the application", "Concrete teaching and mentorship to point to. Not just 'helped train an undergrad.'"),
            ("Time commitment", "Bi-weekly mentee meetings, a few hours a month of project support. September to May."),
        ],
    },
    {
        "slug": "grad",
        "label": "UC Davis Grad Student",
        "eyebrow": "For UC Davis grad students",
        "tag": "UC Davis Graduate Student",
        "role": "Graduate Student",
        "hero_photo": "lab-team.jpg",
        "side_photo": "lab-science.jpg",
        "h1_html": "Be the mentor<br><span class=\"hilite\">you wish you'd had.</span>",
        "lede": "Spend a school year guiding a high schooler through their first real research project.",
        "body_h2": "The shape of it.",
        "body": [
            "EnvironMentors matches you 1:1 with a Sacramento-area high school student. You meet every other week, help them frame a question they care about, and walk with them through designing it, running it, and presenting at the UC Davis Science Fair.",
            "The structure is built so you can do this well without it eating your dissertation. The calendar lines up with the school year — September to May, with summer fully off.",
            "PIs are usually for it. Lab broader-impact lift, no real time hit on the research, and a credential their grad student can put on the academic job market.",
        ],
        "cards": [
            ("What you do", "Frame the question. Help them scope it. Meet bi-weekly. Show up at the fair in May."),
            ("What you get", "A year-long teaching credential and a reference letter that's specific."),
        ],
    },
    {
        "slug": "undergrad",
        "label": "UC Davis Undergrad",
        "eyebrow": "For UC Davis undergraduates",
        "tag": "UC Davis Undergraduate",
        "role": "Undergraduate",
        "hero_photo": "greenhouse.jpg",
        "side_photo": "lab-science.jpg",
        "h1_html": "Lead a year-long<br><span class=\"hilite\">mentorship.</span>",
        "lede": "Advanced undergrads in a UC Davis lab can mentor a high schooler through their own environmental research project.",
        "body_h2": "Where you fit.",
        "body": [
            "If you're already in a UC Davis lab and your PI is on board, we'll pair you with a Sacramento-area high school student for the school year. You're the guide — not a co-pilot.",
            "It works because you remember what high school felt like better than your PI does. You're closer to the gap your mentee is looking up at than anyone else in the lab.",
            "You'll meet every other week, help them scope a project they can actually finish, and walk them through running it. The fair is in May, summer is off.",
        ],
        "cards": [
            ("On grad applications", "Year-long mentorship evidence is rare on undergraduate applications. Reviewers notice."),
            ("What it asks", "Bi-weekly meetings, project support during the school year, fair day in May."),
        ],
    },
    {
        "slug": "teacher",
        "label": "Teacher",
        "eyebrow": "For high school teachers",
        "tag": "High School Teacher",
        "role": "Teacher",
        "hero_photo": "presenting.jpg",
        "side_photo": "award.jpg",
        "h1_html": "Pair your students with<br><span class=\"hilite\">a UC Davis scientist.</span>",
        "lede": "Free, year-long, one-on-one environmental research mentorship for your students. We do the heavy lifting.",
        "body_h2": "How the partnership works.",
        "body": [
            "We work with high schools across the Sacramento region. You nominate students. We pair them with UC Davis researchers, and the pair runs an environmental research project together — meeting every other week, presenting at the UC Davis Science Fair in May.",
            "At many schools, the project counts toward independent-study credit. We can talk through how that gets set up at yours.",
            "It's free for your students and your school. Funding comes from the UC Davis Foundation, federal sponsors, and donors.",
        ],
        "cards": [
            ("What we handle", "Mentor recruiting, project scaffolding, fair registration, travel for the international fair."),
            ("What you do", "Nominate the students. Help them stay on track during the school day."),
        ],
    },
    {
        "slug": "parent",
        "label": "Parent",
        "eyebrow": "For parents and guardians",
        "tag": "Parent / Guardian",
        "role": "Parent / Guardian",
        "hero_photo": "award.jpg",
        "side_photo": "presenting.jpg",
        "h1_html": "Your high schooler's<br><span class=\"hilite\">first real research project.</span>",
        "lede": "Free, year-long, one-on-one mentorship from a UC Davis scientist.",
        "body_h2": "What this is, plainly.",
        "body": [
            "EnvironMentors is for high school students who want to actually do science, not just read about it. Your student gets paired with a UC Davis grad student, postdoc, or faculty member who works alongside them for the school year.",
            "They pick the project — water quality, ecology, climate, food access, whatever they're curious about. Their mentor helps them scope it so it's doable in a school year, then meets with them every other week to keep it moving. In spring they present at the UC Davis Science Fair.",
            "There's no cost. We work with the high school directly. The strongest projects each year travel to the GCSE International Science Fair as a cohort, fully covered.",
        ],
        "cards": [
            ("Free", "Funded through the UC Davis Foundation. No cost to families or schools."),
            ("On college apps", "A real research portfolio item with a UC Davis mentor as a reference."),
        ],
    },
    {
        "slug": "hs-student",
        "label": "High School Student",
        "eyebrow": "For high school students",
        "tag": "High School Student",
        "role": "High School Student",
        "hero_photo": "group-fair.jpg",
        "side_photo": "farm.jpg",
        "h1_html": "Pick a question.<br><span class=\"hilite\">Run a real research project.</span>",
        "lede": "A UC Davis scientist mentors you one-on-one for a year. You design the project. You run it. You present it.",
        "body_h2": "What you'd actually do.",
        "body": [
            "This is your project. You pick the question — climate change, water quality in Putah Creek, an invasive plant in your neighborhood, food access in your zip code, whatever you actually want to look into. Your mentor helps you scope it so you can finish it.",
            "You meet with your mentor every other week from fall to spring. They're a grad student, postdoc, or faculty member at UC Davis. Their job is to help you do real science.",
            "In May you present at the UC Davis Science Fair. The strongest projects each year fly to the GCSE International Science Fair as a group. You meet kids from chapters across the country who've been doing the same thing.",
        ],
        "cards": [
            ("Yours, not assigned", "You pick the question. The project is yours."),
            ("Real mentor", "Someone in your corner who actually does this for a living."),
        ],
    },
    {
        "slug": "donor",
        "label": "Donor",
        "eyebrow": "Support EnvironMentors",
        "tag": "Donor",
        "role": "Donor / Supporter",
        "hero_photo": "award.jpg",
        "side_photo": "group-fair.jpg",
        "h1_html": "Fund a year of research<br><span class=\"hilite\">for a young scientist.</span>",
        "lede": "Donations through the UC Davis Foundation go directly to mentee stipends, fair travel, and project supplies.",
        "body_h2": "Where the money goes.",
        "body": [
            "Every dollar lands on a mentee. Stipends, lab supplies, fair registration, travel to the international fair. Operating overhead is absorbed by the university.",
            "Naming and recognition are available at several levels — sponsoring an individual mentor pairing, a fair, or a travel cohort. Reach out and we'll send the gift instrument that fits.",
            "We're set up for corporate and family foundation partnerships too. Other GCSE chapters have had multi-year sponsorships that transformed what they could do.",
        ],
        "cards": [
            ("Where it goes", "Mentees, supplies, fair travel. The university covers the rest."),
            ("Tax status", "Tax-deductible through the UC Davis Foundation."),
        ],
    },
    {
        "slug": "administrator",
        "label": "Administrator",
        "eyebrow": "For department and unit leaders",
        "tag": "Administrator / Unit Leader",
        "role": "Administrator / Unit Leader",
        "hero_photo": "arboretum.jpg",
        "side_photo": "campus.jpg",
        "h1_html": "A K-12 outreach program<br><span class=\"hilite\">your faculty will actually use.</span>",
        "lede": "EnvironMentors at UC Davis is a chapter of the national GCSE program. We can plug in at the lab, department, or college level.",
        "body_h2": "How it slots in.",
        "body": [
            "Faculty across UC Davis use EnvironMentors to put their grad students and postdocs into year-long mentorship pairings with Sacramento-area high schoolers. Because there's already a curriculum, a fair, and a national network, faculty don't have to build anything from scratch.",
            "From an admin seat that means real K-12 outreach numbers, a defensible answer when accreditation reviews ask about community engagement, and a partner you can put on broader-impact letters of support.",
            "We can be a per-PI broader-impact partner, a unit-wide outreach line, or a co-sponsored initiative with shared branding. Any of the three works.",
        ],
        "cards": [
            ("Three plug-in models", "Per-PI partner, unit-wide line, or co-sponsored initiative with shared branding."),
            ("Reporting", "Mentee participation and project outcomes documented for federal and accreditation reporting."),
        ],
    },
]


def build_form_url(audience):
    why_seed = f"[I'm a {audience['tag']}] "
    parts = [f"embedded=true", "usp=pp_url", f"{WHY_FIELD}={quote(why_seed)}"]
    if audience["role"] and audience["role"] in KNOWN_ROLES:
        parts.append(f"{ROLE_FIELD}={quote(audience['role'])}")
    return f"{FORM_BASE}?" + "&".join(parts)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EnvironMentors at UC Davis — {label}</title>
<meta name="description" content="EnvironMentors at UC Davis · {eyebrow}. Year-long, 1:1 environmental research mentorship.">
<meta property="og:title" content="EnvironMentors at UC Davis — {label}">
<meta property="og:description" content="{lede}">
<meta property="og:image" content="../photos/{hero_photo}">
<link rel="stylesheet" href="../styles.css">
</head>
<body>

<div class="topbar">
  UC Davis EnvironMentors <span class="dot">·</span> <a href="https://environmentors.ucdavis.edu/">environmentors.ucdavis.edu</a>
</div>

<section class="aud-hero" style="background-image: url('../photos/{hero_photo}');">
  <div class="aud-hero-inner">
    <a class="back-link" href="../index.html">← Back · Choose a different role</a>
    <span class="eyebrow" style="margin-top:18px">{eyebrow}</span>
    <h1>{h1_html}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="body-section">
  <h2>{body_h2}</h2>
{body_paragraphs}
</section>

<section class="two-up">
  <div class="two-up-grid">
{cards_html}
  </div>
</section>

<section class="gallery" aria-label="Photo gallery">
  <div class="tile t1" style="background-image:url('../photos/{hero_photo}')" role="img" aria-label="EnvironMentors program photo"></div>
  <div class="tile t2" style="background-image:url('../photos/{side_photo}')" role="img" aria-label="EnvironMentors program photo"></div>
  <div class="tile t3" style="background-image:url('../photos/group-fair.jpg')" role="img" aria-label="EnvironMentors cohort"></div>
  <div class="tile t4" style="background-image:url('../photos/award.jpg')" role="img" aria-label="Award ceremony"></div>
  <div class="tile t5" style="background-image:url('../photos/farm.jpg')" role="img" aria-label="UC Davis student farm"></div>
  <div class="tile t6" style="background-image:url('../photos/lab-science.jpg')" role="img" aria-label="Student in the lab"></div>
  <div class="tile t7" style="background-image:url('../photos/arboretum.jpg')" role="img" aria-label="UC Davis Arboretum"></div>
</section>

<section class="form-section" id="learn-more">
  <div class="form-wrap">
    <div class="kicker">Learn more</div>
    <h2>Drop your info — we'll be in touch.</h2>
    <div class="form-frame">
      <iframe src="{form_url}" height="1100" frameborder="0">Loading…</iframe>
    </div>
  </div>
</section>

<footer>
  <div class="seal">UC Davis EnvironMentors</div>
  <div>A chapter of <a href="https://gcseglobal.org/">GCSE Global</a> · <a href="https://environmentors.ucdavis.edu/">environmentors.ucdavis.edu</a> · <a href="../index.html">All audiences</a></div>
</footer>

</body>
</html>
"""


def render_paragraphs(paragraphs):
    return "\n".join(f"  <p>{p}</p>" for p in paragraphs)


def render_cards(cards):
    out = []
    for h, p in cards:
        out.append(f'    <div class="two-up-card">\n      <h3>{h}</h3>\n      <p>{p}</p>\n    </div>')
    return "\n".join(out)


def main():
    out_dir = Path(__file__).parent / "audiences"
    out_dir.mkdir(exist_ok=True)
    for a in AUDIENCES:
        html = PAGE_TEMPLATE.format(
            label=a["label"],
            eyebrow=a["eyebrow"],
            tag=a["tag"],
            hero_photo=a["hero_photo"],
            side_photo=a["side_photo"],
            h1_html=a["h1_html"],
            lede=a["lede"],
            body_h2=a["body_h2"],
            body_paragraphs=render_paragraphs(a["body"]),
            cards_html=render_cards(a["cards"]),
            form_url=build_form_url(a),
        )
        target = out_dir / f"{a['slug']}.html"
        target.write_text(html)
        print(f"wrote {target}")


if __name__ == "__main__":
    main()
