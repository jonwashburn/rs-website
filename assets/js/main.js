document.addEventListener("DOMContentLoaded", function() {

    function toggleMobileMenu() {
        const nav = document.getElementById('globalNav');
        if (nav) {
            nav.classList.toggle('active');
            
            // Animate hamburger menu
            const button = document.querySelector('.mobile-menu-toggle');
            if (button) {
                button.classList.toggle('active');
            }
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
                    dropbtn.addEventListener('click', handleDropdownClick);
                }
            });
        }, 100);
    }

    function handleDropdownClick(event) {
        if (window.innerWidth <= 768) {
            event.preventDefault();
            const dropdown = event.target.closest('.dropdown');
            
            // Close other open dropdowns
            const allDropdowns = document.querySelectorAll('.global-nav .dropdown');
            allDropdowns.forEach(otherDropdown => {
                if (otherDropdown !== dropdown) {
                    otherDropdown.classList.remove('active');
                }
            });
            
            // Toggle this dropdown
            dropdown.classList.toggle('active');
        }
    }

    function fetchAndInject(url, placeholderId) {
        const placeholder = document.getElementById(placeholderId);
        if (placeholder) {
            fetch(url)
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

    fetchAndInject('/_includes/header.html', 'header-placeholder');
    fetchAndInject('/_includes/footer.html', 'footer-placeholder');
});
