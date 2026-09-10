---
layout: page
title: "Events, Conferences & Symposia"
description: "Discover upcoming academic conferences, distinguished guest lectures, research workshops, and hackathons at InstituteHub."
permalink: /events/
---

<div style="margin-bottom: 2rem;">
  <p style="font-size: 1.1rem; color: var(--color-text-muted);">
    Participate in frontier engineering discourses, distinguished lectures, and research colloquia hosted across InstituteHub auditoriums and labs.
  </p>
</div>

<!-- Interactive Events Filter Chips -->
<div class="filter-toolbar">
  <div class="filter-group">
    <span class="filter-label">Filter:</span>
    <button type="button" class="filter-btn-chip event-filter-chip active" data-filter="all">All Events</button>
    <button type="button" class="filter-btn-chip event-filter-chip" data-filter="upcoming">Upcoming</button>
    <button type="button" class="filter-btn-chip event-filter-chip" data-filter="Symposium">Symposia</button>
    <button type="button" class="filter-btn-chip event-filter-chip" data-filter="Workshop">Workshops</button>
    <button type="button" class="filter-btn-chip event-filter-chip" data-filter="Hackathon">Hackathons</button>
    <button type="button" class="filter-btn-chip event-filter-chip" data-filter="Lecture">Lectures</button>
  </div>
</div>

<div style="display: flex; flex-direction: column; gap: 1.25rem;">
  {% for event in site.events %}
    {% assign event_date = event.date | date: "%Y%m%d" %}
    {% assign current_date = "20260910" %}
    {% assign timing_val = "upcoming" %}
    {% if event_date < current_date %}
      {% assign timing_val = "past" %}
    {% endif %}
    {% include event-card.html event=event timing=timing_val %}
  {% endfor %}
</div>
