document.addEventListener("DOMContentLoaded", function() {

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
            }

            const dropdowns = document.querySelectorAll('.global-nav .dropdown');
            console.log('Found dropdowns:', dropdowns.length); // Debug log
            
            dropdowns.forEach(dropdown => {
                const dropbtn = dropdown.querySelector('.dropbtn');
                if (dropbtn) {
                    // Remove existing listeners to prevent duplicates
                    dropbtn.removeEventListener('click', handleDropdownClick);
                    dropbtn.addEventListener('click', handleDropdownClick, { passive: false });

                    // Also allow tapping the caret/arrow region to open
                    dropbtn.removeEventListener('touchstart', handleDropdownClick);
                    dropbtn.addEventListener('touchstart', handleDropdownClick, { passive: false });
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
                    if (placeholderId === 'header-placeholder') {
                        setupHeaderEventListeners();
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
    fetchAndInject(basePath + '_includes/footer.html', 'footer-placeholder');
});
