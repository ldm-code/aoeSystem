document.addEventListener("DOMContentLoaded", function () {

    const select = document.getElementById('meuSelect');
    const campo = document.getElementById('descricao');
    const repasse = document.getElementById('repasse');
    const meu = document.getElementById('meu');
    const rep = document.getElementById('rep');

    function atualizar_campo() {
        if (!select) return;

        if (select.value === "multa") {
            campo.style.display = "inline";
            meu.style.display = "inline";
            repasse.style.display = "none";
            rep.style.display = "none";
        } 
        else if (select.value === "mensalidade") {
            campo.style.display = "none";
            meu.style.display = "none";
            repasse.style.display = "inline";
            rep.style.display = "inline";
        } 
        else {
            campo.style.display = "none";
            meu.style.display = "none";
        }
    }

    // evento seguro
    if (select) {
        select.addEventListener("change", atualizar_campo);
    }

    atualizar_campo();

    // ALERTA DO BACKEND
    if (typeof mensagem !== "undefined" && mensagem.trim() !== "") {
        alert(mensagem);
    }
});