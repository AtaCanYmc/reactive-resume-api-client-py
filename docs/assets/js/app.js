// Custom Documentation Client Logic for rxresume-python

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initCodeTabs();
  initCopyButtons();
  initSearch();
  initScrollSpy();
  initMobileNav();
});

// 1. Theme Management (Light / Dark / System)
function initTheme() {
  const themeBtn = document.getElementById('theme-toggle');
  const html = document.documentElement;

  // Retrieve saved preference or check OS
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    html.setAttribute('data-theme', savedTheme);
  }

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', nextTheme);
      localStorage.setItem('theme', nextTheme);
      updateThemeIcon(nextTheme);
    });
  }

  const currentTheme = html.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  updateThemeIcon(currentTheme);
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('theme-icon');
  if (!icon) return;
  if (theme === 'dark') {
    // Show sun icon when in dark mode
    icon.innerHTML = '&#9728;&#65039;';
    icon.title = 'Switch to light mode';
  } else {
    // Show moon icon when in light mode
    icon.innerHTML = '&#127769;';
    icon.title = 'Switch to dark mode';
  }
}

// 2. Tabbed Code Snippet Switcher (Sync, Async, CLI)
function initCodeTabs() {
  const tabContainers = document.querySelectorAll('.code-block');

  tabContainers.forEach(container => {
    const tabs = container.querySelectorAll('.code-tab');
    const panes = container.querySelectorAll('.code-pane');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.getAttribute('data-tab');

        tabs.forEach(t => t.classList.remove('active'));
        panes.forEach(p => p.style.display = 'none');

        tab.classList.add('active');
        const activePane = container.querySelector(`.code-pane[data-pane="${target}"]`);
        if (activePane) {
          activePane.style.display = 'block';
        }
      });
    });
  });
}

// 3. One-Click Copy Buttons
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('.copy-btn');

  copyButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const parent = btn.closest('.code-block');
      if (!parent) return;

      // Find active code pane or single pre
      const activePane = parent.querySelector('.code-pane:not([style*="display: none"])') || parent;
      const codeEl = activePane.querySelector('code') || activePane.querySelector('pre');
      if (!codeEl) return;

      const text = codeEl.innerText.trim();
      try {
        await navigator.clipboard.writeText(text);
        const originalText = btn.innerHTML;
        btn.innerHTML = '&#10003; Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.classList.remove('copied');
        }, 2000);
      } catch (err) {
        console.error('Clipboard copy failed:', err);
      }
    });
  });
}

// 4. Instant Search & Topic Filter
function initSearch() {
  const searchInput = document.getElementById('doc-search');
  if (!searchInput) return;

  const sections = document.querySelectorAll('.doc-section');
  const navLinks = document.querySelectorAll('.nav-link');

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();

    sections.forEach(section => {
      const text = section.innerText.toLowerCase();
      const match = text.includes(query);
      section.style.display = match ? 'block' : 'none';
    });

    navLinks.forEach(link => {
      const targetId = link.getAttribute('href')?.replace('#', '');
      const targetSec = document.getElementById(targetId);
      if (targetSec) {
        link.style.display = targetSec.style.display === 'none' ? 'none' : 'flex';
      }
    });
  });
}

// 5. ScrollSpy Indicator for Sidebar Links
function initScrollSpy() {
  const sections = document.querySelectorAll('.doc-section');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let currentId = '';
    const scrollPos = window.scrollY + 120;

    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        currentId = sec.id;
      }
    });

    if (currentId) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentId}`) {
          link.classList.add('active');
        }
      });
    }
  });
}

// 6. Mobile Sidebar Drawer Toggle
function initMobileNav() {
  const toggleBtn = document.getElementById('mobile-toggle');
  const sidebar = document.querySelector('.sidebar');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    // Close when clicking outside or clicking link
    document.addEventListener('click', (e) => {
      if (!sidebar.contains(e.target) && e.target !== toggleBtn) {
        sidebar.classList.remove('open');
      }
    });

    sidebar.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        sidebar.classList.remove('open');
      });
    });
  }
}
