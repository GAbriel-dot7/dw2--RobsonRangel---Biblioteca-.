// scripts.js - Biblioteca Escolar
class BibliotecaApp {
    constructor() {
        this.books = [];
        this.filteredBooks = [];
        this.currentPage = 1;
        this.booksPerPage = 10;
        this.currentFilters = {
            search: '',
            genres: [],
            yearMin: '',
            yearMax: '',
            status: 'todos'
        };
        this.currentSort = this.loadSortPreference();
        this.apiBase = 'http://localhost:8000/api';
        
        this.init();
    }

    // Inicialização
    init() {
        this.bindEvents();
        this.setupKeyboardShortcuts();
        this.loadBooks();
        this.restoreSortUI();
    }

    bindEvents() {
        // Busca
        const searchInput = document.getElementById('search-books');
        searchInput.addEventListener('input', this.debounce((e) => {
            this.currentFilters.search = e.target.value;
            this.applyFilters();
        }, 300));

        // Filtros
        this.bindFilterEvents();
        
        // Modais
        this.bindModalEvents();
        
        // Formulários
        this.bindFormEvents();
        
        // Sorting
        this.bindSortEvents();
        
        // Export
        this.bindExportEvents();
        
        // Clear filters
        document.getElementById('clear-filters').addEventListener('click', () => {
            this.clearAllFilters();
        });
    }

