"use strict";

document.addEventListener('DOMContentLoaded', () => {
    console.log('JS loaded!');

    // ======== Элементы фильтров ========
    const filterName = document.getElementById('filter-name');
    const filterAuthor = document.getElementById('filter-author');
    const filterGenre = document.getElementById('filter-genre');
    const filterBtn = document.getElementById('filter-btn'); // кнопка фильтрации

    // ======== Функция фильтрации таблицы ========
    function filterBooksTable() {
        const nameFilter = (filterName?.value || '').toLowerCase();
        const authorFilter = (filterAuthor?.value || '').toLowerCase();
        const genreFilter = (filterGenre?.value || '').toLowerCase();

        const tbody = document.querySelector('#books-table tbody');
        const rows = tbody.querySelectorAll('tr');

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length < 7) return;

            const name = (cells[1].textContent || '').toLowerCase();
            const author = (cells[2].textContent || '').toLowerCase();
            const genre = (cells[3].textContent || '').toLowerCase();

            const matches =
                (nameFilter ? name.includes(nameFilter) : true) &&
                (authorFilter ? author.includes(authorFilter) : true) &&
                (genreFilter ? genre.includes(genreFilter) : true);

            row.style.display = matches ? '' : 'none';
        });
    }

    // ======== Обработчики фильтрации ========
    filterBtn?.addEventListener('click', filterBooksTable);

    // Фильтруем в реальном времени при вводе
    filterName?.addEventListener('input', filterBooksTable);
    filterAuthor?.addEventListener('input', filterBooksTable);
    filterGenre?.addEventListener('input', filterBooksTable);

    // ======== Загрузка всех книг ========
    async function fetchBooks() {
        try {
            const response = await fetch('/api/books/', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            if (response.ok) {
                const books = await response.json();
                populateBooksTable(books); // передаем массив в функцию
            } else {
                console.error('Error fetching books');
            }
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    }

    // ======== Заполнение таблицы книг ========
    function populateBooksTable(books) {
        const tbody = document.querySelector('#books-table tbody');
        tbody.innerHTML = ''; // очищаем таблицу

        if (books.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No books found</td></tr>';
            return;
        }

        books.forEach(book => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${book.id}</td>
                <td>${book.book_name}</td>
                <td>${book.author}</td>
                <td>${book.genre}</td>
                <td>${book.date_issue}</td>
                <td>$${book.price.toFixed(2)}</td>
                <td></td> <!-- сюда добавим кнопку Delete -->
            `;

            const deleteTd = tr.querySelector('td:last-child');
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'btn btn-danger btn-sm';
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', async () => {
                if (!confirm(`Are you sure you want to delete book ID ${book.id}?`)) return;

                try {
                    const response = await fetch(`/api/books/${book.id}`, { method: 'DELETE' });
                    if (response.ok) {
                        tr.remove();
                        alert(`Book ID ${book.id} deleted successfully.`);
                    } else {
                        const error = await response.json();
                        alert(`Error: ${error.detail}`);
                    }
                } catch (err) {
                    console.error('Error deleting book:', err);
                }
            });

            deleteTd.appendChild(deleteBtn);
            tbody.appendChild(tr);
        });

        // Применяем фильтр после заполнения таблицы
        filterBooksTable();
    }

    // ======== Создание книги ========
    const createForm = document.getElementById('create-book-form');
    createForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const book = {
            book_name: document.getElementById('book_name').value,
            author: document.getElementById('author').value,
            genre: document.getElementById('genre').value,
            date_issue: document.getElementById('date_issue').value,
            price: parseFloat(document.getElementById('price').value),
        };

        try {
            const response = await fetch('/api/books/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(book),
            });

            if (response.ok) {
                const newBook = await response.json();
                alert(`Book created: ${newBook.book_name} by ${newBook.author}`);
                createForm.reset();
                fetchBooks(); // обновляем таблицу
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        } catch (error) {
            console.error('Error creating book:', error);
        }
    });

    // ======== Инициализация ========
    fetchBooks();
});
