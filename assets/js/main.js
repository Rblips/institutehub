/**
 * InstituteHub - Core Client-Side Logic & Accessibility Suite
 * Pure Vanilla JavaScript (No heavy frameworks)
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNavigation();
  initSearchSystem();
  initFacultyFilter();
  initNoticesFilter();
  initEventsFilter();
  initTabs();
  initHeaderScroll();
});

/* ==========================================================================
   1. Mobile Navigation & Accessibility
   ========================================================================== */
function initMobileNavigation() {
  const toggleBtn = document.getElementById('mobileNavToggle');
  const drawer = document.getElementById('mobileNavDrawer');
  
  if (!toggleBtn || !drawer) return;

  toggleBtn.addEventListener('click', () => {
    const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
    toggleBtn.setAttribute('aria-expanded', !isExpanded);
    drawer.classList.toggle('open');
    document.body.style.overflow = isExpanded ? '' : 'hidden';
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
      toggleBtn.setAttribute('aria-expanded', 'false');
      drawer.classList.remove('open');
      document.body.style.overflow = '';
      toggleBtn.focus();
    }
  });
}

/* ==========================================================================
   2. Header Scroll Effect
   ========================================================================== */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.style.boxShadow = '0 4px 12px rgba(10, 37, 64, 0.12)';
    } else {
      header.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
    }
  }, { passive: true });
}

/* ==========================================================================
   3. Fast Client-Side Search Engine & Modal
   ========================================================================== */
let searchIndexData = null;

function initSearchSystem() {
  const modalBackdrop = document.getElementById('searchModalBackdrop');
  const searchInput = document.getElementById('searchModalInput');
  const resultsContainer = document.getElementById('searchResultsList');
  const closeBtn = document.getElementById('searchCloseBtn');
  const triggers = document.querySelectorAll('.search-trigger, .btn-search-trigger');

  if (!modalBackdrop || !searchInput || !resultsContainer) return;

  // Pre-fetch search index
  const fetchIndex = async () => {
    if (searchIndexData) return searchIndexData;
    try {
      const basePath = document.body.getAttribute('data-baseurl') || '';
      const response = await fetch(`${basePath}/search.json`);
      if (response.ok) {
        searchIndexData = await response.json();
      }
    } catch (err) {
      console.warn('InstituteHub Search: Could not load index', err);
    }
    return searchIndexData;
  };

  const openModal = () => {
    modalBackdrop.classList.add('open');
    modalBackdrop.setAttribute('aria-hidden', 'false');
    fetchIndex();
    setTimeout(() => searchInput.focus(), 50);
  };

  const closeModal = () => {
    modalBackdrop.classList.remove('open');
    modalBackdrop.setAttribute('aria-hidden', 'true');
    searchInput.value = '';
    resultsContainer.innerHTML = '';
  };

  window.openSearchModal = openModal;
  window.closeSearchModal = closeModal;

  triggers.forEach(btn => btn.addEventListener('click', openModal));
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });

  // Global Keyboard Shortcuts: '/' or 'Cmd+K' / 'Ctrl+K' to open search, 'Escape' to close
  document.addEventListener('keydown', (e) => {
    if ((e.key === '/' || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) && 
        document.activeElement.tagName !== 'INPUT' && 
        document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      openModal();
    } else if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) {
      closeModal();
    }
  });

  // Real-time Search Filter
  searchInput.addEventListener('input', async (e) => {
    const query = e.target.value.trim().toLowerCase();
    if (query.length < 2) {
      resultsContainer.innerHTML = '<li style="padding: 1.5rem; text-align: center; color: #64748b;">Type at least 2 characters to search across faculty, courses, research, events, and notices...</li>';
      return;
    }

    const data = await fetchIndex();
    if (!data || data.length === 0) {
      resultsContainer.innerHTML = '<li style="padding: 1.5rem; text-align: center; color: #64748b;">Loading search index...</li>';
      return;
    }

    const matched = data.filter(item => {
      return (item.title && item.title.toLowerCase().includes(query)) ||
             (item.subtitle && item.subtitle.toLowerCase().includes(query)) ||
             (item.department && item.department.toLowerCase().includes(query)) ||
             (item.summary && item.summary.toLowerCase().includes(query)) ||
             (item.content && item.content.toLowerCase().includes(query)) ||
             (item.category && item.category.toLowerCase().includes(query));
    }).slice(0, 10);

    if (matched.length === 0) {
      resultsContainer.innerHTML = `<li style="padding: 1.5rem; text-align: center; color: #64748b;">No results found for "${escapeHtml(query)}"</li>`;
      return;
    }

    resultsContainer.innerHTML = matched.map((item, idx) => `
      <li class="search-result-item" role="option">
        <a href="${item.url}" style="display: block; text-decoration: none; color: inherit;">
          <div class="search-result-title">
            <span>${escapeHtml(item.title)}</span>
            <span class="badge badge-secondary">${escapeHtml(item.category)}</span>
          </div>
          <div class="search-result-desc">
            ${item.subtitle ? `<strong>${escapeHtml(item.subtitle)}</strong> &bull; ` : ''}
            ${item.summary ? escapeHtml(item.summary) : ''}
          </div>
        </a>
      </li>
    `).join('');
  });
}

