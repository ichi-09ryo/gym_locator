function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: { lat: 35.6895, lng: 139.6917 }
  });

  var gyms = [
    { lat: 35.6957, lng: 139.698, name: 'エニタイムフィットネス新宿西口店' },
    { lat: 35.6928, lng: 139.722, name: 'エニタイムフィットネス曙橋店' },
    // 他のジムのデータを追加
  ];

  gyms.forEach(function(gym) {
    new google.maps.Marker({
      position: { lat: gym.lat, lng: gym.lng },
      map: map,
      title: gym.name,
      icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    });
  });
}

document.addEventListener('DOMContentLoaded', function() {
  initMap();
});