document.addEventListener('DOMContentLoaded', function() {
    const maintenanceSelect = document.querySelector('select[name="maintenance_type"]');
    const otherField = document.getElementById('other-description-field');

    function toggleOtherField() {
        if (maintenanceSelect.value === 'Others') {
            otherField.style.display = 'block';
        } else {
            otherField.style.display = 'none';
            otherField.querySelector('textarea').value = ''; // clear text if hidden
        }
    }

    maintenanceSelect.addEventListener('change', toggleOtherField);
    toggleOtherField(); // initial check
});
