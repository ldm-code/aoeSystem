const select=document.getElementById('meuSelect')
const campo=document.getElementById('descricao')
function atualizar_campo(){
          if(select.value==="multa"){
                    campo.style.display="inline";
          }
          else{
                    campo.style.display="none";
          }
}
select.addEventListener("change", atualizar_campo);
window.addEventListener("DOMContentLoaded", atualizar_campo);