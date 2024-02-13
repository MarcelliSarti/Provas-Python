function selectAllPermissions() {
    checkboxSelectAll = document.getElementById('selectAll');
    if (checkboxSelectAll.checked) {
        document.querySelectorAll('.checkbox').forEach(function(checkbox) {
            var checkboxInput = checkbox.querySelector('input[type="checkbox"]');
            checkboxInput.checked = true;
        });
    } else {
        document.querySelectorAll('.checkbox').forEach(function(checkbox) {
            var checkboxInput = checkbox.querySelector('input[type="checkbox"]');
            checkboxInput.checked = false;
        });   
    }
}