    bindFilterEvents() {
        // Filtros de gênero
        const genreCheckboxes = document.querySelectorAll('.filter-checkbox input[type="checkbox"]');
        genreCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const genre = e.target.value;
                if (e.target.checked) {
                    this.currentFilters.genres.push(genre);
                } else {
                    this.currentFilters.genres = this.currentFilters.genres.filter(g => g !== genre);
                }
                this.applyFilters();
            });
        });

        // Filtros de ano
        const yearMin = document.getElementById('year-min');
        const yearMax = document.getElementById('year-max');
        
        yearMin.addEventListener('input', this.debounce((e) => {
            this.currentFilters.yearMin = e.target.value;
            this.applyFilters();
        }, 500));
        
        yearMax.addEventListener('input', this.debounce((e) => {
            this.currentFilters.yearMax = e.target.value;
            this.applyFilters();
        }, 500));

        // Filtros de status
        const statusRadios = document.querySelectorAll('.filter-radio input[type="radio"]');
        statusRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentFilters.status = e.target.value;
                this.applyFilters();
            });
        });
    }

    bindModalEvents() {
        // Botões para abrir modais
        document.getElementById('btn-new-book').addEventListener('click', () => {
            this.openModal('modal-new-book');
        });
        
        document.getElementById('btn-loan-return').addEventListener('click', () => {
            this.openModal('modal-loan-return');
        });

        // Botões para fechar modais
        document.querySelectorAll('.modal-close, .modal-overlay').forEach(element => {
            element.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal-close') || e.target.classList.contains('modal-overlay')) {
                    this.closeModal();
                }
            });
        });

        // Fechar modal com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Tabs nos modais
        this.bindTabEvents();
    }

    bindTabEvents() {
        const tabButtons = document.querySelectorAll('.tab-button');
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tabId = e.target.getAttribute('aria-controls');
                this.switchTab(tabId);
            });
        });
    }

    bindFormEvents() {
        // Formulário novo livro
        document.getElementById('new-book-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleNewBookSubmit();
        });

        // Formulário empréstimo
        document.getElementById('loan-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLoanSubmit();
        });

        // Formulário devolução
        document.getElementById('return-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleReturnSubmit();
        });

        // Validação em tempo real
        this.bindValidationEvents();
    }

    bindValidationEvents() {
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('blur', (e) => {
                this.validateField(e.target);
            });
            
            input.addEventListener('input', (e) => {
                this.clearFieldError(e.target);
            });
        });
    }

    bindSortEvents() {
        // Adicionar botões de ordenação ao header
        const booksHeader = document.querySelector('.books-header');
        const sortContainer = document.createElement('div');
        sortContainer.className = 'sort-controls';
        sortContainer.innerHTML = `
            <select id="sort-select" class="sort-select">
                <option value="title-asc">Título (A-Z)</option>
                <option value="title-desc">Título (Z-A)</option>
                <option value="year-asc">Ano (Antigo → Novo)</option>
                <option value="year-desc">Ano (Novo → Antigo)</option>
                <option value="author-asc">Autor (A-Z)</option>
                <option value="author-desc">Autor (Z-A)</option>
            </select>
        `;
        booksHeader.appendChild(sortContainer);

        document.getElementById('sort-select').addEventListener('change', (e) => {
            this.currentSort = e.target.value;
            this.saveSortPreference();
            this.applyFilters();
        });
    }

    bindExportEvents() {
        // Adicionar botões de export
        const actionsSection = document.querySelector('.actions-section');
        const exportContainer = document.createElement('div');
        exportContainer.className = 'export-controls';
        exportContainer.innerHTML = `
            <button class="btn btn-secondary" id="export-csv">
                📊 CSV
            </button>
            <button class="btn btn-secondary" id="export-json">
                📋 JSON
            </button>
        `;
        actionsSection.appendChild(exportContainer);

        document.getElementById('export-csv').addEventListener('click', () => {
            this.exportData('csv');
        });

        document.getElementById('export-json').addEventListener('click', () => {
            this.exportData('json');
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt + N para novo livro
            if (e.altKey && e.key === 'n') {
                e.preventDefault();
                this.openModal('modal-new-book');
            }
            
            // Alt + E para empréstimo
            if (e.altKey && e.key === 'e') {
                e.preventDefault();
                this.openModal('modal-loan-return');
            }
        });
    }

    // API Methods
    async loadBooks() {
        try {
            this.showLoading();
            const response = await fetch(`${this.apiBase}/books`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.books = await response.json();
            this.applyFilters();
            this.hideLoading();
        } catch (error) {
            console.error('Erro ao carregar livros:', error);
            this.showToast('Erro ao carregar livros. Usando dados de exemplo.', 'error');
            this.loadSampleBooks();
            this.hideLoading();
        }
    }

    async createBook(bookData) {
        try {
            const response = await fetch(`${this.apiBase}/books`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const newBook = await response.json();
            this.books.push(newBook);
            this.applyFilters();
            this.showToast('Livro adicionado com sucesso!', 'success');
            return newBook;
        } catch (error) {
            console.error('Erro ao criar livro:', error);
            this.showToast('Erro ao adicionar livro.', 'error');
            throw error;
        }
    }

    async updateBook(id, bookData) {
        try {
            const response = await fetch(`${this.apiBase}/books/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const updatedBook = await response.json();
            const index = this.books.findIndex(book => book.id === id);
            if (index !== -1) {
                this.books[index] = updatedBook;
                this.applyFilters();
            }
            this.showToast('Livro atualizado com sucesso!', 'success');
            return updatedBook;
        } catch (error) {
            console.error('Erro ao atualizar livro:', error);
            this.showToast('Erro ao atualizar livro.', 'error');
            throw error;
        }
    }

    async deleteBook(id) {
        try {
            const response = await fetch(`${this.apiBase}/books/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            this.books = this.books.filter(book => book.id !== id);
            this.applyFilters();
            this.showToast('Livro removido com sucesso!', 'success');
        } catch (error) {
            console.error('Erro ao deletar livro:', error);
            this.showToast('Erro ao remover livro.', 'error');
            throw error;
        }
    }

    // Filtering and Sorting
    applyFilters() {
        let filtered = [...this.books];

        // Filtro de busca
        if (this.currentFilters.search) {
            const searchTerm = this.currentFilters.search.toLowerCase();
            filtered = filtered.filter(book => 
                book.title.toLowerCase().includes(searchTerm) ||
                book.author.toLowerCase().includes(searchTerm) ||
                (book.isbn && book.isbn.toLowerCase().includes(searchTerm))
            );
        }

        // Filtro de gênero
        if (this.currentFilters.genres.length > 0) {
            filtered = filtered.filter(book => 
                this.currentFilters.genres.includes(book.genre)
            );
        }

        // Filtro de ano
        if (this.currentFilters.yearMin) {
            filtered = filtered.filter(book => 
                book.year >= parseInt(this.currentFilters.yearMin)
            );
        }
        
        if (this.currentFilters.yearMax) {
            filtered = filtered.filter(book => 
                book.year <= parseInt(this.currentFilters.yearMax)
            );
        }

        // Filtro de status
        if (this.currentFilters.status !== 'todos') {
            filtered = filtered.filter(book => book.status === this.currentFilters.status);
        }

        // Aplicar ordenação
        this.sortBooks(filtered);

        this.filteredBooks = filtered;
        this.currentPage = 1;
        this.renderBooks();
        this.updateBooksCount();
    }

    sortBooks(books) {
        const [field, direction] = this.currentSort.split('-');
        
        books.sort((a, b) => {
            let aValue = a[field];
            let bValue = b[field];
            
            if (typeof aValue === 'string') {
                aValue = aValue.toLowerCase();
                bValue = bValue.toLowerCase();
            }
            
            if (direction === 'asc') {
                return aValue > bValue ? 1 : -1;
            } else {
                return aValue < bValue ? 1 : -1;
            }
        });
    }

    clearAllFilters() {
        // Limpar busca
        document.getElementById('search-books').value = '';
        
        // Limpar checkboxes de gênero
        document.querySelectorAll('.filter-checkbox input').forEach(cb => cb.checked = false);
        
        // Limpar anos
        document.getElementById('year-min').value = '';
        document.getElementById('year-max').value = '';
        
        // Resetar status para "todos"
        document.querySelector('.filter-radio input[value="todos"]').checked = true;
        
        // Resetar filtros
        this.currentFilters = {
            search: '',
            genres: [],
            yearMin: '',
            yearMax: '',
            status: 'todos'
        };
        
        this.applyFilters();
        this.showToast('Filtros limpos!', 'info');
    }

    // Pagination
    renderBooks() {
        const startIndex = (this.currentPage - 1) * this.booksPerPage;
        const endIndex = startIndex + this.booksPerPage;
        const booksToShow = this.filteredBooks.slice(startIndex, endIndex);
        
        const booksContainer = document.getElementById('books-list');
        
        if (booksToShow.length === 0) {
            this.showEmptyState();
            return;
        }
        
        this.hideEmptyState();
        
        booksContainer.innerHTML = booksToShow.map(book => this.createBookCard(book)).join('');
        
        // Adicionar event listeners aos cards
        this.bindBookCardEvents();
        
        // Renderizar paginação
        this.renderPagination();
    }

    createBookCard(book) {
        const statusClass = `status-${book.status.replace(' ', '-').toLowerCase()}`;
        const statusText = this.getStatusText(book.status);
        
        return `
            <article class="book-card" role="listitem" data-book-id="${book.id}">
                <div class="book-cover">
                    <img 
                        src="${book.cover_url || 'https://via.placeholder.com/120x180?text=Livro'}" 
                        alt="Capa do livro ${book.title}"
                        class="cover-image"
                        onerror="this.src='https://via.placeholder.com/120x180?text=Livro'"
                    >
                    <div class="book-status ${statusClass}">${statusText}</div>
                </div>
                <div class="book-info">
                    <h3 class="book-title">${book.title}</h3>
                    <p class="book-author">${book.author}</p>
                    <p class="book-year">${book.year}</p>
                    <p class="book-genre">${book.genre}</p>
                    <div class="book-actions">
                        <button 
                            class="btn btn-sm btn-primary btn-details"
                            aria-label="Ver detalhes do livro ${book.title}"
                            data-book-id="${book.id}"
                        >
                            Detalhes
                        </button>
                        <button 
                            class="btn btn-sm btn-secondary btn-loan"
                            aria-label="Emprestar livro ${book.title}"
                            data-book-id="${book.id}"
                            ${book.status !== 'disponivel' ? 'disabled' : ''}
                        >
                            ${book.status === 'disponivel' ? 'Emprestar' : 'Indisponível'}
                        </button>
                    </div>
                </div>
            </article>
        `;
    }

    bindBookCardEvents() {
        // Detalhes
        document.querySelectorAll('.btn-details').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const bookId = e.target.dataset.bookId;
                this.showBookDetails(bookId);
            });
        });

        // Empréstimo
        document.querySelectorAll('.btn-loan').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const bookId = e.target.dataset.bookId;
                this.openLoanModal(bookId);
            });
        });
    }

    renderPagination() {
        const totalPages = Math.ceil(this.filteredBooks.length / this.booksPerPage);
        
        if (totalPages <= 1) return;
        
        const booksMain = document.querySelector('.books-main');
        let paginationContainer = document.querySelector('.pagination-container');
        
        if (!paginationContainer) {
            paginationContainer = document.createElement('div');
            paginationContainer.className = 'pagination-container';
            booksMain.appendChild(paginationContainer);
        }
        
        let paginationHTML = '<div class="pagination">';
        
        // Botão anterior
        paginationHTML += `
            <button class="pagination-btn" ${this.currentPage === 1 ? 'disabled' : ''} 
                    onclick="app.goToPage(${this.currentPage - 1})">
                ‹ Anterior
            </button>
        `;
        
        // Números das páginas
        for (let i = 1; i <= totalPages; i++) {
            if (i === this.currentPage) {
                paginationHTML += `<button class="pagination-btn active">${i}</button>`;
            } else if (Math.abs(i - this.currentPage) <= 2 || i === 1 || i === totalPages) {
                paginationHTML += `<button class="pagination-btn" onclick="app.goToPage(${i})">${i}</button>`;
            } else if (Math.abs(i - this.currentPage) === 3) {
                paginationHTML += '<span class="pagination-ellipsis">...</span>';
            }
        }
        
        // Botão próximo
        paginationHTML += `
            <button class="pagination-btn" ${this.currentPage === totalPages ? 'disabled' : ''} 
                    onclick="app.goToPage(${this.currentPage + 1})">
                Próximo ›
            </button>
        `;
        
        paginationHTML += '</div>';
        paginationContainer.innerHTML = paginationHTML;
    }

    goToPage(page) {
        this.currentPage = page;
        this.renderBooks();
        
        // Scroll to top
        document.querySelector('.books-main').scrollIntoView({ behavior: 'smooth' });
    }

    // Modals
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.setAttribute('aria-hidden', 'false');
        
        // Focus management
        const firstInput = modal.querySelector('input, button, select, textarea');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
        
        // Trap focus dentro do modal
        this.trapFocus(modal);
    }

    closeModal() {
        const openModal = document.querySelector('.modal[aria-hidden="false"]');
        if (openModal) {
            openModal.setAttribute('aria-hidden', 'true');
            
            // Limpar formulários
            const forms = openModal.querySelectorAll('form');
            forms.forEach(form => {
                form.reset();
                this.clearFormErrors(form);
            });
        }
    }

    trapFocus(modal) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });
    }

    switchTab(tabId) {
        // Esconder todos os painéis
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        
        // Desativar todos os botões
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        });
        
        // Ativar painel e botão selecionados
        document.getElementById(tabId).classList.add('active');
        document.querySelector(`[aria-controls="${tabId}"]`).classList.add('active');
        document.querySelector(`[aria-controls="${tabId}"]`).setAttribute('aria-selected', 'true');
    }

    // Form Handling
    async handleNewBookSubmit() {
        const form = document.getElementById('new-book-form');
        const formData = new FormData(form);
        
        const bookData = {
            title: document.getElementById('book-title-input').value.trim(),
            author: document.getElementById('book-author-input').value.trim(),
            year: parseInt(document.getElementById('book-year-input').value) || new Date().getFullYear(),
            genre: document.getElementById('book-genre-select').value,
            isbn: document.getElementById('book-isbn-input').value.trim(),
            cover_url: document.getElementById('book-cover-input').value.trim(),
            status: 'disponivel'
        };

        // Validações
        if (!this.validateBookForm(bookData)) {
            return;
        }

        // Verificar título duplicado
        if (this.isDuplicateTitle(bookData.title)) {
            this.showFieldError('book-title-input', 'Já existe um livro com este título');
            return;
        }

        try {
            await this.createBook(bookData);
            this.closeModal();
        } catch (error) {
            // Erro já tratado no createBook
        }
    }

    async handleLoanSubmit() {
        const studentName = document.getElementById('student-name').value.trim();
        const studentClass = document.getElementById('student-class').value.trim();
        const loanDate = document.getElementById('loan-date').value;
        const returnDate = document.getElementById('return-date').value;
        
        // Validações básicas
        if (!studentName) {
            this.showFieldError('student-name', 'Nome do aluno é obrigatório');
            return;
        }

        // Simular empréstimo (implementar API real)
        this.showToast('Empréstimo realizado com sucesso!', 'success');
        this.closeModal();
    }

    async handleReturnSubmit() {
        // Implementar lógica de devolução
        this.showToast('Devolução realizada com sucesso!', 'success');
        this.closeModal();
    }

    // Validation
    validateBookForm(bookData) {
        let isValid = true;

        // Título obrigatório
        if (!bookData.title) {
            this.showFieldError('book-title-input', 'Título é obrigatório');
            isValid = false;
        } else if (bookData.title.length < 2) {
            this.showFieldError('book-title-input', 'Título deve ter pelo menos 2 caracteres');
            isValid = false;
        } else if (bookData.title.length > 200) {
            this.showFieldError('book-title-input', 'Título deve ter no máximo 200 caracteres');
            isValid = false;
        }

        // Autor obrigatório
        if (!bookData.author) {
            this.showFieldError('book-author-input', 'Autor é obrigatório');
            isValid = false;
        } else if (bookData.author.length < 2) {
            this.showFieldError('book-author-input', 'Nome do autor deve ter pelo menos 2 caracteres');
            isValid = false;
        }

        // Ano válido
        const currentYear = new Date().getFullYear();
        if (bookData.year < 1800 || bookData.year > currentYear) {
            this.showFieldError('book-year-input', `Ano deve estar entre 1800 e ${currentYear}`);
            isValid = false;
        }

        return isValid;
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldId = field.id;
        
        this.clearFieldError(field);

        switch (fieldId) {
            case 'book-title-input':
                if (!value) {
                    this.showFieldError(fieldId, 'Título é obrigatório');
                    return false;
                } else if (value.length < 2) {
                    this.showFieldError(fieldId, 'Título deve ter pelo menos 2 caracteres');
                    return false;
                }
                break;
                
            case 'book-author-input':
                if (!value) {
                    this.showFieldError(fieldId, 'Autor é obrigatório');
                    return false;
                } else if (value.length < 2) {
                    this.showFieldError(fieldId, 'Nome do autor deve ter pelo menos 2 caracteres');
                    return false;
                }
                break;
                
            case 'book-year-input':
                const year = parseInt(value);
                const currentYear = new Date().getFullYear();
                if (value && (year < 1800 || year > currentYear)) {
                    this.showFieldError(fieldId, `Ano deve estar entre 1800 e ${currentYear}`);
                    return false;
                }
                break;
        }
        
        return true;
    }

    isDuplicateTitle(title) {
        return this.books.some(book => 
            book.title.toLowerCase() === title.toLowerCase()
        );
    }

    showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const formGroup = field.closest('.form-group');
        
        // Remover erro anterior
        this.clearFieldError(field);
        
        // Adicionar classe de erro
        field.classList.add('error');
        
        // Criar elemento de erro
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        
        formGroup.appendChild(errorElement);
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const formGroup = field.closest('.form-group');
        const existingError = formGroup.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }

    clearFormErrors(form) {
        form.querySelectorAll('.field-error').forEach(error => error.remove());
        form.querySelectorAll('.error').forEach(field => field.classList.remove('error'));
    }

    // Export
    exportData(format) {
        const data = this.filteredBooks;
        const filename = `biblioteca_${new Date().toISOString().split('T')[0]}`;
        
        if (format === 'csv') {
            this.exportCSV(data, filename);
        } else if (format === 'json') {
            this.exportJSON(data, filename);
        }
        
        this.showToast(`Dados exportados como ${format.toUpperCase()}!`, 'success');
    }

    exportCSV(data, filename) {
        const headers = ['Título', 'Autor', 'Ano', 'Gênero', 'Status', 'ISBN'];
        const csvContent = [
            headers.join(','),
            ...data.map(book => [
                `"${book.title}"`,
                `"${book.author}"`,
                book.year,
                `"${book.genre}"`,
                `"${book.status}"`,
                `"${book.isbn || ''}"`
            ].join(','))
        ].join('\n');
        
        this.downloadFile(csvContent, `${filename}.csv`, 'text/csv');
    }

    exportJSON(data, filename) {
        const jsonContent = JSON.stringify(data, null, 2);
        this.downloadFile(jsonContent, `${filename}.json`, 'application/json');
    }

    downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }

    // UI State Management
    showLoading() {
        document.getElementById('loading-state').setAttribute('aria-hidden', 'false');
        document.getElementById('books-list').style.display = 'none';
    }

    hideLoading() {
        document.getElementById('loading-state').setAttribute('aria-hidden', 'true');
        document.getElementById('books-list').style.display = 'grid';
    }

    showEmptyState() {
        document.getElementById('empty-state').setAttribute('aria-hidden', 'false');
        document.getElementById('books-list').style.display = 'none';
    }

    hideEmptyState() {
        document.getElementById('empty-state').setAttribute('aria-hidden', 'true');
        document.getElementById('books-list').style.display = 'grid';
    }

    updateBooksCount() {
        const totalBooks = this.filteredBooks.length;
        document.getElementById('total-books').textContent = totalBooks;
    }

    // Toast Notifications
    showToast(message, type = 'info') {
        // Criar container de toasts se não existir
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }

        // Criar toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">${this.getToastIcon(type)}</span>
                <span class="toast-message">${message}</span>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">×</button>
        `;

        toastContainer.appendChild(toast);

        // Auto remove após 5 segundos
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);

        // Animação de entrada
        setTimeout(() => toast.classList.add('toast-show'), 100);
    }

    getToastIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    // Utility Methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    getStatusText(status) {
        const statusMap = {
            'disponivel': 'Disponível',
            'emprestado': 'Emprestado',
            'manutencao': 'Manutenção'
        };
        return statusMap[status] || status;
    }

    loadSortPreference() {
        return localStorage.getItem('biblioteca-sort') || 'title-asc';
    }

    saveSortPreference() {
        localStorage.setItem('biblioteca-sort', this.currentSort);
    }

    restoreSortUI() {
        const sortSelect = document.getElementById('sort-select');
        if (sortSelect) {
            sortSelect.value = this.currentSort;
        }
    }

    // Sample Data (fallback)
    loadSampleBooks() {
        this.books = [
            {
                id: 1,
                title: "O Pequeno Príncipe",
                author: "Antoine de Saint-Exupéry",
                year: 1943,
                genre: "ficcao",
                status: "disponivel",
                isbn: "978-8520925065",
                cover_url: "https://via.placeholder.com/120x180?text=Pequeno+Príncipe"
            },
            {
                id: 2,
                title: "Dom Casmurro",
                author: "Machado de Assis",
                year: 1899,
                genre: "romance",
                status: "emprestado",
                isbn: "978-8525406569"
            },
            {
                id: 3,
                title: "1984",
                author: "George Orwell",
                year: 1949,
                genre: "ficcao",
                status: "disponivel",
                isbn: "978-8535914849"
            }
        ];
        this.applyFilters();
    }

    // Book Details Modal
    showBookDetails(bookId) {
        const book = this.books.find(b => b.id == bookId);
        if (!book) return;

        // Criar modal de detalhes dinamicamente
        const detailsModal = this.createBookDetailsModal(book);
        document.body.appendChild(detailsModal);
        
        this.openModal('modal-book-details');
    }

    createBookDetailsModal(book) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'modal-book-details';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-hidden', 'true');
        
        modal.innerHTML = `
            <div class="modal-overlay" aria-hidden="true"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">Detalhes do Livro</h2>
                    <button class="modal-close" aria-label="Fechar modal">×</button>
                </div>
                <div class="modal-body">
                    <div class="book-details">
                        <div class="book-cover-large">
                            <img src="${book.cover_url || 'https://via.placeholder.com/200x300?text=Livro'}" 
                                 alt="Capa de ${book.title}">
                        </div>
                        <div class="book-info-detailed">
                            <h3>${book.title}</h3>
                            <p><strong>Autor:</strong> ${book.author}</p>
                            <p><strong>Ano:</strong> ${book.year}</p>
                            <p><strong>Gênero:</strong> ${book.genre}</p>
                            <p><strong>Status:</strong> ${this.getStatusText(book.status)}</p>
                            ${book.isbn ? `<p><strong>ISBN:</strong> ${book.isbn}</p>` : ''}
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="this.closest('.modal').remove()">
                        Fechar
                    </button>
                    <button class="btn btn-danger" onclick="app.confirmDeleteBook(${book.id})">
                        Excluir Livro
                    </button>
                </div>
            </div>
        `;
        
        return modal;
    }

    async confirmDeleteBook(bookId) {
        if (confirm('Tem certeza que deseja excluir este livro?')) {
            await this.deleteBook(bookId);
            document.getElementById('modal-book-details').remove();
        }
    }

    openLoanModal(bookId) {
        const book = this.books.find(b => b.id == bookId);
        if (!book) return;

        // Pre-popular o modal de empréstimo com o livro selecionado
        this.openModal('modal-loan-return');
        
        // Setar data padrão para hoje
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('loan-date').value = today;
        
        // Setar data de devolução para 15 dias
        const returnDate = new Date();
        returnDate.setDate(returnDate.getDate() + 15);
        document.getElementById('return-date').value = returnDate.toISOString().split('T')[0];
    }
}

// Inicializar aplicação quando DOM estiver carregado
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new BibliotecaApp();
});

// Adicionar estilos para novos componentes
const additionalStyles = `
    .sort-controls {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
    }

    .sort-select {
        padding: var(--spacing-2) var(--spacing-3);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        font-size: var(--font-size-sm);
        background: var(--white);
    }

    .export-controls {
        display: flex;
        gap: var(--spacing-2);
    }

    .pagination-container {
        display: flex;
        justify-content: center;
        margin-top: var(--spacing-8);
    }

    .pagination {
        display: flex;
        gap: var(--spacing-2);
        align-items: center;
    }

    .pagination-btn {
        padding: var(--spacing-2) var(--spacing-3);
        border: 1px solid var(--border);
        background: var(--white);
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: var(--transition);
    }

    .pagination-btn:hover:not(:disabled) {
        background: var(--primary);
        color: var(--white);
    }

    .pagination-btn.active {
        background: var(--primary);
        color: var(--white);
        border-color: var(--primary);
    }

    .pagination-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .pagination-ellipsis {
        padding: var(--spacing-2);
        color: var(--text-muted);
    }

    .toast-container {
        position: fixed;
        top: var(--spacing-6);
        right: var(--spacing-6);
        z-index: 3000;
        display: flex;
        flex-direction: column;
        gap: var(--spacing-2);
    }

    .toast {
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-width: 300px;
        padding: var(--spacing-3) var(--spacing-4);
        background: var(--white);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        border-left: 4px solid var(--primary);
        transform: translateX(100%);
        transition: transform 0.3s ease-in-out;
    }

    .toast.toast-show {
        transform: translateX(0);
    }

    .toast-success {
        border-left-color: var(--success);
    }

    .toast-error {
        border-left-color: var(--danger);
    }

    .toast-warning {
        border-left-color: var(--warning);
    }

    .toast-content {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
    }

    .toast-close {
        background: none;
        border: none;
        font-size: var(--font-size-lg);
        cursor: pointer;
        color: var(--text-muted);
        padding: 0;
        line-height: 1;
    }

    .field-error {
        color: var(--danger);
        font-size: var(--font-size-xs);
        margin-top: var(--spacing-1);
    }

    .form-input.error,
    .form-select.error {
        border-color: var(--danger);
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }

    .book-details {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: var(--spacing-6);
    }

    .book-cover-large img {
        width: 100%;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
    }

    .book-info-detailed h3 {
        font-size: var(--font-size-xl);
        margin-bottom: var(--spacing-4);
        color: var(--primary);
    }

    .book-info-detailed p {
        margin-bottom: var(--spacing-2);
        line-height: 1.6;
    }

    @media (max-width: 768px) {
        .book-details {
            grid-template-columns: 1fr;
            text-align: center;
        }
        
        .book-cover-large {
            justify-self: center;
        }
        
        .toast {
            min-width: 280px;
            margin: 0 var(--spacing-4);
        }
        
        .export-controls {
            flex-direction: column;
        }
    }
`;

// Adicionar estilos ao head
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);
