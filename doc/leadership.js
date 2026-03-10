/* Build leadership from JSON + keep modal behavior and scroll lock */
(function () {
  const DATA_URL = "../ccc-leadership/leadership.json";

  // helpers
  const isBlank = v => !v || String(v).toLowerCase() === "nan" || String(v).trim() === "";
  const safeLink = v => (isBlank(v) ? "" : (/^https?:\/\//i.test(v) ? v : "https://" + v));
  const fixAvatarUrl = url => {
    if (!url) return "";
    // Handle relative paths
    if (url.startsWith('./')) {
      return url.replace('./leadership-photos/', '../ccc-leadership/leadership-photos/');
    }
    // turn github.com/.../blob/main/... into raw.githubusercontent.com/.../main/...
    const m = url.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)\/blob\/([^/]+)\/(.+)$/i);
    return m ? `https://raw.githubusercontent.com/${m[1]}/${m[2]}/${m[3]}/${m[4]}` : url;
  };

  function notifyParentModal(isOpen) {
    try { parent.postMessage({ type: 'leadership-modal', open: isOpen }, '*'); } catch (_) {}
  }
  function setModalOpenClass() {
    const open = !!(location.hash && document.querySelector(location.hash + '.modal'));
    document.body.classList.toggle('modal-open', open);
    notifyParentModal(open);
  }

  // lazy-load big image in modal + attach fallback
  function loadModalAvatar(modalEl) {
    if (!modalEl) return;
    const img = modalEl.querySelector('.modal__avatar');
    if (!img) return;

    // attach fallback handler once
    if (!img._fallbackBound) {
      img.addEventListener('error', function () {
        const fb = this.getAttribute('data-fallback');
        if (fb && this.src !== fb) this.src = fb;
      });
      img._fallbackBound = true;
    }

    if (!img.getAttribute('src')) {
      const url = img.getAttribute('data-src');
      if (url) img.src = fixAvatarUrl(url);
    }
  }

  // card + modal templates
  const cardHTML = p => `
    <div class="leadership-card" data-id="${p.id}" data-category="${p.category}">
      <img class="avatar"
           src="${fixAvatarUrl(p.avatar)}"
           alt="${p.name}" width="140" height="140" loading="lazy" />
      <h3 class="name">${p.name}</h3>
      <p class="role">${isBlank(p.role) ? "—" : p.role}</p>
      <p class="organization">${isBlank(p.organization) ? "—" : p.organization}</p>
      <p class="title">${isBlank(p.title) ? "—" : p.title}</p>
    </div>
  `;

  const modalHTML = p => `
    <section id="${p.id}-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="${p.id}-title">
      <a href="#" class="modal__backdrop" aria-hidden="true"></a>
      <div class="modal__card">
        <a href="#" class="modal__close" aria-label="Close">×</a>

        <div class="modal__avatar-wrap">
          <img class="modal__avatar"
               src=""
               data-src="${p.avatar}"
               alt="${p.name}" width="140" height="140" />
        </div>

        <div class="modal__header">
          <h3 id="${p.id}-title">${p.name}</h3>
          <p class="role">${isBlank(p.role) ? "—" : p.role}</p>
          <p class="organization">${isBlank(p.organization) ? "—" : p.organization}</p>
          <p class="title">${isBlank(p.title) ? "—" : p.title}</p>
          <p class="category">${isBlank(p.category) ? "—" : p.category}</p>
        </div>
        <div class="bio">${isBlank(p.bio) ? "—" : p.bio.replace(/\n/g, '<br>')}</div>
      </div>
    </section>
  `;

  async function init() {
    const grid = document.getElementById('leadership-grid');
    if (!grid) return;

    // fetch + normalize
    let people = [];
    try {
      const r = await fetch(DATA_URL, { cache: "no-store" });
      if (!r.ok) {
        console.error(`Failed to fetch JSON: HTTP ${r.status}`);
        console.error(`Attempted URL: ${DATA_URL}`);
        throw new Error(`HTTP ${r.status}`);
      }
      people = await r.json();
      console.log(`Loaded ${people.length} leadership entries`);
    } catch (e) {
      console.error("Failed to load leadership.json:", e);
      console.error("Make sure you're running from a web server, not file:// protocol");
      console.error("Try: python3 -m http.server 8000 (then visit http://localhost:8000/doc/leadership-embed.html)");
      // Show error message on page
      grid.innerHTML = `<div style="padding: 40px; text-align: center; color: #d00;">
        <h2>Error Loading Leadership Data</h2>
        <p>Failed to load leadership.json</p>
        <p style="font-size: 14px; color: #666;">${e.message}</p>
        <p style="font-size: 12px; color: #999; margin-top: 20px;">
          Note: This page must be served from a web server, not opened directly as a file.<br>
          Run: <code>python3 -m http.server 8000</code> then visit http://localhost:8000/doc/leadership-embed.html
        </p>
      </div>`;
      return;
    }

    // normalize avatar URLs + sort by name (defensive)
    people.forEach(p => { p.avatar = fixAvatarUrl(p.avatar); });
    people.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }));

    // Group by category
    const categories = {};
    people.forEach(p => {
      const cat = p.category || 'Other';
      if (!categories[cat]) categories[cat] = [];
      categories[cat].push(p);
    });

    // Define category display order and labels
    const categoryOrder = [
      { key: 'Governing Board', label: 'Governing Board' },
      { key: 'Committee Chairs', label: 'Outreach' },
      { key: 'Technical Advisory Council', label: 'Technical Advisory Council' },
      { key: 'Staff', label: 'Staff' },
      { key: 'Budget Committee', label: 'Budget Committee' }
    ];

    // Inject cards grouped by category in specified order
    const frag = document.createDocumentFragment();
    categoryOrder.forEach(({ key, label }) => {
      if (!categories[key] || categories[key].length === 0) return;
      
      const categoryDiv = document.createElement('div');
      categoryDiv.className = 'category-section';
      const categoryTitle = document.createElement('h2');
      categoryTitle.textContent = label;
      categoryDiv.appendChild(categoryTitle);
      
      const categoryGrid = document.createElement('div');
      categoryGrid.className = 'leadership-grid';
      
      const catFrag = document.createDocumentFragment();
      categories[key].forEach(p => {
        const t = document.createElement('template');
        t.innerHTML = cardHTML(p).trim();
        catFrag.appendChild(t.content.firstElementChild);
      });
      categoryGrid.replaceChildren(catFrag);
      categoryDiv.appendChild(categoryGrid);
      frag.appendChild(categoryDiv);
    });
    grid.replaceChildren(frag);

    // attach fallback to card avatars
    grid.querySelectorAll('img.avatar').forEach(img => {
      if (img._fallbackBound) return;
      img.addEventListener('error', function () {
        console.warn('Failed to load avatar:', this.src);
      });
      img._fallbackBound = true;
    });

    // inject modals (outside page-content so blur doesn't affect them)
    const mfrag = document.createDocumentFragment();
    people.forEach(p => {
      const t = document.createElement('template');
      t.innerHTML = modalHTML(p).trim();
      mfrag.appendChild(t.content.firstElementChild);
    });
    document.body.appendChild(mfrag);

    // open/close behavior
    document.addEventListener('click', e => {
      const card = e.target.closest('.leadership-card');
      if (!card) return;
      const id = card.getAttribute('data-id');
      location.hash = id + '-modal';
      loadModalAvatar(document.getElementById(id + '-modal'));
      setModalOpenClass();
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && location.hash) {
        location.hash = '';
        setModalOpenClass();
      }
    });

    window.addEventListener('hashchange', () => {
      setModalOpenClass();
      if (location.hash) loadModalAvatar(document.querySelector(location.hash + '.modal'));
    });

    // initial state (handles shared hash links)
    setModalOpenClass();
    if (location.hash) loadModalAvatar(document.querySelector(location.hash + '.modal'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

