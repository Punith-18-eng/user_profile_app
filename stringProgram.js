const prompt = require('prompt-sync')();

// Function to create a student object
function createStudent() {
  // Collect inputs for the student object
  let student = {
    name: prompt("Enter the student's name: "),
    grade: parseInt(prompt("Enter the student's grade: ")),
    subjects: prompt("Enter the student's subjects separated by commas: ").split(',').map(subject => subject.trim()),
  };
  return student;
}

// Function to display student details
function displayInfo(student) {
  console.log("Student Details:");

  // Loop through the properties of the student object and log the keys and values
  for (let key in student) {
    if (typeof student[key] !== 'function') {
      console.log(`${key}: ${student[key]}`);
    }
  }

  // Log whether the student passed based on the 'passed' property
  console.log("Passed:", student.passed ? "Yes" : "No");
  console.log("\t");
}

let student = createStudent(); // Collect details and return student object
// Dynamically add 'passed' property based on grade
student.passed = student.grade >= 40;
displayInfo(student);
