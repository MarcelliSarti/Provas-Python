function getFieldsValues(type) {
    const csrftoken = document.cookie.match(/csrftoken=([^;]*)/)[1];

    var input_field1 = document.getElementById('field1');
    var input_field2 = document.getElementById('field2');
    var input_field3 = document.getElementById('field3');
    var input_field4 = document.getElementById('field4');
    
    if (type == 'courseId'){
        $.ajax({
            type: 'POST',
            url: '/provas/exams/courses/' + input_field1.value + '/specialties/',  // Substitua pela URL correta
            data: {csrfmiddlewaretoken: csrftoken},
            dataType: 'json',
            success: function(response) {
                input_field2.innerHTML = '';
                var option = document.createElement('option');
                option.text  = '';
                input_field2.add(option);
                response.specialities.forEach(function(spec){
                    var option = document.createElement('option');
                    option.value = spec['id'];
                    option.text  = spec['caption'];
                    input_field2.add(option);
                });
                var input_inputfield2 = document.getElementById('field-field2');
                input_inputfield2.classList.remove('hidden');

                input_field3.innerHTML = '';
                var option = document.createElement('option');
                option.text  = '';
                input_field3.add(option);
                for (let i=1; i<=response.numberOfSeries; i++){
                    var option = document.createElement('option');
                    option.value = i;
                    option.text  = 'Série ' + String(i);
                    input_field3.add(option);
                }
                var input_inputfield3 = document.getElementById('field-field3');
                input_inputfield3.classList.remove('hidden');
            },
            error: function(error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    } else if (type == 'specialityId'){
        $.ajax({
            type: 'POST',
            url: '/provas/exams/courses/' + input_field1.value + '/specialties/' + input_field2.value + '/series/' + input_field3.value + '/subjects/',
            data: {csrfmiddlewaretoken: csrftoken},
            dataType: 'json',
            success: function(response) {
                input_field4.innerHTML = '';
                var option = document.createElement('option');
                option.text  = '';
                input_field4.add(option);
                response.subjects.forEach(function(subject){
                    var option = document.createElement('option');
                    option.value = subject['id'];
                    option.text  = subject['caption'];
                    input_field4.add(option);
                });
                var input_inputfield4 = document.getElementById('field-field4');
                input_inputfield4.classList.remove('hidden');
            },
            error: function(error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    } else if (type == 'subjectId'){
        var input_inputfield5 = document.getElementById('field-field5');
        input_inputfield5.classList.remove('hidden');
        var input_inputfield6 = document.getElementById('field-field6');
        input_inputfield6.classList.remove('hidden');
        var input_inputfield7 = document.getElementById('field-field7');
        input_inputfield7.classList.remove('hidden');
        var input_inputfield7 = document.getElementById('field-field8');
        input_inputfield7.classList.remove('hidden');
    }
}

function openAddModal(fields, model, type) {
    var modal = document.getElementById('addModal');
    var modalTitle = document.getElementById('addModal-title');

    modal.style.display = 'block';

    if (type == 'edit')
        modalTitle.innerText = 'Editar ' + model;
    else
        modalTitle.innerText = 'Inserir ' + model;

    if (model == 'Provas'){
        ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7'].forEach(async function(field){
            document.getElementById(field).value = '';
        });
        ['field-field2', 'field-field3', 'field-field4', 'field-field5', 'field-field6', 'field-field7'].forEach(function(field){
            document.getElementById(field).classList.add('hidden');
        });
    }
}