// Funciones de unir pdf 
//funcion limpiar y enviar
function enviar_unir_pdf() {
    let formulario = document.getElementById('form_data_unir');
    var div_alert = document.querySelector('#div_alert_1');
    //formulario.submit(); 
    setTimeout(function () { formulario.reset() }, 10);
    div_alert.remove();
}
// Funciones de unir x carpetas pdf
//funcion limpiar y enviar
function enviar_carpeta_pdf() {
    let formulario = document.getElementById('form_carpeta_unir');
    var div_alert = document.querySelector('#div_alert_2');
    var div_alert2 = document.querySelector('#div_alert_3');
    //formulario.submit(); 
    setTimeout(function () { formulario.reset() }, 10);
    div_alert.remove();
    div_alert2.remove();
}
// Funciones de dividir pdf
//funcion limpiar y enviar
function enviar_dividir() {
    let formulario = document.getElementById('form_data_dividir');
    var div_alert = document.querySelector('#div_alert_4');
    var div_alert2 = document.querySelector('#div_alert_5');
    //formulario.submit();
    setTimeout(function () { formulario.reset() }, 10);
    div_alert.remove();
    div_alert2.remove();
}
// Funcion de extraer hoja
//funcion limpiar y enviar
function enviar_extraer_hoja() {
    let formulario = document.getElementById('form_data_extraer');
    var div_alert = document.querySelector('#div_alerta_7');
    console.log(div_alert, formulario)
    //formulario.submit();
    setTimeout(function () { formulario.reset() }, 10);
    div_alert.remove();
}

// Funciones de extrear rango pdf
//funcion limpiar y enviar
function enviar_extraer_rango() {
    let formulario = document.getElementById('form_data_extraer_range');
    var div_alert = document.querySelector('#div_alert_8');
    //formulario.submit();
    console.log(formulario, div_alert)
    setTimeout(function () { formulario.reset() }, 10);
    div_alert.remove();
}


function Girar(image, volteado, estado, mostrador) {
    var angle = ($('#' + image).data('angle') + 90) || 90;
    if (angle == 360) { angle = 0; }
    $('#' + image).data('angle', angle);
    var img = document.querySelector('#' + image);
    img.setAttribute('data_rotate', angle);
    var contador = img.getAttribute("contador");
    sumador = parseInt(contador) + 1;
    if (sumador == 5) { sumador = 1; }
    img.setAttribute('contador', sumador);
    residuo = sumador % 2;
    var voltea = document.querySelector('#' + volteado);
    var estados = document.querySelector('#' + estado);
    document.getElementById(mostrador).innerHTML = angle+"°"; 


    if (estados.value == 1) {
        if (voltea.value == 0) {
            if (residuo == 0) { scale = 0.7; }
            if (residuo == 1) { scale = 1; }
            $('#' + image).css({ 'transform': 'rotate(' + angle + 'deg) scale(' + scale + ')' });
        }
        if (voltea.value == 1) {
            if (residuo == 0) {
                scale = 1.3;
                var top = 95 - ((img.clientHeight / 2));
                $('#' + image).css({ 'position': 'relative', 'top': '' + top + 'px' });
            }
            else {
                $('#' + image).css({ 'position': 'relative', 'top': '0px' });
                scale = 1;
            }
            $('#' + image).css({ 'transform': 'rotate(' + angle + 'deg) scale(' + scale + ')' });
        }
    } else {
        if (voltea.value == 0) {
            if (residuo == 0) { scale = 0.7; }
            if (residuo == 1) { scale = 1; }
            $('#' + image).css({ 'transform': 'rotate(' + angle + 'deg) scale(' + scale + ')' });
        }
        if (voltea.value == 1) {
            if (residuo == 0) {
                scale = 1.6;
                $('#' + image).css({ 'position': 'relative', 'top': '75px' });
            }
            else {
                $('#' + image).css({ 'position': 'relative', 'top': '0px' });
            }
            if (residuo == 1) { scale = 1; }
            $('#' + image).css({ 'transform': 'rotate(' + angle + 'deg) scale(' + scale + ')' });
        }

    }


    //img.setAttribute('contador',contador);
    console.log(sumador, residuo)




}

function eliminar(div_eliminar) {
    var elem = document.querySelector("#" + div_eliminar);
    elem.remove();
}

var source;

function isbefore(a, b) {
    if (a.parentNode == b.parentNode) {
        for (var cur = a; cur; cur = cur.previousSibling) {
            if (cur === b) {
                return true;
            }
        }
    }
    return false;
}


function dragenter(e) {
    var targetelem = e.target;

    while (!targetelem.classList.contains("bandera")) {
        targetelem = targetelem.parentNode;
    }

    if (isbefore(source, targetelem)) {
        targetelem.parentNode.insertBefore(source, targetelem);
        console.log(source.classList, targetelem.classList)

    } else {
        targetelem.parentNode.insertBefore(source, targetelem.nextSibling);
    }

}

function dragstart(e) {
    source = e.target;

    while (!source.classList.contains("bandera")) {
        source = source.parentNode;

    }
    if (source.classList.contains("bandera") == true) {
        e.dataTransfer.effectAllowed = 'move';
    }

}

function lectorOrden() {

    var valorLista = [];
    let contenedor = document.getElementsByName('listaHojas')[0];
    let articles = contenedor.getElementsByClassName('bandera2');
    let formulario = document.getElementById('enviar_json');

    for (var i = 0; i < articles.length; i++) {
        if (articles != null) {
            var img_rotate = articles[i].querySelector('img');
            var numero_pg = articles[i].id;
            var rotacion_pag = img_rotate.getAttribute('data_rotate');
            valorLista.push({ numero_pg, rotacion_pag });
        }
    }

    var json = JSON.stringify(valorLista)

    document.getElementById("listaOrden").value = json;
    //buscar el formulario y hacer el post desde aca 

    formulario.submit();
    return false;


}



