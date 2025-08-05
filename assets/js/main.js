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