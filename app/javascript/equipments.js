document.addEventListener("DOMContentLoaded", function() {
  fetch('/equipments.json')
    .then(response => response.json())
    .then(data => {
      const equipmentList = document.getElementById('equipmentList');
      data.forEach(equipment => {
        const listItem = document.createElement('li');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'equipment[]';
        checkbox.value = equipment;

        const label = document.createElement('label');
        label.textContent = equipment;

        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        equipmentList.appendChild(listItem);
      });
    });

  document.getElementById('searchButton').addEventListener('click', function() {
    const form = document.getElementById('equipmentForm');
    const formData = new FormData(form);
    const selectedEquipments = formData.getAll('equipment[]');

    window.location.href = `/map?equipments=${selectedEquipments.join(',')}`;
  });
});