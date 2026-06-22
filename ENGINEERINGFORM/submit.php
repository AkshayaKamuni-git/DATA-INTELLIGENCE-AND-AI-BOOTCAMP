<?php

$conn = new mysqli("localhost", "root", "", "engineering_db");

if ($conn->connect_error) {
    die("Connection Failed: " . $conn->connect_error);
}

$name = $_POST['name'];
$email = $_POST['email'];
$phone = $_POST['phone'];
$gender = $_POST['gender'];
$dob = $_POST['dob'];
$branch = $_POST['branch'];
$address = $_POST['address'];

$sql = "INSERT INTO applications
(name,email,phone,gender,dob,branch,address)
VALUES
('$name','$email','$phone','$gender','$dob','$branch','$address')";

if ($conn->query($sql) === TRUE) {
    echo "<h2>Application Submitted Successfully!</h2>";
} else {
    echo "Error: " . $conn->error;
}

$conn->close();

?>