#!/usr/bin/env python3
"""Build script: reads _data/guests/*.yml and generates static HTML pages."""
import os, yaml, html as html_module
from pathlib import Path

SITE_URL = "https://coolvectorexperts.netlify.app"
TAGLINE = "Primary-source intel about data centers and the digital infrastructure asset class"

LOGO_HTML_GUEST = """    <div class="site-logo-wrap">
      <a href="https://coolvector.substack.com/" target="_blank" rel="noopener">
        <img src="../images/cool-vector-logo.png" alt="Cool Vector" class="site-logo" />
      </a>
    </div>"""

LOGO_HTML_INDEX = """    <div class="site-logo-wrap">
      <a href="https://coolvector.substack.com/" target="_blank" rel="noopener">
        <img src="images/cool-vector-logo.png" alt="Cool Vector" class="site-logo" />
      </a>
    </div>"""

def esc(s):
    return html_module.escape(str(s or ''), quote=True)

def capitalize_first(s):
    s = s.strip()
    if not s:
        return s
    words = s.split(' ')
    words[0] = words[0].capitalize()
    return ' '.join(words)

ABOUT_SECTION = """<div class="about-section">
  <h2>Welcome to Cool Vector!</h2>
  <h3>About Cool Vector</h3>
  <p>Cool Vector is a video-podcast about the rise of data centers and the digital infrastructure asset class. On a regular basis, the podcast convenes expert conversations about the investment opportunities and macro themes driving the build-out of digital infrastructure, including private capital dynamics, performance expectations, energy demand, geopolitical influences, sustainability opportunities, development and construction, technology and community impact.</p>
  <p>Cool Vector is hosted by financial journalist David Snow, a long-time chronicler of the alternative investment market, as well as editorial advisors Phillip Koblence and Nabeel Mahmood, data center industry veterans and co-founders of the Nomad Futurist Foundation.</p>
  <form class="subscribe-form" action="https://coolvector.substack.com/subscribe" method="get" target="_blank">
    <input type="email" name="email" placeholder="Enter your email address" />
    <button type="submit">Subscribe</button>
  </form>
</div>"""

def build_guest_page(gid, g):
    name = g.get('name', '')
    title = g.get('title', '')
    firm = g.get('firm', '')
    bio = g.get('bio', '')
    topics = [capitalize_first(t) for t in g.get('topics', [])]
    ep_title = g.get('episodeTitle', '')
    ep_url = g.get('episodeUrl', '')

    bio_short = esc(bio[:160]) + '\u2026' if len(bio) > 160 else esc(bio)
    topics_li = '\n'.join(f'          <li>{esc(t)}</li>' for t in topics)
    bio_html = f'<p class="guest-bio">{esc(bio)}</p>' if bio else ''
    
    job_title = title.split(',')[0].split('&')[0].strip()

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(name)} | Cool Vector Video-Podcast</title>
  <meta name="description" content="{bio_short}">
  <meta property="og:title" content="{esc(name)} | Cool Vector">
  <meta property="og:description" content="{bio_short}">
  <meta property="og:image" content="../images/{gid}.jpg">
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{name}",
  "jobTitle": "{job_title}",
  "worksFor": {{
    "@type": "Organization",
    "name": "{firm}"
  }},
  "description": {json_str(bio)},
  "url": "{SITE_URL}/guests/{gid}.html",
  "appearanceOn": {{
    "@type": "PodcastEpisode",
    "name": "{ep_title}",
    "url": "{ep_url}"
  }}
}}
  </script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="site-wrapper">

{LOGO_HTML_GUEST}

    <a class="back-link" href="../index.html">← Back to all guests</a>

    <div class="guest-header">
      <img class="guest-photo" src="../images/{gid}.jpg" alt="Photo of {esc(name)}" />
      <div class="guest-meta">
        <div class="podcast-label">Cool Vector Video-Podcast</div>
        <div class="podcast-tagline">{TAGLINE}</div>
        <div class="guest-speaker-label">Guest Speaker</div>
        <h1 class="guest-name">{esc(name)}</h1>
        <div class="guest-title-firm">{esc(title)}, {esc(firm)}</div>

        {bio_html}

        <div class="topics-label">Topics covered on Cool Vector:</div>
        <ul class="topics-list">
{topics_li}
        </ul>

        <div class="episodes-label">Cool Vector episodes in which {esc(name.split()[0])} appears:</div>
        <a class="episode-link" href="{esc(ep_url)}" target="_blank" rel="noopener">{esc(ep_title)}</a>
      </div>
    </div>

    <a class="back-link-bottom" href="../index.html">← Back to all guests</a>

    {ABOUT_SECTION}

  </div>
</body>
</html>"""
    return page

def json_str(s):
    import json
    return json.dumps(s)

def build_index(guests_list):
    cards = []
    for gid, g in guests_list:
        name = g.get('name', '')
        title = g.get('title', '')
        firm = g.get('firm', '')
        cards.append(f"""    <a class="guest-card" href="guests/{gid}.html">
      <img src="images/{gid}.jpg" alt="{esc(name)}" />
      <div class="card-info">
        <div class="card-name">{esc(name)}</div>
        <div class="card-title">{esc(title)}</div>
        <div class="card-firm">{esc(firm)}</div>
      </div>
    </a>""")

    cards_html = '\n'.join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cool Vector | Expert Guest Directory</title>
  <meta name="description" content="Meet the experts who have appeared on Cool Vector, the video-podcast about data centers and digital infrastructure.">
  <link rel="stylesheet" href="style.css">
  <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
  <script>
    // Redirect Netlify Identity tokens (invite/recovery) to /admin so the widget can process them
    if (window.location.hash && (window.location.hash.includes('invite_token') || window.location.hash.includes('recovery_token'))) {{
      window.location = '/admin/' + window.location.hash;
    }}
  </script>
</head>
<body>
  <div class="site-wrapper">
    <div class="index-header">
{LOGO_HTML_INDEX}
      <div class="podcast-tagline">{TAGLINE}</div>
      <h1>Expert Guest Directory</h1>
    </div>
    <div class="guest-grid">
{cards_html}
    </div>
    {ABOUT_SECTION}
  </div>
</body>
</html>"""

def main():
    data_dir = Path('_data/guests')
    guests_dir = Path('guests')
    guests_dir.mkdir(exist_ok=True)

    guests_list = []
    for yml_file in sorted(data_dir.glob('*.yml')):
        gid = yml_file.stem
        with open(yml_file) as f:
            g = yaml.safe_load(f)
        guests_list.append((gid, g))
        page = build_guest_page(gid, g)
        out_path = guests_dir / f'{gid}.html'
        out_path.write_text(page)
        print(f'Built {out_path}')

    index = build_index(guests_list)
    Path('index.html').write_text(index)
    print(f'Built index.html with {len(guests_list)} guests')

if __name__ == '__main__':
    main()
