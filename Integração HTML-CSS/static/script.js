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

function mostrarTexto(id){

  // aqui tá armazenando o id referenciado no parâmetro e guardando na variável mostrar
  var mostrar = document.getElementById(id);

  // aqui ele "injeta" a classe "mostrando" no elemento armazenado na variável
  mostrar.classList.toggle("mostrando");
  // esse ".classList.toggle(parametro)" recebe como parametro a classe que será injetada no elemento. É tipo um if else. se o elemento já tiver a classe injetada, esse método remove ela do elemmento. Se não tiver a classe, ela será injetada.
}

function mostrarHorariosDisponiveis() {
  var horarios = [];
  var horaInicial = 8;
  var horaFinal = 18;
  var intervalo = 1;
  for (var i = horaInicial; i <= horaFinal; i += intervalo) {
    for (var j = 0; j < 60; j += 60) {
      var hora = ("0" + i).slice(-2);
      var minuto = ("0" + j).slice(-2);
      var horario = hora + ":" + minuto;
      horarios.push(horario);
    }
  }
  var horaInput = document.getElementById("hora");
  horaInput.innerHTML = "";
  for (var i = 0; i < horarios.length; i++) {
    var horario = horarios[i];
    horaInput.innerHTML += "<option value='" + horario + "'>" + horario + "</option>";
  }
}

var horaInput = document.getElementById("hora");
horaInput.addEventListener("change", function() {
  var valorSelecionado = horaInput.value;
  var elementoDesejado = document.getElementById("hora");
  elementoDesejado.value = valorSelecionado;
});

mostrarHorariosDisponiveis();


function mostrarDatasDisponiveis() {
var dataInput = document.getElementById("data");
var hoje = new Date();
var ano = hoje.getFullYear();
var mes = ("0" + (hoje.getMonth() + 1)).slice(-2);
var dia = ("0" + hoje.getDate()).slice(-2);
var dataAtual = ano + "-" + mes + "-" + dia;
dataInput.setAttribute("min", dataAtual);
}

var dataInput = document.getElementById("data");
dataInput.addEventListener("click", mostrarDatasDisponiveis);

function mostrar_senha(){
  var senha = document.getElementById("senha");
  var senhaConfirm = document.getElementById("senha-confirmar");
  if (senha.type && senhaConfirm.type == "password"){
    senha.type = "text";
    senhaConfirm.type = "text";
  }else{
  senha.type = "password";  
  senhaConfirm.type = "password";

  }
}

function mostrar_senhaLogin(){
  var senhaLogin = document.getElementById("senhaLogin")
  if (senhaLogin.type == "password"){
    senhaLogin.type = "text";
  }else{
  senhaLogin.type = "password";

  }
}