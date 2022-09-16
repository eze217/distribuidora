

function getCookie(name) { 
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');         
        for (var i = 0; i < cookies.length; i++) { 
            var cookie = cookies[i].trim();
  
            if (cookie.substring(0, name.length + 1) == (name + '=')) { 
            //console.log(cookie)
           // console.log(cookie.substring(name.length + 1))
              //cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break; 
              cookieValue=cookie.substring(name.length + 1)
              
         }
         } 
          return cookieValue;
        }
    }


// busco la cotizacion del dia




function capitalize(word) {
    const lower = word.toLowerCase();
    return lower.charAt(0).toUpperCase() + lower.slice(1);
  }






let producto_a_comprar=[]

function producto_proveedor(){
   
    let proveedor_seleccionado= document.getElementById('proveedor').value

    let url=('/pedidos_proveedor/'+proveedor_seleccionado).trim()


    fetch(url)
    //Exito
    .then(response => response.json())  // convertir a json
    .then(json=>{
        
        var div = document.getElementById('productos_pedido')
        
        var div_contenido= document.getElementById('contenido')
        // reseteo el total al cambiar de proveedor y saco el boton de confirmar
        var total_general_info = document.getElementById('total_general')
        total_general_info.innerHTML = '0 €'
        var boton_confirmar = document.getElementById('boton_confirmar_pedido')
        boton_confirmar.classList.add("oculto")    

        producto_a_comprar=[]

        if(div_contenido.hasChildNodes()){
            div_contenido.remove()
            div_contenido = document.createElement("tbody");
            div_contenido.setAttribute('id',"contenido")
            div.appendChild(div_contenido);
          
        }
       

        
       

        for(var i= 0; i < json.data.length;i++){
            //comunes_array.push(json[i])
            
            var fila = document.createElement('tr');

            var columna = document.createElement("td");
            var columna2 = document.createElement("td");
            var columna3 = document.createElement("td");
            var columna4 = document.createElement("td");
            var columna5 = document.createElement("td");
            var columna6 = document.createElement("td");
            

            columna. innerHTML = capitalize(json.data[i].name);
            columna2. innerHTML = json.data[i].precio;
            columna3. innerHTML = json.data[i].descripcion;

            var input = document.createElement("input");
            input.setAttribute('type',"number")
            input.setAttribute('onChange','cuenta()')
            var input2 = document.createElement("input");
            input2.setAttribute('type',"text")
            input2.setAttribute('value',json.data[i].id)
            input2.setAttribute('class','oculto')
            
            columna4.appendChild(input)

            columna6.appendChild(input2)
            
            

            fila.appendChild(columna)
            fila.appendChild(columna2)
            fila.appendChild(columna3)
            fila.appendChild(columna4)
            fila.appendChild(columna6)
            fila.appendChild(columna5)
            div_contenido.appendChild(fila);
                    
        }


    })    //imprimir los datos en la consola
    .catch(err => console.log('Solicitud fallida', err)); // Capturar errores
    

  
}


function cuenta(){
    producto_a_comprar=[]
    //traigo tabla de ofertas

    var tabla_proveedores=document.getElementById('productos_pedido');
    
    
    //RECORRO TABLA
    
    var total_general= 0

    for (var i=1, row; row = tabla_proveedores.rows[i]; i++){
         // leo datos de la fila
        for ( var j=0,col; col= row.cells[j]; j++){


           
            
                
            if(j== 1){
                precio=col.innerHTML

                
                
                
            }
            
            if(j== 3){
                cantidad_solicitada = col.childNodes[0].value


                
              
            }
            if(j== 4){
                id_producto=col.childNodes[0].value

                
              
            }


            if(j== 5){
                total = col.childNodes[0]
                if(cantidad_solicitada > 0 ){
                    costo_total=cantidad_solicitada* parseFloat (precio)
                    col.innerHTML=  costo_total+ ' €'
                    total_general += costo_total;
                    producto_a_comprar.push({id: id_producto, cantidad:cantidad_solicitada ,costo: precio },)
                    
                }else{
                    col.innerHTML=  ''
                    
                    
                    
                }
                
                
            }



            
            
        }


        
    }
    var total_general_info = document.getElementById('total_general')
    total_general_info.innerHTML = total_general+ ' €'
    var boton_confirmar = document.getElementById('boton_confirmar_pedido')
    if(total_general>0){
        boton_confirmar.classList.remove("oculto")    
    }else{
        boton_confirmar.classList.add('oculto')
    }
    
  
}







