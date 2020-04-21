// $("#articulos").val($("#articulos option:eq(5)").val());
// $("#articulos").selectmenu("refresh");


var productos = ['Azúcar', 'Leche en polvo/cartón', 'Yerba', 'Panificados secos', 'Harina', 'Aceite', 'Pollo/Carne enlatada', 'Poroto', 'Arroz', 'Fideo', 'Detergente', 'Jabón en pan', 'Alcohol líquido a 70%', 'Sal', 'Lavandina']

function agregarArticulo() {
  var list = document.getElementById('list')
  var articulo = document.getElementById('articulo').value
  var nombreArticulo = document.getElementById('articulo').children[articulo - 1].innerHTML
  var unidad = nombreArticulo.slice(nombreArticulo.indexOf("("));
  nombreArticulo = nombreArticulo.slice(0, - (nombreArticulo.length - nombreArticulo.indexOf('(')))
  var cantidad = document.getElementById('cantidad').value
  //Agrega al final

  // listaArticulos.push(articulo)// guardamos el id del articulo 
  // listaCantidades.push(cantidad)

  // var row = table.insertRow()
  var newItem = document.createElement('li')
  newItem.classList.add('list-group-item')
  newItem.appendChild(document.createTextNode(nombreArticulo + ' ' + cantidad + unidad))
  list.appendChild(newItem)
}

function envio() {
  console.log(listaArticulos)
  console.log(listaCantidades)

  $.post('cargarlista',
    {
      articulos: listaArticulos,
      cantidades: listaCantidades
    },
    function (response) {
      alert(response.mensaje);
    });
}