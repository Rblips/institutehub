---
layout: page
title: "InstituteHub Newsroom & Media"
description: "Latest institutional news, faculty accolades, research breakthroughs, and campus events at InstituteHub."
permalink: /news/
---

<div style="margin-bottom: 2.5rem;">
  <p style="font-size: 1.1rem; color: var(--color-text-muted);">
    Stay updated on scientific breakthroughs, distinguished academic honors, and transformative campus initiatives.
  </p>
</div>

<!-- Featured Post -->
{% assign featured = site.posts.first %}
{% if featured %}
<div class="card" style="margin-bottom: 3rem; border-left: 5px solid var(--color-primary); background: var(--color-surface);">
  <div class="card-body" style="padding: 2rem;">
    <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.75rem;">
      <span class="badge badge-accent">{{ featured.category | default: "Featured Story" }}</span>
      <time datetime="{{ featured.date | date_to_xmlschema }}" style="font-size: 0.85rem; color: var(--color-text-light);">
        {{ featured.date | date: "%B %d, %Y" }}
      </time>
    </div>
    <h2 style="font-size: 1.75rem; font-weight: 800; line-height: 1.25; margin-bottom: 0.75rem;">
      <a href="{{ featured.url | relative_url }}" style="color: var(--color-primary);">{{ featured.title }}</a>
    </h2>
    <p style="font-size: 1rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem;">
      {{ featured.lead | default: featured.excerpt | strip_html }}
    </p>
    <a href="{{ featured.url | relative_url }}" class="btn btn-primary btn-sm">Read Full Article &rarr;</a>
  </div>
</div>
{% endif %}

<!-- News Archive Grid -->
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--color-border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
  <h2 style="color: var(--color-primary); margin: 0; font-size: 1.4rem;">
    All Institutional Articles
  </h2>
  <span class="badge badge-secondary">{{ site.posts | size }} Stories</span>
</div>

<div class="grid grid-cols-3">
  {% for post in site.posts %}
    {% include news-card.html post=post %}
  {% endfor %}
</div>
