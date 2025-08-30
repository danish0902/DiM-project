document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('journal-form');
    const entryInput = document.getElementById('journal-entry');
    const entriesContainer = document.getElementById('journal-entries');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const entryText = entryInput.value.trim();
        if (entryText !== '') {
            addEntry(entryText);
            entryInput.value = '';
        }
    });

    function addEntry(text) {
        const entryDiv = document.createElement('div');
        entryDiv.classList.add('entry');
        entryDiv.textContent = text;
        entriesContainer.prepend(entryDiv);
    }
});
