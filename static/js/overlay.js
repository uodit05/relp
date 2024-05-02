// overlay.js

function openOverlay(name, price, address, bedrooms, bathrooms, sqft, ptype, description) {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("property-name").innerText = name;
    document.getElementById("property-price").innerText = price;
    document.getElementById("property-address").innerText = address;
    document.getElementById("property-bedrooms").innerText = bedrooms;
    document.getElementById("property-bathrooms").innerText = bathrooms;
    document.getElementById("property-sqft").innerText = sqft;
    document.getElementById("property-ptype").innerText = ptype;
    document.getElementById("property-description").innerText = description;
}

function closeOverlay() {
    document.getElementById("overlay").style.display = "none";
}
