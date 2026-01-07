/**
 * NBA Hub - Custom JavaScript
 */

// Alpine.js component for search box
function searchBox() {
    return {
        query: '',
        results: [],
        showResults: false,
        loading: false,

        async search() {
            if (this.query.length < 2) {
                this.results = [];
                return;
            }

            this.loading = true;

            try {
                const response = await fetch(`/api/search/players?q=${encodeURIComponent(this.query)}`);
                if (response.ok) {
                    const data = await response.json();
                    this.results = data;
                } else {
                    console.error('Search failed:', response.statusText);
                    this.results = [];
                }
            } catch (error) {
                console.error('Search error:', error);
                this.results = [];
            } finally {
                this.loading = false;
            }
        }
    };
}

// Utility function to format numbers
function formatNumber(num, decimals = 1) {
    if (num === null || num === undefined) return '-';
    return Number(num).toFixed(decimals);
}

// Utility function to format percentages
function formatPercentage(num) {
    if (num === null || num === undefined || num === 0) return '-';
    return `${Number(num).toFixed(1)}%`;
}

// Sort table columns
function sortTable(tableId, columnIndex, isNumeric = false) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        if (isNumeric) {
            return parseFloat(bValue) - parseFloat(aValue);
        } else {
            return aValue.localeCompare(bValue);
        }
    });

    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// Debounce function for search input
function debounce(func, wait) {
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

// Initialize tooltips (if using a tooltip library)
document.addEventListener('DOMContentLoaded', function() {
    console.log('NBA Hub loaded successfully');

    // Add any initialization code here
    // For example, initializing charts, tooltips, etc.
});

// Export functions for use in Alpine.js
window.searchBox = searchBox;
window.formatNumber = formatNumber;
window.formatPercentage = formatPercentage;
window.sortTable = sortTable;
