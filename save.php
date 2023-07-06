<?php
   $conn = mysqli_connect('localhost','root','','test');
   if(!$conn){
      echo "connection unsuccessful";
   }else{
   $firstname = $_POST['firstname'];
   $email= $_POST['email'];
   $address = $_POST['address'];
   $city = $_POST['city'];
   $state = $_POST['state'];
   $pin = $_POST['zip'];
   
   $sql = "INSERT INTO registration (firstname , email , address , city , state , zip)
   VALUES ('$firstname','$email','$address','$city','$state','$pin')";

   if ($conn->query($sql) === TRUE) {
      echo "<h1><center>ORDER BOOKED</center></h1>";
   }else{
      echo "Error: " . $sql . "<br>" , $conn->error;
   }
    $conn->close();
   }
?>