/* ==========================================================================
   4. Faculty Directory Filter & Search
   ========================================================================== */
function initFacultyFilter() {
  const deptSelect = document.getElementById('facultyDeptFilter');
  const searchInput = document.getElementById('facultySearchInput');
  const areaSelect = document.getElementById('facultyAreaFilter');
  const facultyCards = document.querySelectorAll('.faculty-item-card');
  const countDisplay = document.getElementById('facultyResultCount');

  if (!facultyCards.length) return;

  const applyFilters = () => {
    const selectedDept = deptSelect ? deptSelect.value.toLowerCase() : 'all';
    const selectedArea = areaSelect ? areaSelect.value.toLowerCase() : 'all';
    const searchQuery = searchInput ? searchInput.value.toLowerCase().trim() : '';

    let visibleCount = 0;

    facultyCards.forEach(card => {
      const dept = (card.getAttribute('data-department') || '').toLowerCase();
      const area = (card.getAttribute('data-interests') || '').toLowerCase();
      const text = card.textContent.toLowerCase();

      const matchesDept = (selectedDept === 'all' || dept.includes(selectedDept));
      const matchesArea = (selectedArea === 'all' || area.includes(selectedArea));
      const matchesSearch = (!searchQuery || text.includes(searchQuery));

      if (matchesDept && matchesArea && matchesSearch) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (countDisplay) {
      countDisplay.textContent = `Showing ${visibleCount} faculty members`;
    }
  };

  if (deptSelect) deptSelect.addEventListener('change', applyFilters);
  if (areaSelect) areaSelect.addEventListener('change', applyFilters);
  if (searchInput) searchInput.addEventListener('input', applyFilters);
}

/* ==========================================================================
   5. Notices & Circulars Filter
   ========================================================================== */
function initNoticesFilter() {
  const chips = document.querySelectorAll('.notice-filter-chip');
  const searchInput = document.getElementById('noticeSearchInput');
  const noticeItems = document.querySelectorAll('.notice-item');

  if (!noticeItems.length) return;

  let activeCategory = 'all';

  const applyFilters = () => {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    noticeItems.forEach(item => {
      const category = (item.getAttribute('data-category') || '').toLowerCase();
      const text = item.textContent.toLowerCase();

      const matchesCategory = (activeCategory === 'all' || category === activeCategory);
      const matchesSearch = (!query || text.includes(query));

      if (matchesCategory && matchesSearch) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });
  };

  chips.forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.preventDefault();
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = (chip.getAttribute('data-filter') || 'all').toLowerCase();
      applyFilters();
    });
  });

  if (searchInput) searchInput.addEventListener('input', applyFilters);
}

/* ==========================================================================
   6. Events Filter (Upcoming / Past / Category)
   ========================================================================== */
function initEventsFilter() {
  const chips = document.querySelectorAll('.event-filter-chip');
  const eventItems = document.querySelectorAll('.event-item-row');

  if (!eventItems.length) return;

  chips.forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.preventDefault();
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const filter = chip.getAttribute('data-filter') || 'all';

      eventItems.forEach(item => {
        const category = item.getAttribute('data-category') || '';
        const timing = item.getAttribute('data-timing') || '';

        if (filter === 'all' || filter === timing || filter.toLowerCase() === category.toLowerCase()) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   7. Accessible Tabs Component
   ========================================================================== */
function initTabs() {
  const tabContainers = document.querySelectorAll('.tab-container');

  tabContainers.forEach(container => {
    const tabs = container.querySelectorAll('[role="tab"]');
    const panels = container.querySelectorAll('[role="tabpanel"]');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.getAttribute('aria-controls');

        tabs.forEach(t => {
          t.setAttribute('aria-selected', 'false');
          t.classList.remove('active');
        });
        panels.forEach(p => {
          p.hidden = true;
          p.classList.remove('active');
        });

        tab.setAttribute('aria-selected', 'true');
        tab.classList.add('active');
        
        const targetPanel = container.querySelector(`#${targetId}`);
        if (targetPanel) {
          targetPanel.hidden = false;
          targetPanel.classList.add('active');
        }
      });
    });
  });
}

/* Helper Utilities */
function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
