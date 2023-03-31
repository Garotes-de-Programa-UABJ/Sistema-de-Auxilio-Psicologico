function mostrarMais() {
  var mostrar = document.getElementById("info-card");
  mostrar.classList.toggle("fechado");
}

function sorry() {
  Swal.fire({
    title: 'Desculpe!',
    text: 'Função indisponível no momento',
    icon: 'warning',
    confirmButtonText: 'Fechar'
  })
}

function menuDrop() {
  var drop = document.getElementById("navbar2");
  drop.classList.toggle("menu-drop");
}