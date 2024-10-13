// document.getElementById("obtener_ticket").addEventListener("click", async function() {
//   await Swal.fire({
//     title: 'Ingresa tus datos para obtener tu ticket',
//     html: '<input id="nombre" class="swal2-input" placeholder="Nombre">' +
//           '<input type="number" id="cedula" class="swal2-input" placeholder="Cedula">',
//     focusConfirm: false,
//     showCancelButton: true,
//     confirmButtonText: 'Guardar',
//     confirmButtonColor: '#095',
//     cancelButtonText: 'Cancelar',
//     cancelButtonColor: '#d33',
//     customClass: {
//         popup: 'custom-swal-popup',
//         title: 'custom-swal-title',
//         htmlContainer: 'custom-swal-html',
//     },
//     preConfirm: () => {
//       const nombre = document.getElementById('nombre').value;
//       const cedula = document.getElementById('cedula').value;
//       if (!nombre || !cedula) {
//         Swal.showValidationMessage('Por favor ingrese ambos campos')
//       }
//       return {nombre: nombre, cedula: cedula};
//     }
//   }).then((result) => {
//     if(result.isConfirmed){
//       fetch('/guardar_usuario/', {
//         method: 'POST',
//         headers: {
//           'content-type': 'application/json',
//           'X-CSRFToken':csrToken
//         },
//         body: JSON.stringify(result.value)
//       })
//       .then(response =>{
//       if(response.ok){
//         window.location.href='/';
//        }
//       })
//       .then(data => {
//         if (data.success) {
//           Swal.fire({
//             title:'Ticket Generado',
//             icon:'success'});
//         }else {
//           Swal.fire({
//             title:'Error',
//             text:'No se pudo generar el ticket',
//             icon:'error'});
//         }
//       }).catch( error => {
//             Swal.fire('Error','Ocurrio un error inesperado','error');
//       });
//     }
//   });
// });
//
// console.log('hola desde git')