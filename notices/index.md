---
layout: page
title: "Official Notices & Circulars"
description: "Central repository of official administrative notifications, academic circulars, exam schedules, and recruitment announcements."
permalink: /notices/
---

<div style="margin-bottom: 2rem;">
  <p style="font-size: 1.1rem; color: var(--color-text-muted);">
    Central notice repository for students, faculty, staff, and external applicants. All official orders and circulars are digitally signed.
  </p>
</div>

<!-- Notice Category Filter Toolbar -->
<div class="filter-toolbar">
  <div class="filter-group">
    <span class="filter-label">Category:</span>
    <button type="button" class="filter-btn-chip notice-filter-chip active" data-filter="all">All</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Academic">Academic</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Admissions">Admissions</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Examination">Examination</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Recruitment">Recruitment</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Research">Research</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Campus">Campus</button>
    <button type="button" class="filter-btn-chip notice-filter-chip" data-filter="Administration">Administration</button>
  </div>

  <div class="filter-group" style="flex: 1; max-width: 320px;">
    <label for="noticeSearchInput" class="sr-only">Search Notices</label>
    <input type="text" id="noticeSearchInput" class="filter-input" placeholder="Search notices by title, ref no..." style="width: 100%;">
  </div>
</div>

<div style="display: flex; flex-direction: column;">
  {% for notice in site.notices %}
    {% include notice-card.html notice=notice %}
  {% endfor %}
</div>
