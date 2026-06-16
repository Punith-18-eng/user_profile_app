// JavaScript Program to Print Prime Numbers Between 1 and 100
// Using Loops and Conditions

console.log("Prime Numbers Between 1 and 100:\n");

// Outer loop to check numbers from 1 to 100
for (let number = 2; number <= 100; number++) {

    // Assume the number is prime
    let isPrime = true;

    // Inner loop to check divisibility
    for (let i = 2; i <= number / 2; i++) {

        // If number is divisible by i
        if (number % i === 0) {

            // Number is not prime
            isPrime = false;

            // Exit loop
            break;
        }
    }

    // If number is prime, print it
    if (isPrime === true) {
        console.log(number);
    }
}