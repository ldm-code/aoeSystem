const senha=document.getElementById('senha');
const olho=document.getElementById('olho')

olho.addEventListener("click",(e)=>{
          
          
          if (senha.type==="password"){
                              senha.type="text";

                    }
          else{
                              senha.type="password";
                    }
          
});