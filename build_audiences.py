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
        "eyebrow": "For UC Davis Faculty",
        "tag": "Professor / Faculty PI",
        "role": "Professor / Faculty",
        "hero_photo": "poster-mentor.jpg",
        "side_photo": "lab-team.jpg",
        "h1_html": "Broader impact, <span class=\"hilite\">without inventing a program.</span>",
        "lede": "Plug your lab into EnvironMentors. We deliver the K-12 mentorship; your science provides the substance.",
        "body": [
            "Federal funders (NSF, USDA, DOE, NIH) all require broader-impact deliverables. Most PIs cobble these together with one-off school visits or a YouTube explainer. EnvironMentors gives you a turnkey alternative — a decade-old chapter of a national program — that produces real, documented student research.",
            "Your lab provides a mentor (yourself, a postdoc, a grad student, or an advanced undergrad — your call) and a research thread the mentee can latch onto. We provide the high school student, the curriculum scaffolding, the fair logistics, and the program documentation.",
            "Mentors and mentees meet bi-weekly during the academic year. Summer is free. Show up for your group meetings; the mentee shows up for theirs.",
        ],
        "cards": [
            ("Real broader impact", "Tangible, documentable outputs you can cite in renewals, biosketches, and advancement files."),
            ("Lab credit", "Your grad students and postdocs build mentorship credentials that matter on the job market."),
        ],
    },
    {
        "slug": "postdoc",
        "label": "Postdoc",
        "eyebrow": "For Postdoctoral Researchers",
        "tag": "Postdoc",
        "role": "Postdoc",
        "hero_photo": "lab-team.jpg",
        "side_photo": "poster-mentor.jpg",
        "h1_html": "Mentorship is on the application. <span class=\"hilite\">Make it real.</span>",
        "lede": "A year-long, structured 1:1 mentorship credential that search committees actually weight.",
        "body": [
            "Most postdocs claim mentorship experience on faculty applications. Few have something formal to point to. EnvironMentors gives you a documented, year-long, 1:1 mentee relationship with a clear deliverable: their independent research project at the UC Davis Science Fair.",
            "Translating your science to a high schooler clarifies your own thinking — the same forcing function that makes you better at chalk talks and grant statements.",
            "Bi-weekly meetings during the academic year, summer free. Built around your existing schedule, not on top of it.",
        ],
        "cards": [
            ("Faculty job market", "Real teaching and mentorship evidence for your statement of teaching and reference letters."),
            ("Broader impact", "Document it for your next K-award, NSF proposal, or postdoc fellowship application."),
        ],
    },
    {
        "slug": "grad",
        "label": "UC Davis Grad Student",
        "eyebrow": "For Graduate Students at UC Davis",
        "tag": "UC Davis Graduate Student",
        "role": "Graduate Student",
        "hero_photo": "lab-team.jpg",
        "side_photo": "lab-science.jpg",
        "h1_html": "Be the mentor <span class=\"hilite\">you needed.</span>",
        "lede": "A year-long mentorship that strengthens your science, your CV, and somebody's whole trajectory.",
        "body": [
            "You wanted to do science before anyone walked you through how. EnvironMentors lets you be that person for a high school student in the Sacramento region — guiding them through a year-long environmental research project they design and own.",
            "It's a real teaching credential — the kind that means something on faculty applications, NSF GRFP renewals, and the teaching statement you'll be writing in five years.",
            "Bi-weekly meetings. Project scaled to fit your time. Summer free.",
        ],
        "cards": [
            ("Real teaching", "Documented year-long mentorship for the academic job market or research-track careers."),
            ("Better science", "Explaining your work to a high schooler is a forcing function on clarity. Your committee will notice."),
        ],
    },
    {
        "slug": "undergrad",
        "label": "UC Davis Undergrad",
        "eyebrow": "For UC Davis Undergraduates",
        "tag": "UC Davis Undergraduate",
        "role": "Undergraduate",
        "hero_photo": "greenhouse.jpg",
        "side_photo": "lab-science.jpg",
        "h1_html": "Lead a research project — <span class=\"hilite\">from the mentor side.</span>",
        "lede": "Build the mentorship credential that lifts grad school applications. One year, one mentee.",
        "body": [
            "Advanced undergrads are eligible to mentor. If you're working in a UC Davis lab and ready to take more ownership, EnvironMentors pairs you with a high school student for a year and gives you the structure to lead them.",
            "It works because you're closer to the gap they're looking up at than anyone else. You remember high school.",
            "Bi-weekly meetings, summer free. Counts as recognized mentorship for grad school personal statements and reference letters.",
        ],
        "cards": [
            ("Grad app boost", "Genuine year-long mentorship evidence — rare and credible in undergrad applications."),
            ("Lab credit", "Your PI gets broader-impact lift; your CV gets a documented program credential."),
        ],
    },
    {
        "slug": "teacher",
        "label": "Teacher",
        "eyebrow": "For High School Teachers",
        "tag": "High School Teacher",
        "role": "Teacher",
        "hero_photo": "presenting.jpg",
        "side_photo": "award.jpg",
        "h1_html": "Pair your students with <span class=\"hilite\">a UC Davis scientist.</span>",
        "lede": "Your students get free, year-long, 1-on-1 research mentorship — and a science fair pipeline to a national stage.",
        "body": [
            "We partner with high schools across the Sacramento region. You nominate students; we pair them 1:1 with vetted UC Davis researchers (faculty, postdocs, grad students, or advanced undergrads). The students build research projects that count toward independent-study credit at many schools.",
            "Mentors and mentees meet bi-weekly, work toward the UC Davis Science Fair in spring, and the top cohort travels to the GCSE International Science Fair. We handle the logistics, fair registration, and travel coordination.",
            "It's free for your students and your school. Our funding comes from the UC Davis Foundation, federal sponsors, and individual donors.",
        ],
        "cards": [
            ("No cost to you", "We handle mentor recruiting, scaffolding, fair registration, and travel logistics."),
            ("Real outcomes", "Your students walk away with a research portfolio item and a UC Davis network."),
        ],
    },
    {
        "slug": "parent",
        "label": "Parent",
        "eyebrow": "For Parents and Guardians",
        "tag": "Parent / Guardian",
        "role": "Parent / Guardian",
        "hero_photo": "award.jpg",
        "side_photo": "presenting.jpg",
        "h1_html": "Your high school student, <span class=\"hilite\">paired with a UC Davis scientist.</span>",
        "lede": "Free, year-long, 1-on-1 environmental research mentorship — leading to a real science fair and a real network.",
        "body": [
            "EnvironMentors is for high school students who like science and want to do their own research project — not just read about it. Your student gets paired with a UC Davis grad student, postdoc, or faculty member who works alongside them for the full school year.",
            "They design their own project — water quality, climate adaptation, ecology, food systems, whatever they're curious about. Their mentor helps them scope it, run it, and present it at the UC Davis Science Fair in spring.",
            "The program is free. We work with the high school directly to make logistics easy. Some students go on to the GCSE International Science Fair — an all-expenses-covered trip with their cohort.",
        ],
        "cards": [
            ("Free, no cost", "Funded by the UC Davis Foundation and donors — no financial barrier."),
            ("College-app ready", "A real research portfolio item with a UC Davis mentor as a reference."),
        ],
    },
    {
        "slug": "hs-student",
        "label": "High School Student",
        "eyebrow": "For High School Students",
        "tag": "High School Student",
        "role": "High School Student",
        "hero_photo": "group-fair.jpg",
        "side_photo": "farm.jpg",
        "h1_html": "Pick a question. <span class=\"hilite\">Run a year-long research project.</span>",
        "lede": "A UC Davis scientist mentors you 1:1 for a year. You design the project, run it, and present at the UC Davis Science Fair.",
        "body": [
            "This is your project. You pick the question — climate change in your neighborhood, an invasive plant, water quality in Putah Creek, food access, anything environmental you can actually go investigate. Your mentor helps you scope it so it's doable in a year, then meets with you regularly to keep you moving.",
            "You'll learn how science actually works: framing a question, designing a method, collecting and analyzing data, and presenting your results to scientists who give you real feedback.",
            "In spring, you present at the UC Davis Science Fair. The strongest projects each year travel to the GCSE International Science Fair — meeting peers from chapters across the country.",
        ],
        "cards": [
            ("Real research", "Something to put on college applications that isn't a worksheet or a class lab."),
            ("Real mentor", "A scientist in your corner, all year. They have your back."),
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
        "h1_html": "Fund a year of research <span class=\"hilite\">for a young scientist.</span>",
        "lede": "Every dollar goes directly to mentee stipends, fair travel, and project supplies.",
        "body": [
            "EnvironMentors at UC Davis runs on philanthropic funding through the UC Davis Foundation. Donations are tax-deductible and earmarked specifically for our chapter — they pay for student stipends, lab supplies, fair registration fees, and travel to the GCSE International Science Fair.",
            "Naming and recognition opportunities are available at multiple levels — including individual mentor pairings, fair sponsorships, and travel-cohort sponsorships. Reach out and we'll tell you exactly what your gift will do.",
            "We also welcome corporate sponsorships and family foundation partnerships. A number of our peer chapters have multi-year sponsor relationships that have transformed what they can do.",
        ],
        "cards": [
            ("100% to students", "Stipends, supplies, fair travel — operational overhead is absorbed by UC Davis."),
            ("Tax-deductible", "Through the UC Davis Foundation; receipt provided."),
        ],
    },
    {
        "slug": "administrator",
        "label": "Administrator",
        "eyebrow": "For Department & Unit Leaders",
        "tag": "Administrator / Unit Leader",
        "role": "Administrator / Unit Leader",
        "hero_photo": "arboretum.jpg",
        "side_photo": "campus.jpg",
        "h1_html": "Plug into a <span class=\"hilite\">proven outreach program.</span>",
        "lede": "Help your faculty meet broader-impact requirements. Strengthen K-12 outreach metrics. Low overhead.",
        "body": [
            "EnvironMentors at UC Davis is a chapter of a national GCSE program with a proven structure. We deliver the K-12 outreach and mentorship lift that almost every federal grant in your unit's portfolio needs to demonstrate — without your faculty needing to design and run a program from scratch.",
            "We can plug in at multiple levels: as a turnkey broader-impact partner for individual PIs, as a unit-wide outreach line, or as a College or Center co-sponsored initiative with shared branding and metrics.",
            "Our reporting captures mentee outcomes, project quality, and post-program trajectories — useful for accreditation reviews, advancement materials, and federal reporting.",
        ],
        "cards": [
            ("Faculty BI lift", "Your PIs get a turnkey broader-impact partner — fewer one-off DIY programs."),
            ("Outreach metrics", "We deliver the K-12 engagement numbers that strengthen your unit's profile."),
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
  <div class="kicker">{label}</div>
  <h2>What this looks like for you.</h2>
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
            body_paragraphs=render_paragraphs(a["body"]),
            cards_html=render_cards(a["cards"]),
            form_url=build_form_url(a),
        )
        target = out_dir / f"{a['slug']}.html"
        target.write_text(html)
        print(f"wrote {target}")


if __name__ == "__main__":
    main()
