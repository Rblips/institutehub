---
layout: page
title: "Contact & Campus Directory"
description: "Get in touch with InstituteHub administrative offices, department chairs, admissions counselors, and emergency services."
permalink: /contact/
---

<div class="layout-with-sidebar">
  <div>
    <h2 style="color: var(--color-primary); border-bottom: 2px solid var(--color-border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
      Send an Inquiry
    </h2>
    <p style="font-size: 0.95rem; color: var(--color-text-muted); margin-bottom: 1.5rem;">
      Please select the appropriate recipient department to ensure your inquiry is routed promptly to the relevant administrative office.
    </p>

    <form style="display: flex; flex-direction: column; gap: 1.25rem; background: var(--color-surface); border: 1px solid var(--color-border); padding: 2rem; border-radius: 6px;" onsubmit="event.preventDefault(); alert('Inquiry submitted successfully. InstituteHub offices will respond within 2 business days.'); this.reset();">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
          <label for="contactName" style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.35rem; color: var(--color-primary);">Full Name *</label>
          <input type="text" id="contactName" required class="filter-input" style="width: 100%;" placeholder="e.g. Dr. Jane Doe">
        </div>
        <div>
          <label for="contactEmail" style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.35rem; color: var(--color-primary);">Email Address *</label>
          <input type="email" id="contactEmail" required class="filter-input" style="width: 100%;" placeholder="e.g. user@domain.com">
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
          <label for="contactDept" style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.35rem; color: var(--color-primary);">Department / Office *</label>
          <select id="contactDept" required class="filter-select" style="width: 100%;">
            <option value="admissions">Admissions & Outreach</option>
            <option value="academics">Academic Affairs</option>
            <option value="research">Research & Technology Transfer (SRIC)</option>
            <option value="registrar">Office of the Registrar</option>
            <option value="its">IT Services & Helpdesk</option>
            <option value="media">Media & Communications</option>
          </select>
        </div>
        <div>
          <label for="contactSubject" style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.35rem; color: var(--color-primary);">Subject *</label>
          <input type="text" id="contactSubject" required class="filter-input" style="width: 100%;" placeholder="e.g. Ph.D. Fellowship Inquiry">
        </div>
      </div>

      <div>
        <label for="contactMessage" style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.35rem; color: var(--color-primary);">Message *</label>
        <textarea id="contactMessage" rows="5" required class="filter-input" style="width: 100%; font-family: inherit;" placeholder="Please outline your specific query..."></textarea>
      </div>

      <button type="submit" class="btn btn-primary" style="align-self: flex-start;">
        Submit Official Inquiry &rarr;
      </button>
    </form>
  </div>

  <aside>
    <div class="sidebar-widget">
      <h3 class="sidebar-title">Campus Headquarters</h3>
      <address style="font-style: normal; font-size: 0.9rem; line-height: 1.6; color: var(--color-text-muted);">
        <strong>InstituteHub of Technology & Engineering</strong><br>
        {{ site.institute.address }}<br>
        {{ site.institute.city }}, {{ site.institute.state }} - {{ site.institute.postal_code }}<br>
        {{ site.institute.country }}
      </address>
    </div>

    <div class="sidebar-widget">
      <h3 class="sidebar-title">Key Contact Directory</h3>
      <div style="font-size: 0.85rem; display: flex; flex-direction: column; gap: 0.75rem;">
        <div>
          <span style="font-weight: 700; color: var(--color-primary); display: block;">General Inquiries</span>
          <a href="mailto:{{ site.institute.email }}">{{ site.institute.email }}</a><br>
          <span>{{ site.institute.phone }}</span>
        </div>
        <div>
          <span style="font-weight: 700; color: var(--color-primary); display: block;">Admissions Desk</span>
          <a href="mailto:{{ site.institute.admissions_email }}">{{ site.institute.admissions_email }}</a>
        </div>
        <div>
          <span style="font-weight: 700; color: var(--color-primary); display: block;">Office of Registrar</span>
          <a href="mailto:{{ site.institute.registrar_email }}">{{ site.institute.registrar_email }}</a>
        </div>
        <div>
          <span style="font-weight: 700; color: var(--color-accent); display: block;">Emergency Control Room</span>
          <span style="font-weight: 700;">+91 (080) 4567-8999 (24x7)</span>
        </div>
      </div>
    </div>
  </aside>
</div>
