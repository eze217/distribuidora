// url notificaciones_count

window.onload= function(){

    notificaciones()

    setInterval(notificaciones,300000)
    
}



// Actualiza el numero de notificaciones SIN LEER en el nav

async function notificaciones (){
    url='/notificaciones/count/'
    
    const response = await fetch(url)

    const data= await response.json()

    let cant_notificaciones = document.getElementById('cant_notificaciones')

    if (response.status == 200){
        
        cant_notificaciones.innerHTML=data.data
        
    }


}

