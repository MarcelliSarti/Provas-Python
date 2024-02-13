var paginas = [];
var options_list = [];

function toggleDetails(rowId) {
    // Obter todas as linhas ocultas associadas à especialidade e matéria
    var detailsRows = document.querySelectorAll('.hidden-row[data-spec-id="' + rowId + '"]');

    // Alternar a exibição de cada linha
    detailsRows.forEach(function (row) {
        row.style.display = (row.style.display === 'none' || row.style.display === '') ? 'table-row' : 'none';
    });
}

function nextPage(currentPage, nextPage) {
    var input_field1 = document.getElementById('field1');
    var input_field2 = document.getElementById('field2');
    var input_field3 = document.getElementById('field3');
    if ((input_field1.value === '') | (input_field2.value === '') | (input_field3.value === '')) {
        exibirSnackbar('error', 'Preencha os campos antes de prosseguir!');
        return;
    } else if (currentPage == 'page1') {
        if (!(paginas == [])) {
            paginas.forEach(function(pagina) {
                document.getElementById(pagina).remove();
            });
        }
        const csrftoken = document.cookie.match(/csrftoken=([^;]*)/)[1];
        var especId     = input_field1.value;
        var cursoId     = input_field2.value;
        $.ajax({
            type: 'POST',
            url: '/provas/series/',  // Substitua pela URL correta
            data: {'curso_id': cursoId, 'espec_id': especId, csrfmiddlewaretoken: csrftoken},
            dataType: 'json',
            success: function(response) {
                getSerie(response.series, response.subjects, response.selectSubjects);
            },
            error: function(error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    }
    document.getElementById(currentPage).classList.remove('active');
    if (document.getElementById(nextPage))
        document.getElementById(nextPage).classList.add('active');
}

function getSerie(series, subjects, selected) {
    var specialityForm = document.getElementById("speciality-form");
    for(let i=1; i<=series;i++){
        var formPage = document.createElement('div');
        formPage.id = "page"+String(1+i);
        paginas.push("page"+String(1+i));
        formPage.classList.add("form-page");
        if (i==1)
            formPage.classList.add("active");

        var title = document.createElement('p');
        title.textContent = 'Escolha as matérias da série ' + String(i);

        var multiselect = document.createElement('div');
        multiselect.classList.add("multiselect");

        var selectedItems = document.createElement('div');
        selectedItems.classList.add("selected-items");
        selectedItems.id = "selected-items-page" + String(i+1);
        
        var titleSelected = document.createElement('p');
        titleSelected.textContent = 'Selecionados: ';

        selectedItems.appendChild(titleSelected);
        if (Object.keys(selected).length !== 0) {
            selected[i].forEach(function(select_item) {
                var item = document.createElement('span');
                item.classList.add('item');
                item.id = select_item['subjectId'];
                item.textContent = select_item['subjectId'];
                item.onclick = function() {
                    removeSelectedItem(select_item['subjectId']);
                };
                selectedItems.appendChild(item);
            });
        }

        var searchBox = document.createElement('div');
        searchBox.classList.add("search-box");

        var inputPesquisar = document.createElement('input')
        inputPesquisar.type = 'text'
        inputPesquisar.placeholder = 'Pesquisar';
        inputPesquisar.addEventListener('click', function() {
            toggleOptions('page'+ String(1+i));
        });
        inputPesquisar.addEventListener('input', function() {
            filterOptions(this.value, 'page'+String(i+1));
        });

        var options = document.createElement('div')
        options.classList.add('options')
        options.id = 'options-page' + String(1+i);
        options.addEventListener('click', function() {
            handleOptionClick(event, 'page'+String(i+1));
        });

        var buttons = document.createElement('div');
        buttons.classList.add("buttons");

        var buttonAnt = document.createElement('button');
        buttonAnt.type = "button";
        buttonAnt.classList.add("button");
        buttonAnt.classList.add("resize");
        buttonAnt.classList.add("cancel");
        buttonAnt.textContent = 'Anterior';
        buttonAnt.addEventListener('click', function() {
            nextPage("page"+String(i+1), "page"+String(i));
        });

        var buttonPos = document.createElement('button');
        if (i != series){
            buttonPos.textContent = 'Próximo';

            buttonPos.addEventListener('click', function() {
                nextPage("page"+String(i+1), "page"+String(i+2));
            });
        } else {
            buttonPos.type = "submit";
            buttonPos.textContent = 'Salvar';

            buttonPos.addEventListener('click', function() {
                saveSpeciality();
            });
        }

        buttonPos.type = "button";
        buttonPos.classList.add("button");
        buttonPos.classList.add("resize");

        buttons.appendChild(buttonAnt);
        buttons.appendChild(buttonPos);
        searchBox.append(inputPesquisar);
        multiselect.appendChild(selectedItems);
        multiselect.appendChild(searchBox);
        multiselect.appendChild(options);
        formPage.appendChild(title);    
        formPage.appendChild(multiselect);    
        formPage.appendChild(buttons);
        specialityForm.appendChild(formPage);
    }
    options_list = subjects;
}

function toggleOptions(pageId) {
    filterOptions('', pageId);
    var optionsList = document.querySelector('#options-'+pageId);
    optionsList.classList.toggle('show-options');
}

function filterOptions(searchTerm, pageId) {
    var optionsList = document.querySelector('#options-'+pageId);
    optionsList.innerHTML = '';

    options_list.forEach(function(option) {
        if (option['caption'].toLowerCase().includes(searchTerm.toLowerCase())) {
            var optionElement = document.createElement('div');
            optionElement.classList.add('option');
            optionElement.id = option['id']
            optionElement.textContent = option['caption'];
            optionsList.appendChild(optionElement);
        }
    });
}

function handleOptionClick(event, pageId) {
    if (event.target.classList.contains('option')) {
        var selectedItems = document.querySelector('#selected-items-'+pageId);
        if (!(selectedItems.querySelector('#' + event.target.id))){
            var selectedItem = document.createElement('span');
            selectedItem.textContent = event.target.id;
            selectedItem.classList.add('item');
            selectedItem.id = event.target.id;
            selectedItem.onclick = function() {
                removeSelectedItem(event.target.id);
            };
            selectedItems.appendChild(selectedItem);
            // Adiciona um eventListener a cada elemento novo
            selectedItem.addEventListener('click', function() {
                removeSelectedItem(item.id);
            });
        }
        toggleOptions('page'+ String(1+i));
    }
}

function removeSelectedItem(item) {
    var itemRemove = document.getElementById(item);
    if (itemRemove != null){
        itemRemove.remove();
    }
}

function saveSpeciality(){
    const csrftoken = document.cookie.match(/csrftoken=([^;]*)/)[1];

    var input_field1 = document.getElementById('field1');
    var input_field2 = document.getElementById('field2');
    var input_field3 = document.getElementById('field3');
    var especId     = input_field1.value;
    var cursoId     = input_field2.value;
    var descricao   = input_field3.value;

    var selectedItems = document.querySelectorAll('.selected-items');
    var idsByPage = [];
    selectedItems.forEach(function(selectedItem, pageIndex) {
        var spanElements = selectedItem.querySelectorAll('span');
        var idsOnPage = [];
        spanElements.forEach(function(spanElement) {
            idsOnPage.push(spanElement.id);
        });
        idsByPage.push({[pageIndex + 1]: idsOnPage});
    });

    $.ajax({
        type: 'POST',
        url: '/provas/specialties/save/',  
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: JSON.stringify({
            'curso_id': cursoId,
            'espec_id': especId,
            'descricao': descricao,
            'subjectsBySeries': idsByPage
        }),
        dataType: 'json',
        success: function() {
            location.reload()
        },
        error: function(error) {
            exibirSnackbar('error', 'Erro ao salvar especialidade: ' + error);
            console.error('Erro na solicitação AJAX:', error);
        }
    });
}

function closeModal(type) {
    var modal = document.getElementById(type + 'Modal');
    modal.style.display = 'none';

    if (!(paginas == [])) {
        paginas.forEach(function(pagina) {
            document.getElementById(pagina).remove();
        });
    }
}
