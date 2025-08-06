document.addEventListener("DOMContentLoaded", function() {

    function toggleMobileMenu() {
        const nav = document.getElementById('globalNav');
        if (nav) {
            nav.classList.toggle('active');
        }
    }

    function setupHeaderEventListeners() {
        const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
        if (mobileMenuButton) {
            mobileMenuButton.addEventListener('click', toggleMobileMenu);
        }

        const dropdowns = document.querySelectorAll('.global-nav .dropdown');
        dropdowns.forEach(dropdown => {
            const dropbtn = dropdown.querySelector('.dropbtn');
            if (dropbtn) {
                dropbtn.addEventListener('click', function(event) {
                    if (window.innerWidth <= 768) {
                        event.preventDefault();
                        // Close other open dropdowns
                        dropdowns.forEach(otherDropdown => {
                            if (otherDropdown !== dropdown) {
                                otherDropdown.classList.remove('active');
                            }
                        });
                        dropdown.classList.toggle('active');
                    }
                });
            }
        });
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
