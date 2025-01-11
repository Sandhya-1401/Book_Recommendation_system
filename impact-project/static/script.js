// Function to toggle the visibility of the menu card
function toggleMenu() {
    const menuCard = document.getElementById('menu-card'); // Get the menu card element by its ID
    if (menuCard) {
        // Toggle the display style between 'flex' (visible) and 'none' (hidden)
        menuCard.style.display = (menuCard.style.display === 'flex') ? 'none' : 'flex';
    }
}

// Wait until the DOM content is fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.querySelector('form'); // Get the search form element
    const searchBox = document.querySelector('.search-box'); // Get the search input box element
    const searchResultContainer = document.querySelector('.search-result'); // Get the container for displaying search results
    const menuCard = document.getElementById('menu-card'); // Get the menu card element
    const categoriesWrapper = document.querySelector('.categories-wrapper'); // Get the categories wrapper (currently unused)
    const prevBtn = document.querySelector('.prev-btn'); // Get the previous button (currently unused)
    const nextBtn = document.querySelector('.next-btn'); // Get the next button (currently unused)

    // Search form functionality
    if (searchForm && searchBox && searchResultContainer) {
        searchForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent the form from submitting the traditional way

            const userInput = searchBox.value.trim(); // Get the user's input and trim extra spaces
            if (!userInput) {
                alert('Please enter a book name to search!'); // Alert the user if the input is empty
                return; // Stop further execution
            }

            try {
                // Send the user's search input to the server via a POST request
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }, // Specify JSON content type
                    body: JSON.stringify({ user_input: userInput }) // Include the user input in the request body
                });

                const result = await response.json(); // Parse the server's response as JSON
                searchResultContainer.innerHTML = ''; // Clear any previous search results

                if (result.found) {
                    // If the book is found, update the DOM with the book's details
                    searchResultContainer.innerHTML = `
                        <div class="book-container" style="
                            display: flex; 
                            flex-direction: column; 
                            align-items: center; 
                            justify-content: center; 
                            height: 100%; 
                            text-align: center;">
                            <img src="${result.image}" alt="Book Cover" class="book-image" style="
                                width: 120px; 
                                height: 180px; 
                                margin-bottom: 15px; 
                                object-fit: cover;">
                            <h3 style="margin: 10px 0;">${result.title}</h3>
                            <h3 style="margin: 10px 0; font-size: 1rem;">Author: ${result.author}</h3>
                        </div>
                    `;
                } else {
                    // If the book is not found, display a "Book Not Found" message
                    searchResultContainer.innerHTML = `
                        <div style="text-align: center; width: 100%;">
                            <h3>Book Not Found !!</h3>
                            <h3>Sorry</h3>
                        </div>
                    `;
                }

                searchResultContainer.classList.add('active'); // Show the search results container
            } catch (error) {
                console.error('Error during search:', error); // Log the error to the console
                alert('An error occurred while searching. Please try again later.'); // Alert the user about the error
            }
        });
    }

    // Click event listener to hide search results or menu card when clicking outside
    document.addEventListener('click', (event) => {
        const isClickInsideSearchResult = searchResultContainer?.contains(event.target); // Check if the click is inside the search results container
        const isClickInsideMenuCard = menuCard?.contains(event.target); // Check if the click is inside the menu card
        const isClickMenuIcon = event.target.classList.contains('menu-icon'); // Check if the click is on the menu icon

        // Hide the search results container if the click is outside it
        if (searchResultContainer && !isClickInsideSearchResult) {
            searchResultContainer.innerHTML = ''; // Clear the search results
            searchResultContainer.classList.remove('active'); // Remove the active class to hide it
        }

        // Hide the menu card if the click is outside it and not on the menu icon
        if (menuCard && !isClickInsideMenuCard && !isClickMenuIcon) {
            menuCard.style.display = 'none'; // Hide the menu card
        }
    });
});
