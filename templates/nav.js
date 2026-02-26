document.addEventListener('DOMContentLoaded', function () {
  // Inject improved CSS for active states and uniform buttons
  var style = document.createElement('style');
  style.textContent = "\n    :root{--theme:#106EBE;}\n    .sidebar-active{background-color:var(--theme)!important;color:#fff!important;padding:0.625rem 1rem!important;border-radius:0.75rem!important;box-shadow:0 8px 20px rgba(16,110,190,0.16);display:flex!important;align-items:center!important;}\n    .sidebar-active .material-symbols-outlined{color:#fff!important;}\n    .sidebar-active span{color:#fff!important;}\n    .bottom-active{background-color:var(--theme)!important;color:#fff!important;padding:0.5rem 0.875rem!important;border-radius:0.6rem!important;display:inline-flex!important;align-items:center!important;box-shadow:0 8px 20px rgba(16,110,190,0.16);}\n    .bottom-active .material-symbols-outlined{color:#fff!important;}\n    .uniform-btn{min-height:2.75rem;padding:0.625rem 1rem;border-radius:0.625rem;display:inline-flex;align-items:center;gap:0.5rem;font-size:1rem;font-weight:700;background-color:var(--theme);color:#fff;}\n    /* ensure anchors in sidebar expand full width when active */\n    aside a{display:flex;align-items:center;gap:0.75rem;font-size:0.875rem;}\n    /* mobile wash support — anchors marked with data-canwash get a soft background on small screens */\n    @media (max-width:1023px){\n      a[data-canwash=\"true\"]{background-color:rgba(16,110,190,0.04);border-radius:0.6rem;padding:0.5rem 0.875rem;display:inline-flex;align-items:center;gap:0.5rem;}\n      a[data-canwash=\"true\"] .material-symbols-outlined{color:var(--theme)!important;}\n    }\n  ";
  document.head.appendChild(style);

  // ... (rest of the file logic preserved)

  /* THEME HANDLER: inject variables, apply saved theme, and add a toggle */
  try {
    var themeStyle = document.createElement('style');
    // Add theme-related CSS variables on the fly (light + dark)
    themeStyle.textContent = `
      :root {
        --bg: #f8fafc;
        --surface: #ffffff;
        --muted: #64748b;
        --text: #0f172a;
        --primary: #106EBE;
        --primary-600: #0d5a9c;
        --accent: #0FFCBE;
      }
      [data-theme="dark"] {
        --bg: #0f172a;
        --surface: #1e293b;
        --muted: #94a3b8;
        --text: #f1f5f9;
        --primary: #106EBE;
        --primary-600: #0d5a9c;
        --accent: #0FFCBE;
      }
      body { background-color: var(--bg) !important; color: var(--text) !important; font-size: 1rem !important; }
      .bg-surface { background-color: var(--surface) !important; }
      .text-muted { color: var(--muted) !important; }
      .btn-theme { 
        position: fixed; right: 1rem; bottom: 5rem; z-index: 9999; 
        background: var(--surface); border-radius: 9999px; padding: 0.5rem; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.05); 
        cursor: pointer; transition: all 0.2s;
      }
      .btn-theme:hover { transform: scale(1.1); }
      .sidebar-active{ background-color: var(--primary) !important; }
      .uniform-btn{ background-color: var(--primary) !important; color: white !important; }
    `;
    document.head.appendChild(themeStyle);

    // Theme helpers
    function getSavedTheme() { try { return localStorage.getItem('site-theme') || null } catch (e) { return null } }
    function saveTheme(t) { try { localStorage.setItem('site-theme', t) } catch (e) { } }
    function applyTheme(t) { if (!t) return; document.documentElement.setAttribute('data-theme', t); }

    var saved = getSavedTheme();
    if (!saved) {
      // default: prefer user's system preference
      var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      saved = prefersDark ? 'dark' : 'light';
    }
    applyTheme(saved);

    // Inject a floating theme toggle button (if not present)
    if (!document.querySelector('.btn-theme')) {
      var btn = document.createElement('button');
      btn.className = 'btn-theme';
      btn.setAttribute('aria-label', 'Toggle theme');
      btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;line-height:1">light_mode</span>';
      btn.addEventListener('click', function () {
        var cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        var next = cur === 'dark' ? 'light' : 'dark';
        applyTheme(next); saveTheme(next);
        // update icon
        btn.innerHTML = next === 'dark' ? '<span class="material-symbols-outlined" style="font-size:20px;line-height:1">dark_mode</span>' : '<span class="material-symbols-outlined" style="font-size:20px;line-height:1">light_mode</span>';
      });
      // set initial icon to match current theme
      if (document.documentElement.getAttribute('data-theme') === 'dark') btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;line-height:1">dark_mode</span>';
      document.body.appendChild(btn);
    }
  } catch (themeErr) { /* non-fatal */ }

  // Global Identity Sync (Image, Name, Role)
  (async function () {
    const drId = sessionStorage.getItem('doctor_id');
    if (!drId) return;

    // 1. Fast-track from session storage (minimize flicker)
    const cachedImg = sessionStorage.getItem('doctor_profile_image');
    const cachedName = sessionStorage.getItem('doctor_name');

    if (cachedImg) {
      document.querySelectorAll('aside img, header img, #profile-img-preview, #nav-profile-img').forEach(img => {
        img.src = cachedImg;
      });
    }

    if (cachedName) {
      const navName = document.getElementById('nav-doctor-name');
      if (navName) navName.textContent = cachedName;

      const welcomeHeading = document.getElementById('welcomeHeading');
      if (welcomeHeading) {
        const displayName = cachedName.includes('Dr.') ? cachedName : cachedName.split(' ')[0];
        welcomeHeading.textContent = `Welcome, ${displayName}`;
      }
    }

    // 2. Background Sync with Server
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/doctor/profile?doctorid=${drId}`);
      const res = await response.json();
      if (res.success && res.data) {
        const dr = res.data;

        // Sync Profile Image (Server Authority)
        if (dr.profile_image) {
          if (cachedImg !== dr.profile_image) {
            sessionStorage.setItem('doctor_profile_image', dr.profile_image);
            document.querySelectorAll('aside img, header img, #profile-img-preview, #nav-profile-img').forEach(img => {
              img.src = dr.profile_image;
            });
          }
        }

        // Sync Name (Server Authority)
        if (dr.fullname) {
          if (cachedName !== dr.fullname) {
            sessionStorage.setItem('doctor_name', dr.fullname);
            const navName = document.getElementById('nav-doctor-name');
            if (navName) navName.textContent = dr.fullname;

            const welcomeHeading = document.getElementById('welcomeHeading');
            if (welcomeHeading) {
              const displayName = dr.fullname.includes('Dr.') ? dr.fullname : dr.fullname.split(' ')[0];
              welcomeHeading.textContent = `Welcome, ${displayName}`;
            }
          }
        }

        // Sync Clinical Role
        if (dr.specialization) {
          const navRole = document.getElementById('nav-doctor-role');
          if (navRole) navRole.textContent = dr.specialization.charAt(0).toUpperCase() + dr.specialization.slice(1);
        }

        // Sync Clinical Details (Specialization & Clinic)
        const welcomeContext = document.getElementById('welcomeContext');
        if (welcomeContext && dr.clinic_name && dr.specialization) {
          welcomeContext.innerHTML = `
            <span class="material-symbols-outlined text-sm">medical_services</span>
            ${dr.clinic_name} • ${dr.specialization.charAt(0).toUpperCase() + dr.specialization.slice(1)}
          `;
        }
      }
    } catch (e) {
      console.warn('Identity sync failed');
    }
  })();
});
