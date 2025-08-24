document.addEventListener("DOMContentLoaded", function() {
    const bookThumbnails = document.querySelectorAll(".book-thumbnail");

    bookThumbnails.forEach(thumbnail => {
        const isbn = thumbnail.dataset.isbn;

        console.log("Fetching cover for ISBN:", isbn);

        if (isbn) {
            fetch(`https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`)
                .then(response => response.json())
                .then(data => {
                    if (data.items && data.items.length > 0) {
                        const coverImage = data.items[0].volumeInfo.imageLinks?.thumbnail;
                        if (coverImage) {
                            thumbnail.src = coverImage;
                        }
                    }
                })
                .catch(error => console.error("Error fetching book cover for ISBN:", isbn, "ERROR:", error));
        }
       
    });

});