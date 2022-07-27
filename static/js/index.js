function mostrarComentarios(id) {
    comentario = document.getElementById(`comentarios_${id}`)
    comentario.style.visibility = "visible"
    comentario.style.display = "block"
}

function responder(id) {
    responder = document.getElementById(`comentario_${id}`)
    responder.style.display = "block"
}


function AddLike(likesCount) {
    countLikes = document.getElementById(`likes_${likesCount}`)
    count = Number(countLikes.textContent)
    like = document.getElementById(`like_${likesCount}`)

    dislike = document.getElementById(`dislike_${likesCount}`)
    countDislikes = document.getElementById(`dislikes_${likesCount}`)
    counts = Number(countDislikes.textContent)
    if (like.style.background == 'blue') {
        like.style.background = ""
        like.style.color = ""
        countLikes.innerHTML = + count - 1
    } else {
        like.style.background = "blue"
        like.style.color = "white"
        dislike.style.background = ""
        dislike.style.color = ""
        countLikes.innerHTML = count + 1
        if (countDislikes.textContent == 0) {
            countDislikes.innerHTML = counts
        } else {
            countDislikes.innerHTML = + counts - 1
        }
    }
}

function AddDislike(dislikeCount) {
    countDislikes = document.getElementById(`dislikes_${dislikeCount}`)
    count = Number(countDislikes.textContent)
    dislike = document.getElementById(`dislike_${dislikeCount}`)

    like = document.getElementById(`like_${dislikeCount}`)

    countLikes = document.getElementById(`likes_${dislikeCount}`)
    counts = Number(countLikes.textContent)
    if (dislike.style.background == 'red') {
        dislike.style.background = ""
        dislike.style.color = ""
        countDislikes.innerHTML = + count - 1
    } else {
        dislike.style.background = "red"
        dislike.style.color = "white"
        like.style.background = ""
        like.style.color = ""
        countDislikes.innerHTML = + 1
        if (countLikes.textContent == 0) {
            countLikes.innerHTML = counts
        } else {
            countLikes.innerHTML = counts - 1
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function comentarios(id) {
    comentar = document.getElementById(`comentar_${id}`)
    comentario = document.getElementById(`comentarios_${id}`)
    if (comentario.style.display == 'none') {
        comentario.style.visibility = "visible"
        comentario.style.display = "block"
        comentar.style.display = "block"
        fetch(`/api/comentarios/?id=${id}`)
            .then(response => response.json())
            .then(data => {
                for (let res of data) {
                    if (res.post == id & res.respuestas == "") {
                        comentario.innerHTML +=
                            `<div class="comentario" style="white-space: nowrap; display: inline-block; ">
                                <img src="${res.perfil}" style="height:35px;width: 35px; border-radius: 15px;float: left;">
                                <div style="border: 1px solid #000;border-radius:10px; width: auto; height: auto; max-width: 540px; margin-left: 37px;">
                                    <span >${res.first_name} ${res.last_name} 
                                    </span><br>
                                    <span>${res.comentario}</span>
                                </div>
                            </div>
                            <br>`
                        //<button hx-post="posts/like_comentario/${res.id}" hx-headers='{"X-CSRFToken": ${csrftoken}}' style="margin-left:40px;font-size: 10px;" class="si">Me gusta</button>
                        //<button type="button" style="font-size: 10px;" onclick="responder(${res.id})" class="si">Contestar</button>
                        // <div id="comentario_${res.id}" style="display:none;">
                        //     <form method="post" action="posts/contestar/${res.id}" headers="{"X-CSRFToken": ${csrftoken}}">
                        //         <img src="" style="height:25px;width: 25px; border-radius: 15px;">
                        //         <input type="text" name="comentario" placeholder="responder a ${res.first_name} ${res.last_name}..." class="form-control" style="width: 250px;height: 30px;display:inline-block;border-radius:15px">
                        //     </form>
                        // </div>
                    }
                    // if (res.respuestas == id) {
                    //     comentario.innerHTML +=
                    //         //<form action="posts/contestar/${id}" method="post" style="display: none;" id="comentario_${id}"><img src="${res.perfil}" style="height:25px;width: 25px; border-radius: 15px;"><input type="text" name="comentario" placeholder="responder a comentario.usuario..." class="form-control" style="width: 200px;height: 30px;display:inline-block;border-radius:15px"></form><br>
                    //         `
                    //         <div class="comentario" style="white-space: nowrap; display: inline-block; ">
                    //         <img src="${res.perfil}" style="height:35px;width: 35px; border-radius: 15px;float: left;">
                    //         <div style="border: 1px solid #000;border-radius:10px; width: auto; height: auto; max-width: 540px; margin-left: 37px;">
                    //         <span >${res.first_name} ${res.last_name} 
                    //             </span><br>
                    //             <span>${res.comentario}</span>
                    //         </div>
                    //         <button hx-post="posts/like_comentario/${res.id}" hx-headers='{"X-CSRFToken": csrftoken}' style="margin-left:40px;font-size: 10px;" class="si">Me gusta</button>
                    //         <button type="button" style="font-size: 10px;" onclick="responder(${res.id})" class="si">Contestar</button>
                    //         </div>
                    //         <div id="comentario_${res.id}" style="display:none;"><img src="" style="height:25px;width: 25px; border-radius: 15px;">
                    //         <form><input type="text" name="comentario" placeholder="responder a ${res.first_name} ${res.last_name}..." class="form-control" style="width: 200px;height: 30px;display:inline-block;border-radius:15px"></div>
                    //         <br>`
                    // }
                }
            }
            )
    } else {
        comentario.style.visibility = "hidden"
        comentario.style.display = "none"
        comentario.innerHTML = ""
        comentar.style.display = "none"
    }
}



function sleep(lf_ms) {
    return new Promise(resolve => setTimeout(resolve, lf_ms));
}

async function eliminarNotificacion(id) {
    await sleep(100);
    notificacion = document.getElementById(`notificacion_${id}`)
    notificacion.innerHTML = ""
    alerts = document.querySelector(".alerts")
    alert = Number(alerts.textContent)
    alerts.innerHTML = alert - 1
}


function post() {
    let row = document.querySelector(".row")
    let contenido = document.getElementById("id_contenido").value
    let imagen = document.getElementById("imagenPrevisualizacion").src
    //let disponible = document.getElementById("id_disponible").textContent
    row.innerHTML += `<div class="d-flex justify-content-center">
    <div style="align-items: center; justify-content: center">
        <div class="card" style="width: 34rem; border-radius: 10px;">
            <div class="card-body">
                <h5 class="card-title"><a
                        href="">
                        <img src=""style="height:35px;width: 35px; border-radius: 15px;"></a><a
                        href="">
                    </a> <label>
                    </label><label style="float:right;">
                        <div class="dropdown">
                            <button class="" type="button" id="dropdown1" data-toggle="dropdown" aria-label="Close"
                                style="font-size: 25px; border: none; background: transparent;">...</button>
                            <div class="dropdown-menu">
                                <button class="dropdown-item" hx-get=""
                                hx-target="#dialog">Editar</button>
                                    <button class="dropdown-item" hx-get=""
                                    hx-target="#dialog">Editar</button>
                                <button class=" dropdown-item" hx-post=""
                                    hx-headers=''>Eliminar</button>
                                <a class="dropdown-item" hx-post=""
                                    hx-headers=''>Guardar Post</a>
                            </div>
                        </div>
                </h5>
                <br>
                <p>${contenido}</p>
                <img src="${imagen}"
                    style="height:500px ; width: 500px;">
            </div>
            <div class="debajo">
                <div class="seccion1">
                    <div class=""><label id="likes_"></label> Likes</div>
                    <div class=""><label id="dislikes_"></label> Dislikes
                    </div>
                    <div class="">Comentarios</div>
                    <div class=""> Veces Compartido</div>
                </div>
                <div class="seccion2">
                    <form action="" method="post"><i
                            class="fa-solid fa-thumbs-up"></i><button type="submit" class="si"
                            id="like_"
                            style="background:blue; color:white;"
                            onclick="AddLike()">Like</button></form>
                    <form action="" method="post"><i
                            class="fa-solid fa-thumbs-down"></i><button type="submit" class="si"
                            id="dislike_"
                            style="background:red; color:white;"
                            onclick="AddDislike()">Dislike</button></form>
                    <button class="si" onclick="comentarios()">Comentar</button> 
                    <button class="si" hx-get=""
                        hx-target="#dialog">Compartir</button>
                </div>
                    <form action="" method="post" id="comentar_" style="display:none;margin-bottom: 10px;"><img src="" style="height:35px;width: 35px; border-radius: 15px;"><input
                        style="width: 500px;display:inline-block;border-radius:15px " type="text" class="form-control" name="comentario"
                        placeholder="Escribe un comentario público...">
                    </form>
                <div class="comentarios" id="comentarios_" style="display:none;">
                </div>
            </div>
        </div>
        <br>
    </div>
</div>`

$('#modal').modal('hide')

}

function comentarPost(id,image,user){
    comentar = document.getElementById(`comentar_${id}`)
    comentarios = document.getElementById(`comentarios_${id}`)
    console.log(comentar.lastChild.value)
    comentarios.innerHTML += `
<div class="comentario" style="white-space: nowrap; display: inline-block; ">
    <img src="${image}" style="height:35px;width: 35px; border-radius: 15px;float: left;">
    <div style="border: 1px solid #000;border-radius:10px; width: auto; height: auto; max-width: 540px; margin-left: 37px;">
        <span>${user}</span>
        <br>
        <span>${comentar.lastChild.value}</span>
    </div>
</div>
<br>
`
}