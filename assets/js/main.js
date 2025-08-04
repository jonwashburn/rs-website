document.addEventListener("DOMContentLoaded", function() {
    // Find the placeholder element
    const headerPlaceholder = document.getElementById("header-placeholder");
    
    if (headerPlaceholder) {
        // Fetch the header HTML
        fetch('/_includes/header.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.text();
            })
            .then(data => {
                // Inject the header HTML into the placeholder
                headerPlaceholder.innerHTML = data;
            })
            .catch(error => {
                console.error('Error fetching header:', error);
                headerPlaceholder.innerHTML = "<p style='color:red;'>Error loading navigation.</p>";
            });
    }
});