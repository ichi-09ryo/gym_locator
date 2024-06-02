function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: { lat: 35.6895, lng: 139.6917 }
  });

  var gyms = [
    { lat: 35.6957, lng: 139.698, name: 'エニタイムフィットネス新宿西口店', prefecture: '東京都' },
    { lat: 35.6928, lng: 139.722, name: 'エニタイムフィットネス曙橋店', prefecture: '東京都' },
    // 他のジムのデータを追加
  ];

  var markers = gyms.map(function(gym) {
    var marker = new google.maps.Marker({
      position: { lat: gym.lat, lng: gym.lng },
      map: map,
      title: gym.name,
      icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    });

    marker.set('prefecture', gym.prefecture);

    return marker;
  });

  document.getElementById('prefecture-select').addEventListener('change', function() {
    var selectedPrefecture = this.value;
    filterGymsByPrefecture(selectedPrefecture);
  });

  function filterGymsByPrefecture(prefecture) {
    markers.forEach(function(marker) {
      if (prefecture === 'all' || marker.get('prefecture') === prefecture) {
        marker.setMap(map);
      } else {
        marker.setMap(null);
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', function() {
  initMap();
});