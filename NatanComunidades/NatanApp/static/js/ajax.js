console.log('entro en el js')
$(document).ready(function () {
    console.log('entro en el codigo jquery')
    console.log(document.getElementById('nombre-comunidad').value )
    $("#formulario").bind("submit",function(){
        // se captura el boton de envio
        var btnEnviar = $("#enviar");
        console.log('entro en la funcion');
        $.ajax({
            type: $(this).attr("method"),
            url: $(this).attr("action"),
            data:{ 
                iden: document.getElementById('nombre-comunidad').value,
                estado:document.getElementById('estado').value
            },
            beforeSend: function(){
                /*
                * Esta función se ejecuta durante el envió de la petición al
                * servidor.
                * */
                // btnEnviar.text("Enviando"); 
                btnEnviar.val("Enviando"); // Para input de tipo button
                // btnEnviar.attr("disabled","disabled");
                console.log('se esta ejecutando la peticion')

            },
            complete:function(data){
                /*
                * Se ejecuta al termino de la petición
                * */
                btnEnviar.val("Enviado");
                btnEnviar.removeAttr("disabled");
                console.log('se realizo la peticion' + data.message)
            },
            success: function(data){
                /*
                * Se ejecuta cuando termina la petición y esta ha sido
                * correcta
                * */
                // $(".respuesta").html(data);
                alert("Los datos se actualizaron correctamente ");
                console.log('se completo la peticion')
                window.location='/mapa_distribucion'
            },
            error: function(data){
                /*
                * Se ejecuta si la peticón ha sido erronea
                * */
                alert("Problemas al tratar de enviar el formulario");
                console.log('no se realizo la peticion')
            }
        });
        // Nos permite cancelar el envio del formulario
        return false;
    });
});