function mostrarImagemSelecionada(input, imgId) {
    var preview = document.getElementById(imgId);
    preview.style.display = 'block';
    var file = input.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        preview.src = e.target.result;
    };

    if (file) {
        reader.readAsDataURL(file);
    }
    var button = document.getElementById('remove'+imgId);
    button.style.display = 'block';
}

function removerImagem(imgId) {
    var input = document.querySelector('input[name='+imgId+']');
    var image = document.getElementById(imgId);
    var button = document.getElementById('remove'+imgId);

    input.value = ''; // Limpar o valor do campo de arquivo
    image.src = '#';
    image.style.display = 'none';
    button.style.display = 'none';
}