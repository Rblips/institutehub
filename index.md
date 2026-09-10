---
layout: default
title: "InstituteHub | Premier Engineering Institute"
---

{% include hero.html %}
{% include stats.html %}

<!-- Section 1: Institutional Announcements / Notices -->
<section class="section section-subtle" aria-labelledby="notices-heading">
  <div class="container">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem;">
      <div>
        <span class="section-tag">Official Communication</span>
        <h2 id="notices-heading" class="section-title">Latest Announcements & Circulars</h2>
        <p class="section-subtitle">Official administrative orders, academic deadlines, and doctoral admissions notices.</p>
      </div>
      <a href="{{ '/notices/' | relative_url }}" class="btn btn-outline btn-sm">View Notice Board &rarr;</a>
    </div>

    <div>
      {% for notice in site.notices limit: 4 %}
        {% include notice-card.html notice=notice %}
      {% endfor %}
    </div>
  </div>
</section>

<!-- Section 2: Research Spotlight -->
<section class="section" aria-labelledby="research-heading">
  <div class="container">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem;">
      <div>
        <span class="section-tag">Discovery & Innovation</span>
        <h2 id="research-heading" class="section-title">Frontier Research Spotlight</h2>
        <p class="section-subtitle">Addressing complex global challenges through interdisciplinary engineering science and technology transfer.</p>
      </div>
      <a href="{{ '/research/' | relative_url }}" class="btn btn-outline btn-sm">Explore All Projects &rarr;</a>
    </div>

    <div class="grid grid-cols-3">
      {% for project in site.research limit: 3 %}
        {% include research-card.html project=project %}
      {% endfor %}
    </div>
  </div>
</section>

<!-- Section 3: Academic Programs -->
<section class="section section-subtle" aria-labelledby="programs-heading">
  <div class="container">
    <div style="text-align: center; max-width: 760px; margin: 0 auto 3rem auto;">
      <span class="section-tag">Curriculum & Degrees</span>
      <h2 id="programs-heading" class="section-title">World-Class Academic Programs</h2>
      <p class="section-subtitle" style="margin: 0 auto;">Rigorous, laboratory-intensive degree programs engineered to develop technical leaders and researchers.</p>
    </div>

    <div class="grid grid-cols-4">
      <div class="card" style="border-top: 4px solid var(--color-primary);">
        <div class="card-body">
          <span class="badge badge-primary" style="margin-bottom: 0.75rem;">Undergraduate</span>
          <h3 class="card-title">Bachelor of Technology (B.Tech)</h3>
          <p class="card-text">4-year intensive program across CS, Electrical, Robotics, and Data Science with hands-on capstones.</p>
        </div>
        <div class="card-footer">
          <a href="{{ '/academics/#undergraduate' | relative_url }}" class="btn btn-outline btn-sm" style="width: 100%;">Curriculum Details &rarr;</a>
        </div>
      </div>

      <div class="card" style="border-top: 4px solid var(--color-secondary);">
        <div class="card-body">
          <span class="badge badge-secondary" style="margin-bottom: 0.75rem;">Postgraduate</span>
          <h3 class="card-title">Master of Technology (M.Tech / M.S.)</h3>
          <p class="card-text">2-year research and thesis-driven programs specialized in Distributed Systems, VLSI, and AI.</p>
        </div>
        <div class="card-footer">
          <a href="{{ '/academics/#postgraduate' | relative_url }}" class="btn btn-outline btn-sm" style="width: 100%;">Specializations &rarr;</a>
        </div>
      </div>

      <div class="card" style="border-top: 4px solid var(--color-accent);">
        <div class="card-body">
          <span class="badge badge-accent" style="margin-bottom: 0.75rem;">Doctoral</span>
          <h3 class="card-title">Doctor of Philosophy (Ph.D.)</h3>
          <p class="card-text">Fully funded doctoral fellowships with access to supercomputing clusters, cleanrooms, and top mentors.</p>
        </div>
        <div class="card-footer">
          <a href="{{ '/academics/#doctoral' | relative_url }}" class="btn btn-outline btn-sm" style="width: 100%;">Fellowship Info &rarr;</a>
        </div>
      </div>

      <div class="card" style="border-top: 4px solid var(--color-primary-light);">
        <div class="card-body">
          <span class="badge badge-primary" style="margin-bottom: 0.75rem;">Executive</span>
          <h3 class="card-title">Continuing & Executive Studies</h3>
          <p class="card-text">Advanced modular diplomas and certifications in Systems Security, Cloud, and Deep Learning.</p>
        </div>
        <div class="card-footer">
          <a href="{{ '/academics/#continuing' | relative_url }}" class="btn btn-outline btn-sm" style="width: 100%;">Executive Portal &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Section 4: Faculty Spotlight -->
<section class="section" aria-labelledby="faculty-heading">
  <div class="container">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem;">
      <div>
        <span class="section-tag">Scholars & Mentors</span>
        <h2 id="faculty-heading" class="section-title">Distinguished Faculty Spotlight</h2>
        <p class="section-subtitle">Internationally recognized researchers and dedicated educators driving scientific breakthroughs.</p>
      </div>
      <a href="{{ '/people/' | relative_url }}" class="btn btn-outline btn-sm">Full Faculty Directory &rarr;</a>
    </div>

    <div class="grid grid-cols-4">
      {% for member in site.faculty limit: 4 %}
        {% include faculty-card.html faculty=member %}
      {% endfor %}
    </div>
  </div>
</section>

<!-- Section 5: Upcoming Events & News Grid -->
<section class="section section-subtle" aria-labelledby="events-news-heading">
  <div class="container">
    <div class="layout-with-sidebar">
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <h2 id="events-news-heading" class="section-title" style="margin: 0; font-size: 1.5rem;">Upcoming Events & Symposia</h2>
          <a href="{{ '/events/' | relative_url }}" class="btn btn-outline btn-sm">All Events &rarr;</a>
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          {% for event in site.events limit: 3 %}
            {% include event-card.html event=event %}
          {% endfor %}
        </div>
      </div>

      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <h2 class="section-title" style="margin: 0; font-size: 1.5rem;">Campus News</h2>
          <a href="{{ '/news/' | relative_url }}" class="btn btn-outline btn-sm">Newsroom &rarr;</a>
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          {% for post in site.posts limit: 3 %}
            {% include news-card.html post=post %}
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Section 6: Final Call to Action -->
<section class="section section-primary" style="text-align: center;">
  <div class="container" style="max-width: 800px;">
    <span class="section-tag" style="color: #fca5a5;">Join Our Community</span>
    <h2 class="section-title" style="color: #ffffff; font-size: 2.5rem; margin-bottom: 1rem;">Shape the Future of Engineering</h2>
    <p class="section-subtitle" style="color: #cbd5e1; margin: 0 auto 2rem auto; font-size: 1.15rem;">
      Whether you are an aspiring undergraduate, prospective doctoral fellow, industry partner, or prospective faculty scholar, discover your path at InstituteHub.
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
      <a href="{{ '/admissions/' | relative_url }}" class="btn btn-accent">Explore Admissions 2026-27</a>
      <a href="{{ '/contact/' | relative_url }}" class="btn btn-outline-white">Contact Admissions Office</a>
    </div>
  </div>
</section>
