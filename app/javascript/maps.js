function initMap() {
  var mapElement = document.getElementById('map');
  if (!mapElement) return;

  var gymsData = mapElement.getAttribute('data-gyms');
  var gyms = JSON.parse(gymsData);

  // 最初のジムの位置を中心に設定
  var initialLatLng = gyms.length > 0 ? { lat: gyms[0].latitude, lng: gyms[0].longitude } : { lat: 35.6895, lng: 139.6917 }; // 東京をデフォルトに設定

  var map = new google.maps.Map(mapElement, {
    zoom: 12,
    center: initialLatLng
  });

  var infowindow = new google.maps.InfoWindow();

  gyms.forEach(function(gym) {
    var marker = new google.maps.Marker({
      position: { lat: gym.latitude, lng: gym.longitude },
      map: map,
      title: gym.gym_name,
      icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    });

    marker.addListener('mouseover', function() {
      infowindow.setContent('<div><strong>' + gym.gym_name + '</strong><br>' + gym.address + '</div>');
      infowindow.open(map, marker);
    });

    marker.addListener('mouseout', function() {
      infowindow.close();
    });

    var listItem = document.createElement('li');
    listItem.className = 'list-group-item';
    
    // ジム名と住所を別々のdivにして、2段に分けたい
    var gymNameDiv = document.createElement('div');
    gymNameDiv.className = 'gym-name';
    gymNameDiv.textContent = gym.gym_name;

    var gymAddressDiv = document.createElement('div');
    gymAddressDiv.className = 'gym-address';
    gymAddressDiv.textContent = gym.address;

    listItem.appendChild(gymNameDiv);
    listItem.appendChild(gymAddressDiv);

    listItem.addEventListener('click', function() {
      map.setCenter(marker.getPosition());
      infowindow.setContent('<div><strong>' + gym.gym_name + '</strong><br>' + gym.address + '</div>');
      infowindow.open(map, marker);
    });

    document.getElementById('gym-list').appendChild(listItem);
  });
}

// initMapをグローバルに設定
window.initMap = initMap;

document.addEventListener('turbolinks:load', function() {
  initMap();
});