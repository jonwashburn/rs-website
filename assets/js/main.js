document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch and inject HTML content
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
                    // After injecting header, re-run script logic if needed
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

    // Load header and footer
    fetchAndInject('/_includes/header.html', 'header-placeholder');
    fetchAndInject('/_includes/footer.html', 'footer-placeholder');
});

function toggleMobileMenu() {
    const nav = document.getElementById('globalNav');
    if (nav) {
        nav.classList.toggle('active');
    }
}

function setupHeaderEventListeners() {
    const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
    if (mobileMenuButton) {
        mobileMenuButton.onclick = toggleMobileMenu;
    }

    const dropdowns = document.querySelectorAll('.dropdown > .dropbtn');
    dropdowns.forEach(dropbtn => {
        dropbtn.onclick = function(event) {
            // Use this to handle clicks on mobile for dropdowns
            if (window.innerWidth <= 768) {
                event.preventDefault();
                const dropdown = this.parentElement;
                dropdown.classList.toggle('active');
            }
        }
    });
}