function confirmo_pedido(){   

    let url;

    try {
        let proveedor_seleccionado= document.getElementById('proveedor').value
        
        url =('/pedidos_proveedor/'+proveedor_seleccionado).trim()
        
    } catch (error) {
        
         url ='/pedidos_proveedor/'
    }

    let almacen = document.getElementById('entrega').value
    
    list_proveedores=  fetch(url, {
        method: 'POST',
        credentials: "same-origin",
        headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Accept": "application/json",
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'Metar': producto_a_comprar, 'almacen': almacen }),


    }).then(res => res.json())
    .then(json=>{

        let container_principal = document.getElementById('container_principal')
        container_principal.remove()
        
        let container_detalle = document.getElementById('detalle_pedido')
        // si la API devuelve error True

        if (json.error){
            let h1= document.createElement('h1')
            //h1.innerHTML=' Error al generar el pedido, intentelo de nuevo mas tarde'
            h1.innerHTML=json.mensaje
            container_detalle.appendChild(h1)

        } else{


            let h1= document.createElement('h1')
            h1.innerHTML=' Pedido generado con exito '
            container_detalle.appendChild(h1)

            let contenedor_detalle_datos = document.createElement('div')
            contenedor_detalle_datos.classList.add('tabla_proveedores') // Contenedor datos pedido

            // titulo-proveedor
            let h4_datos_proveedor= document.createElement('h4')
            h4_datos_proveedor.innerHTML= 'Pedido realizado al proveedor: '+json.data.pedido[0].proveedor
            contenedor_detalle_datos.appendChild(h4_datos_proveedor)


            //Entrega
            let h4_datos_entrega= document.createElement('h4')
            h4_datos_entrega.innerHTML= 'Datos de entrega: '+json.data.pedido[0].datos_entrega
            contenedor_detalle_datos.appendChild(h4_datos_entrega)



            //estado
            let h5_estado_pedido = document.createElement('h5')
            h5_estado_pedido.innerHTML= 'Estado: '+ json.data.pedido[0].estado
            contenedor_detalle_datos.appendChild(h5_estado_pedido)

            // Nro Pedido
            let h5_numero_pedido = document.createElement('h5')
            h5_numero_pedido.innerHTML= 'Nro Pedido: '+ json.data.pedido[0].id
            contenedor_detalle_datos.appendChild(h5_numero_pedido)

            //linea detalle
            let h5_detalle_pedido = document.createElement('h5')
            h5_detalle_pedido.innerHTML= 'Detalle:'
            contenedor_detalle_datos.appendChild(h5_detalle_pedido)

            let hr = document.createElement('hr')
            contenedor_detalle_datos.appendChild(hr)


            // Titulo de tabla

            let tabla = document.createElement('table')
            tabla.classList.add('table','table-striped')
            
            let thead = document.createElement('thead')
            
            let fila_titulos = document.createElement('tr')

            let th_nombre  = document.createElement('th')
            let th_cantidad  = document.createElement('th')
            let th_unitario  = document.createElement('th')
            let th_costo  = document.createElement('th')
            

            th_nombre.innerHTML = 'Producto'
            th_cantidad.innerHTML = 'Cantidad'
            th_unitario.innerHTML='Costo Unitario'
            th_costo.innerHTML = 'Costo Total'

            fila_titulos.appendChild(th_nombre)
            fila_titulos.appendChild(th_cantidad)
            fila_titulos.appendChild(th_unitario)
            fila_titulos.appendChild(th_costo)


            let tbody = document.createElement('tbody')



            thead.appendChild(fila_titulos)
            tabla.appendChild(thead)
            tabla.appendChild(tbody)
            contenedor_detalle_datos.appendChild(tabla)



            let costo_peido_total= 0
            // Table detalle productos
            for(var i = 0; i< json.data.detalle_pedido.length ; i++){

                let fila = document.createElement('tr')//fila contenedora
                // celdas
                let p = document.createElement('td')
                p.innerHTML = json.data.detalle_pedido[i].producto
                fila.appendChild(p)
                let pe = document.createElement('td')
                pe.innerHTML = json.data.detalle_pedido[i].cantidad
                fila.appendChild(pe)
                let p_unitario = document.createElement('td')
                p_unitario.innerHTML =json.data.detalle_pedido[i].precio_unitario
                fila.appendChild(p_unitario)
                let p_costo = document.createElement('td')
                p_costo.innerHTML = json.data.detalle_pedido[i].costo
                fila.appendChild(p_costo)


                tbody.appendChild(fila)

                costo_peido_total+= json.data.detalle_pedido[i].costo

            }

            let tfoot = document.createElement('tfoot')
            let fila_foot = document.createElement('tr')
            let td_foot= document.createElement('td')


            td_foot.innerHTML = 'TOTAL PEDIDO : '+ costo_peido_total

            fila_foot.appendChild(td_foot)

            tfoot.appendChild(fila_foot)
            tabla.appendChild(tfoot)
                
        
            container_detalle.appendChild(contenedor_detalle_datos)
          

        }// fin else
        let boton_volver = document.getElementById('botonlistapedidos')
            
        boton_volver.classList.remove('oculto')


        


        


    
    
    })
    .catch(err => console.log('Solicitud fallida', err)); // Capturar errores;
    
  
} 
