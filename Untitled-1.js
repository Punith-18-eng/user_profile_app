// Create an array of 5 cities
let cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata"];

// Log the total number of cities
console.log("Total number of cities:", cities.length);

// Add a new city at the end
cities.push("Hyderabad");
console.log("After adding a new city:", cities);

// Remove the first city
cities.shift();
console.log("After removing the first city:", cities);

// Find and log the index of a specific city
let index = cities.indexOf("Bangalore");
console.log("Index of Bangalore:", index);