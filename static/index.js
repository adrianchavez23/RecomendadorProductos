
const Productos_Por_Empaque = document.getElementById("Productos_Por_Empaque");
const ProdKey = document.getElementById("ProdKey");
const Brand = document.getElementById("Brand");
const MLSize = document.getElementById("MLSize");
const Returnability = document.getElementById("Returnability");
const Size = document.getElementById("Size");
const Flavor = document.getElementById("Flavor");
const Container = document.getElementById("Container");
const ProductType = document.getElementById("ProductType");

const loadingOverlay = document.getElementById("loading-overlay");

const enviarButton = document.getElementById("enviar");

const resultado = document.getElementById("resultado");

enviarButton.addEventListener('click', ()=> {

   // Show the overlay
  loadingOverlay.style.display = 'block';
  enviarButton.disabled = true;

  const nuevoProducto = {
    Productos_Por_Empaque: Productos_Por_Empaque.value,
    ProdKey: ProdKey.value,
    Brand: Brand.value,
    MLSize: MLSize.value,
    Returnability: Returnability.value,
    Size: Size.value,
    Flavor: Flavor.value,
    Container: Container.value,
    ProductType: ProductType.value
  };

  // Send the HTTP request
  fetch('http://127.0.0.1:3001/predict', {  // replace with the actual endpoint
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(nuevoProducto)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Success:', data);
    renderTable(data.resultados);
    // resultado.textContent = data.prediction;
    // Handle success (e.g., show success message to user)
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
    // Handle error (e.g., show error message to user)
  })
  .finally(() => {
    // Hide the overlay
    loadingOverlay.style.display = 'none';

    // Re-enable the button
    enviarButton.disabled = false;
  });

})

function renderTable(resultados) {

  const tableBody = document.querySelector("#clients-table tbody");
  tableBody.innerHTML = '';

  if (resultados.length > 0 ) {
    resultados.forEach(client => {
      const row = document.createElement('tr');
      
      const nameCell = document.createElement('td');
      nameCell.textContent = client.CustomerId;
      const successPercentageCell = document.createElement('td');
      successPercentageCell.textContent = (client.Porcentaje).toFixed(2);
  
      row.appendChild(nameCell);
      row.appendChild(successPercentageCell);
  
      tableBody.appendChild(row);
    });

    // Show the table
    const table = document.getElementById('clients-table');
    table.style.display = 'table';  // Show the table

    // Hide the no-results message
    document.getElementById('no-results').style.display = 'none';

  } else {
     // Show the "No results" message
     const table = document.getElementById('clients-table');
     table.style.display = 'none';  // Hide the table

     document.getElementById('no-results').style.display = 'table-row';  // Show the no-results message
  }
  
}

document.getElementById('clear-all').addEventListener('click', function() {
  // Clear form inputs
  Productos_Por_Empaque.value = '';
  ProdKey.value = '';
  Brand.value = '';
  MLSize.value = '';
  Returnability.value = '';
  Size.value = '';
  Flavor.value = '';
  Container.value = '';
  ProductType.value = '';

  // Clear table data
  const tableBody = document.querySelector('#clients-table tbody');
  tableBody.innerHTML = '<tr id="no-results"><td colspan="2" class="no-results-message">No hay resultados disponibles.</td></tr>';
});
