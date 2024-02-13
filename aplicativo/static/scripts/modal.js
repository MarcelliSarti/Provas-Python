function exibirSnackbar(type, message) {
    var snackbar = document.getElementById('snackbar');

    var snackBarMessage = document.getElementById('snackbar-message');
    snackBarMessage.innerText = message;

    snackbar.className = 'show';

    if (type == 'success')
        snackbar.style.backgroundColor = '#4CAF50';
    else if (type == 'error')
        snackbar.style.backgroundColor = '#FF0000';

    setTimeout(function () {
        snackbar.className = snackbar.className.replace('show', '');
    }, 3000);  // Remover a snackbar após 3 segundos
}

function openAddModal(fields, model, type) {
    var modal = document.getElementById('addModal');
    var modalTitle = document.getElementById('addModal-title');

    ['field1', 'field2', 'field3'].forEach(function(field){
        if ((fields[field] != '') && (type == 'edit')) 
            document.getElementById(field).value = fields[field];
        else
            document.getElementById(field).value = ''
    });

    if (type == 'edit')
        modalTitle.innerText = 'Editar ' + model;
    else
        modalTitle.innerText = 'Inserir ' + model;

    if (type == 'specialties'){
        getSerie();
    }

    if (model == 'Usuário'){
        if (type == 'edit'){
            var option = document.getElementById(fields['field1']);  
            option.select = true;   

            var username = document.getElementById('field2');  
            username.readOnly = true;
        }
    }
    if (model == 'Carga Horária'){
        ['field4', 'field5', 'field6'].forEach(function(field){
            if ((fields[field] != '') && (type == 'edit')) 
                document.getElementById(field).value = fields[field];
            else
                document.getElementById(field).value = ''
        });
    }
    modal.style.display = 'block';
};

function openDeleteModal(id, type, url) {
    var modal = document.getElementById('deleteModal');
    modal.style.display = 'block';

    var modalTitle = document.getElementById('deleteModal-title');
    modalTitle.innerText = 'Deletar ' + type;

    var link = document.getElementById('deleteLink');
    link.setAttribute('href', '/provas/' + url + '/' + id.replace('/', '%252F') + '/delete/');
}

function openPasswordModal(id) {
    var modal = document.getElementById('passwordModal');
    modal.style.display = 'block';

    var link = document.getElementById('passswordLink');
    link.setAttribute('href', '/provas/users/' + id.replace('/', '%252F') + '/changePassword/');
}

function closeModal(type) {
    var modal = document.getElementById(type + 'Modal');
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    window.onclick = function (event) {
        if (event.target == document.getElementById('addModal')) {
            document.getElementById('addModal').style.display = 'none';
        } else if (event.target == document.getElementById('deleteModal')) {
            document.getElementById('deleteModal').style.display = 'none';
        }
    }
});

function nextPage(currentPage, nextPage){
    document.getElementById(currentPage).classList.remove('active');
    document.getElementById(nextPage).classList.add('active');
}