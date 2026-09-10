---
layout: page
title: "Research, Innovation & Frontiers"
description: "Pioneering interdisciplinary research in systems, artificial intelligence, quantum sciences, robotics, and clean energy technologies."
permalink: /research/
---

<div style="margin-bottom: 3rem;">
  <p style="font-size: 1.15rem; color: var(--color-primary); font-weight: 500;">
    Research at InstituteHub spans fundamental mathematical and theoretical inquiries to industrial-scale translation. With over $45M in active research grants and 40 dedicated research centers, our scholars address high-impact challenges across modern engineering.
  </p>
</div>

<!-- Research Areas -->
<section style="margin-bottom: 3.5rem;" id="areas">
  <h2 style="color: var(--color-primary); border-bottom: 2px solid var(--color-border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
    Key Strategic Research Areas
  </h2>
  <div class="grid grid-cols-4">
    <div class="card" style="padding: 1.25rem;">
      <h3 style="font-size: 1.1rem; color: var(--color-primary); margin-bottom: 0.35rem;">Distributed Systems</h3>
      <p style="font-size: 0.85rem; color: var(--color-text-muted); margin: 0;">Byzantine consensus, geo-replicated databases, fault tolerance, and cloud virtualization.</p>
    </div>
    <div class="card" style="padding: 1.25rem;">
      <h3 style="font-size: 1.1rem; color: var(--color-primary); margin-bottom: 0.35rem;">Artificial Intelligence</h3>
      <p style="font-size: 0.85rem; color: var(--color-text-muted); margin: 0;">Multimodal diagnostic vision, low-resource Indic LLMs, and explainable neural reasoning.</p>
    </div>
    <div class="card" style="padding: 1.25rem;">
      <h3 style="font-size: 1.1rem; color: var(--color-primary); margin-bottom: 0.35rem;">Operating Systems</h3>
      <p style="font-size: 0.85rem; color: var(--color-text-muted); margin: 0;">eBPF kernel telemetry, hardware-assisted memory tagging, and hypervisor isolation.</p>
    </div>
    <div class="card" style="padding: 1.25rem;">
      <h3 style="font-size: 1.1rem; color: var(--color-primary); margin-bottom: 0.35rem;">Quantum Computing</h3>
      <p style="font-size: 0.85rem; color: var(--color-text-muted); margin: 0;">Fault-tolerant surface codes, cryogenic microwave synthesis, and quantum error mitigation.</p>
    </div>
  </div>
</section>

<!-- Active Research Projects Dynamic Listing -->
<section style="margin-bottom: 3.5rem;" id="projects">
  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--color-border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
    <h2 style="color: var(--color-primary); margin: 0;">
      Active Funded Research Projects
    </h2>
    <span class="badge badge-primary">{{ site.research | size }} Projects</span>
  </div>

  <div class="grid grid-cols-3">
    {% for project in site.research %}
      {% include research-card.html project=project %}
    {% endfor %}
  </div>
</section>

<!-- Publications Archive Dynamic Listing -->
<section style="margin-bottom: 3.5rem;" id="publications">
  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--color-border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
    <h2 style="color: var(--color-primary); margin: 0;">
      Selected Peer-Reviewed Publications
    </h2>
    <span class="badge badge-secondary">{{ site.publications | size }} Recent Papers</span>
  </div>

  <div style="background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 6px; padding: 1.5rem;">
    <ol style="padding-left: 1.25rem; font-size: 0.95rem; line-height: 1.7;">
      {% for pub in site.publications %}
        <li style="margin-bottom: 1.25rem; padding-bottom: 1rem; border-bottom: 1px dashed var(--color-border);">
          <span style="font-weight: 700; color: var(--color-primary); font-size: 1rem; display: block;">
            <a href="{{ pub.url | relative_url }}">{{ pub.title }}</a>
          </span>
          <span style="color: var(--color-text-muted); font-size: 0.85rem; display: block;">
            {{ pub.authors | join: ", " }} &bull; <em>{{ pub.venue }}</em> ({{ pub.year }})
          </span>
          {% if pub.doi %}
            <span style="font-size: 0.75rem; color: var(--color-text-light);">
              DOI: <a href="https://doi.org/{{ pub.doi }}" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent);">{{ pub.doi }}</a>
            </span>
          {% endif %}
        </li>
      {% endfor %}
    </ol>
  </div>
</section>

<!-- Centers of Excellence & Labs -->
<section style="margin-bottom: 3.5rem;" id="labs">
  <h2 style="color: var(--color-primary); border-bottom: 2px solid var(--color-border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
    Advanced Centers of Excellence
  </h2>
  <div class="grid grid-cols-2">
    <div style="background: var(--color-surface); border: 1px solid var(--color-border); padding: 1.5rem; border-radius: 6px;">
      <h3 style="color: var(--color-primary); margin-top: 0;">Center for Frontier Artificial Intelligence (CFAI)</h3>
      <p style="font-size: 0.9rem; color: var(--color-text-muted);">
        Equipped with 64x NVIDIA H100 GPU clusters powering foundational research in medical imaging, reasoning models, and edge neural processing.
      </p>
    </div>
    <div style="background: var(--color-surface); border: 1px solid var(--color-border); padding: 1.5rem; border-radius: 6px;">
      <h3 style="color: var(--color-primary); margin-top: 0;">Bose Quantum Systems Complex</h3>
      <p style="font-size: 0.9rem; color: var(--color-text-muted);">
        Housing 10 mK dilution refrigerators, microwave vector signal generators, and FPGA cryogenic control instrumentation.
      </p>
    </div>
    <div style="background: var(--color-surface); border: 1px solid var(--color-border); padding: 1.5rem; border-radius: 6px;">
      <h3 style="color: var(--color-primary); margin-top: 0;">Systems Architecture & Resilience (SAR) Lab</h3>
      <p style="font-size: 0.9rem; color: var(--color-text-muted);">
        Testing ground for Linux kernel security, custom hypervisors, memory tagging, and line-rate programmable network switches.
      </p>
    </div>
    <div style="background: var(--color-surface); border: 1px solid var(--color-border); padding: 1.5rem; border-radius: 6px;">
      <h3 style="color: var(--color-primary); margin-top: 0;">Autonomous Swarms & Field Robotics Arena</h3>
      <p style="font-size: 0.9rem; color: var(--color-text-muted);">
        A 5,000 sq ft indoor-outdoor testing arena equipped with Vicon sub-millimeter motion tracking cameras for multi-drone swarms.
      </p>
    </div>
  </div>
</section>

<!-- Industry Collaborations -->
<section id="collaborations" style="background: var(--color-surface-subtle); border: 1px solid var(--color-border); padding: 2rem; border-radius: 6px;">
  <h2 style="color: var(--color-primary); margin-top: 0;">Industry Collaborations & Technology Transfer</h2>
  <p style="font-size: 0.95rem; color: var(--color-text-muted); line-height: 1.6;">
    InstituteHub partners with global tech leaders, national research agencies, and innovative startups through sponsored joint development projects, consortium memberships, and licensing of patented intellectual property.
  </p>
  <div style="margin-top: 1rem;">
    <a href="{{ '/contact/' | relative_url }}" class="btn btn-primary">Partner with InstituteHub R&D &rarr;</a>
  </div>
</section>
