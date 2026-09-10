---
layout: page
title: "Faculty & Scholars Directory"
description: "Search and discover faculty members, research interests, department chairs, and scholarly profiles at InstituteHub."
permalink: /people/
---

<div style="margin-bottom: 2rem;">
  <p style="font-size: 1.1rem; color: var(--color-text-muted);">
    InstituteHub's faculty comprises world-renowned researchers, dedicated educators, and recipients of premier national and international honors.
  </p>
</div>

<!-- Interactive Search & Filtering Toolbar -->
<div class="filter-toolbar">
  <div class="filter-group">
    <label for="facultyDeptFilter" class="filter-label">Department:</label>
    <select id="facultyDeptFilter" class="filter-select" aria-label="Filter by Department">
      <option value="all">All Departments</option>
      <option value="Computer Science">Computer Science and Engineering</option>
      <option value="Artificial Intelligence">AI and Data Science</option>
      <option value="Electrical">Electrical & Electronics</option>
      <option value="Robotics">Robotics & Automation</option>
      <option value="Quantum">Physics & Quantum Engineering</option>
      <option value="Systems Engineering">Systems Engineering</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="facultyAreaFilter" class="filter-label">Research Area:</label>
    <select id="facultyAreaFilter" class="filter-select" aria-label="Filter by Research Area">
      <option value="all">All Research Fields</option>
      <option value="Distributed Systems">Distributed Systems</option>
      <option value="Computer Vision">Computer Vision / AI</option>
      <option value="Operating Systems">Operating Systems & Security</option>
      <option value="Edge AI">Edge AI & VLSI</option>
      <option value="Robotics">Robotics & Swarms</option>
      <option value="Quantum">Quantum Computing</option>
      <option value="Smart Grid">Power & Smart Grids</option>
    </select>
  </div>

  <div class="filter-group" style="flex: 1; max-width: 350px;">
    <label for="facultySearchInput" class="sr-only">Search Faculty</label>
    <input type="text" id="facultySearchInput" class="filter-input" placeholder="Search by name, topic, or keyword..." style="width: 100%;">
  </div>
</div>

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
  <span id="facultyResultCount" style="font-size: 0.9rem; font-weight: 700; color: var(--color-primary);">
    Showing {{ site.faculty | size }} faculty members
  </span>
  <span style="font-size: 0.8rem; color: var(--color-text-light);">
    Click any profile to view full curriculum, publications, and office hours.
  </span>
</div>

<!-- Dynamic Faculty Directory Grid -->
<div class="grid grid-cols-3" id="facultyGridContainer">
  {% for faculty in site.faculty %}
    {% include faculty-card.html faculty=faculty %}
  {% endfor %}
</div>
