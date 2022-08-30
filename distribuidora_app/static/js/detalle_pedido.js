window.onload = (event) =>{

    suma_total()
   
};




function suma_total(){
    let tabla = document.getElementById('productos_pedidos')
   
    let costo_total=0
    for (var i=1, row; row = tabla.rows[i]; i++){
        // leo datos de la fila
        
       for ( var j=0,col; col= row.cells[j]; j++){
    
            if(j == 3){
                
                costo_total += parseFloat(col.innerHTML)
              
            }
       

       }
    }

    var total_general_info = document.getElementById('total_general')
    total_general_info.innerHTML = costo_total+ ' €'
}

function edito_pedido(event){
    let datos_pedido=document.getElementById('datos_pedidos')
    let form_datos=document.getElementById ('datos_pedidos_form')
    let lapiz_edicion= document.getElementById('lapiz_edicion')
    datos_pedido.classList.toggle('oculto')
    form_datos.classList.toggle('oculto')
    lapiz_edicion.classList.toggle('oculto')
    

}