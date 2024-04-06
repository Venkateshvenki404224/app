function initAutocomplete() {
    var pickupInput = document.getElementById('pickup_location');
    var dropoffInput = document.getElementById('dropoff_location');

    var autocompletePickup = new google.maps.places.Autocomplete(pickupInput);
    var autocompleteDropoff = new google.maps.places.Autocomplete(dropoffInput);

    autocompletePickup.addListener('place_changed', function () {
        var place = autocompletePickup.getPlace();
        document.getElementById('pickup_lat').value = place.geometry.location.lat();
        document.getElementById('pickup_lng').value = place.geometry.location.lng();
    });

    autocompleteDropoff.addListener('place_changed', function () {
        var place = autocompleteDropoff.getPlace();
        document.getElementById('dropoff_lat').value = place.geometry.location.lat();
        document.getElementById('dropoff_lng').value = place.geometry.location.lng();
    });
}