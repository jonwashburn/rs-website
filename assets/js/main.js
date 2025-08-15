document.addEventListener("DOMContentLoaded", function() {

    // Force-refresh critical stylesheets across the site to avoid CDN/browser cache staleness
    function bumpStylesheetCache() {
        try {
            const versionTag = 'v=20250813-1';
            const targets = [
                '/assets/css/main.css',
                '/assets/css/site-template.css',
                '/assets/css/academic-style.css',
                '/assets/css/encyclopedia.css'
            ];
            const links = document.querySelectorAll('link[rel="stylesheet"][href]');
            links.forEach(link => {
                const href = link.getAttribute('href');
                if (!href) return;
                const isTarget = targets.some(t => href.endsWith(t) || href.includes(t + '?'));
                if (!isTarget) return;
                const base = href.split('?')[0];
                const next = `${base}?${versionTag}`;
                if (href !== next) {
                    link.setAttribute('href', next);
                }
            });
        } catch (_) {}
    }

    // Run immediately to swap in fresh CSS post-load
    bumpStylesheetCache();

    function toggleMobileMenu() {
        const nav = document.getElementById('globalNav');
        if (!nav) return;

        nav.classList.toggle('active');

        // Ensure the menu can grow beyond initial measurement and scroll within viewport
        const list = nav.querySelector('ul');
        if (list) {
            if (nav.classList.contains('active')) {
                list.style.maxHeight = 'calc(100vh - 3.5rem)';
                list.style.overflowY = 'auto';
            } else {
                list.style.maxHeight = '0px';
                list.style.overflowY = 'hidden';
            }
        }

        // Animate hamburger menu
        const button = document.querySelector('.mobile-menu-toggle');
        if (button) {
            button.classList.toggle('active');
        }
    }

    function setupHeaderEventListeners() {
        // Use a small delay to ensure DOM is fully ready
        setTimeout(() => {
            const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
            console.log('Setting up mobile menu button:', mobileMenuButton); // Debug log
            
            if (mobileMenuButton) {
                // Remove any existing listeners to prevent duplicates
                mobileMenuButton.removeEventListener('click', toggleMobileMenu);
                mobileMenuButton.addEventListener('click', toggleMobileMenu);
                // Expand clickable area to surrounding box as fallback
                mobileMenuButton.addEventListener('touchstart', (e) => { e.stopPropagation(); }, { passive: true });
            }

            const dropdowns = document.querySelectorAll('.global-nav .dropdown');
            console.log('Found dropdowns:', dropdowns.length); // Debug log
            
            dropdowns.forEach(dropdown => {
                const dropbtn = dropdown.querySelector('.dropbtn');
                if (dropbtn) {
                    // Remove existing listeners to prevent duplicates
                    dropbtn.removeEventListener('click', handleDropdownClick);
                    dropbtn.addEventListener('click', handleDropdownClick, { passive: false, capture: true });

                    // Also allow tapping the caret/arrow region to open
                    dropbtn.removeEventListener('touchstart', handleDropdownClick);
                    dropbtn.addEventListener('touchstart', handleDropdownClick, { passive: false, capture: true });
                }
            });
        }, 100);
    }

    function handleDropdownClick(event) {
        console.log('Dropdown clicked, window width:', window.innerWidth); // Debug log
        if (window.innerWidth <= 768) {
            event.preventDefault();
            event.stopPropagation();
            
            // Get the dropdown element (handle clicks on children of dropbtn too)
            const dropbtn = event.target.closest('.dropbtn');
            const dropdown = dropbtn ? dropbtn.closest('.dropdown') : null;
            
            console.log('Dropdown element:', dropdown); // Debug log
            
            if (dropdown) {
                // Close other open dropdowns
                const allDropdowns = document.querySelectorAll('.global-nav .dropdown');
                allDropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                        const otherContent = otherDropdown.querySelector('.dropdown-content');
                        if (otherContent) {
                            otherContent.style.maxHeight = '0px';
                        }
                    }
                });
                
                // Toggle this dropdown
                dropdown.classList.toggle('active');
                console.log('Dropdown active state:', dropdown.classList.contains('active')); // Debug log
                
                // Animate the dropdown content
                const dropdownContent = dropdown.querySelector('.dropdown-content');
                if (dropdownContent) {
                    if (dropdown.classList.contains('active')) {
                        dropdownContent.style.maxHeight = dropdownContent.scrollHeight + 'px';
                    } else {
                        dropdownContent.style.maxHeight = '0px';
                    }
                }

                // After expanding/collapsing a submenu, ensure the outer list can scroll to fit
                const navList = document.querySelector('#globalNav ul');
                if (navList && document.getElementById('globalNav').classList.contains('active')) {
                    navList.style.maxHeight = 'calc(100vh - 3.5rem)';
                    navList.style.overflowY = 'auto';
                }
            }
        }
    }

    function executeScripts(container) {
        try {
            const scripts = container.querySelectorAll('script');
            scripts.forEach((oldScript) => {
                const newScript = document.createElement('script');
                // Copy attributes
                for (let i = 0; i < oldScript.attributes.length; i += 1) {
                    const attr = oldScript.attributes[i];
                    newScript.setAttribute(attr.name, attr.value);
                }
                if (oldScript.src) {
                    newScript.src = oldScript.src;
                } else {
                    newScript.textContent = oldScript.textContent;
                }
                // Replace to trigger execution
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        } catch (e) {
            // Silently ignore script execution errors in includes
        }
    }

    function fetchAndInject(url, placeholderId) {
        const placeholder = document.getElementById(placeholderId);
        if (placeholder) {
            // Bust caches aggressively to avoid stale includes
            const cacheBustedUrl = `${url}${url.includes('?') ? '&' : '?'}v=${Date.now()}`;
            fetch(cacheBustedUrl, { cache: 'no-store' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.text();
                })
                .then(data => {
                    placeholder.innerHTML = data;
                    // Ensure any scripts inside the included HTML execute
                    executeScripts(placeholder);
                    if (placeholderId === 'header-placeholder') {
                        setupHeaderEventListeners();
                        // Inject sitewide banner only after header is present to avoid race conditions
                        const base = getBasePath();
                        const bannerTarget = document.getElementById('sitewide-banner-placeholder');
                        if (bannerTarget) {
                            fetchAndInject(base + '_includes/banner.html', 'sitewide-banner-placeholder');
                        }
                    }
                })
                .catch(error => {
                    console.error(`Error fetching ${url}:`, error);
                    placeholder.innerHTML = `<p style='color:red;'>Error loading content.</p>`;
                });
        }
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768) {
            // Only close if we're not clicking on a dropdown button
            if (!event.target.closest('.dropbtn') && !event.target.closest('.dropdown-content')) {
                const activeDropdowns = document.querySelectorAll('.dropdown.active');
                activeDropdowns.forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            }
        }
    });

    // Robust base path detection (works for any depth)
    function getBasePath() {
        const pathname = window.location.pathname;
        if (pathname === '/' || pathname === '' || pathname === '/index.html') {
            return '';
        }
        const segments = pathname.split('/').filter(Boolean);
        const lastSegment = segments[segments.length - 1] || '';
        const isFile = lastSegment.includes('.');
        const depth = isFile ? segments.length - 1 : segments.length;
        if (depth <= 0) return '';
        return '../'.repeat(depth);
    }

    const basePath = getBasePath();
    fetchAndInject(basePath + '_includes/header.html', 'header-placeholder');
    // Footer can be injected immediately
    fetchAndInject(basePath + '_includes/footer.html', 'footer-placeholder');
    
    // MathJax loader (guarded). Use both $...$ and \(...\) like RH paper; include $$ and \[\] for display.
    if (!document.getElementById('MathJax-script')) {
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
        // Load MathJax (SVG renderer for fidelity)
        (function () {
            var pf = document.createElement('script');
            pf.src = 'https://polyfill.io/v3/polyfill.min.js?features=es6';
            document.head.appendChild(pf);
            pf.onload = function() {
                var mj = document.createElement('script');
                mj.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
                mj.async = true;
                mj.id = 'MathJax-script';
                document.head.appendChild(mj);
            };
        })();
    }

    // Ensure <math-note> and .math-note content has TeX delimiters if missing
    function wrapMathNotesWithDelimiters() {
        try {
            const nodes = document.querySelectorAll('math-note, .math-note');
            nodes.forEach(node => {
                // Skip if already contains any TeX delimiters
                const html = node.innerHTML.trim();
                const hasDelims = /\\\(|\\\)|\$|\\\[|\\\]/.test(html);
                if (!hasDelims && html.length > 0) {
                    // Wrap entire content as inline TeX
                    node.innerHTML = `\\(${html}\\)`;
                }
            });
        } catch(_) {}
    }

    // Robust typeset trigger akin to RH page
    function typesetWhenReady(){
        try {
            wrapMathNotesWithDelimiters();
            if (window.MathJax && typeof MathJax.typesetPromise === 'function') { MathJax.typesetPromise(); return; }
            if (window.MathJax && typeof MathJax.typeset === 'function') { MathJax.typeset(); return; }
            const mj = document.getElementById('MathJax-script');
            if (mj && !mj.dataset.bound) {
                mj.dataset.bound = '1';
                mj.addEventListener('load', function(){
                    wrapMathNotesWithDelimiters();
                    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
                });
                return;
            }
            setTimeout(typesetWhenReady, 250);
        } catch(_) {}
    }
    typesetWhenReady();
});
