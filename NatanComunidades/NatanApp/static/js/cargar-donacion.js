
var listaArticulos = []
var listaCantidades = []

function agregarArticulo() {

  // se obtienen los elementos del nuevo articulo a cargar
  var list = document.getElementById('list')
  var articulo = document.getElementById('articulo').value
  var nombreArticulo = document.getElementById('articulo').children[articulo - 1].innerHTML

  // se extraen las partes del texto que va a ir formateado en la lista
  var unidad = nombreArticulo.slice(nombreArticulo.indexOf("("));
  nombreArticulo = nombreArticulo.slice(0, - (nombreArticulo.length - nombreArticulo.indexOf('(')))
  var cantidad = document.getElementById('cantidad').value
  //Agrega al final

  if (cantidad === '' || cantidad === null || cantidad === 0) {
    return null
  }

  listaArticulos.push(articulo)
  listaCantidades.push(cantidad)

  // se crea un nuevo itema para la lista y se le agrega la clase
  var newItem = document.createElement('li')
  newItem.setAttribute('id', articulo - 1)
  newItem.setAttribute('class', 'list-group-item d-flex flex-row')

  // se agrega el contenido textual al list item
  var parrafo = document.createElement('p')
  var texto = document.createTextNode(nombreArticulo + ' - ' + cantidad + unidad)
  parrafo.setAttribute('class', 'w-100 my-auto')
  parrafo.setAttribute('style', 'vertical-align: middle;')
  parrafo.appendChild(texto)
  newItem.appendChild(parrafo)

  // se agrega el botón eliminar
  var btn = document.createElement('BUTTON')
  btn.innerHTML = 'Borrar'
  btn.addEventListener("click", borrar)
  btn.setAttribute('class', 'btn flex-shrink-1')
  btn.setAttribute('style', 'background-color: #6200ED; color: white;')

  newItem.appendChild(btn)

  // se agrega el item a la lista
  list.appendChild(newItem)

  document.getElementById('cantidad').value = ''
  envio()
}

function borrar(e) {
  e.target.parentElement.remove()
  var posicion_a_eliminar=e.target.parentElement.attributes[0].nodeValue
  var pos_en_lista= listaArticulos.indexOf(posicion_a_eliminar);
  listaArticulos.splice(pos_en_lista,1)
  listaCantidades.splice(pos_en_lista,1)

 
  console.log(typeof(posicion_a_eliminar))
  console.log(posicion_a_eliminar)
  envio()
}

function envio() {
  // console.log(listaArticulos)
  // console.log(listaCantidades)
  var counter = document.getElementById('list').childElementCount
  console.log(counter)
  if ( counter === 0 || donante === '' || donante === null){
    return null
  }

  $.post('/cargarlista',
    {
      articulos: listaArticulos,
      cantidades: listaCantidades
    },
    function (response) {
      console.log(response.mensaje);
    });
}
function mostrar(pagina){
  console.log(pagina)
  window.location= pagina

}