<?php

  header("Content-Type: application/json;charset=utf-8");

  include('includes/json.php');

  $dbhost = 'mysql';
  $dbuser = 'root';
  $dbpass = 'pjr9npassword';
  $db = 'JTEST';

  $conn = new mysqli($dbhost, $dbuser, $dbpass, $db);

  if( $conn->connect_errno ) {
            die('Could not connect: ' . $conn->connect_errno);
               }

  $q = "SELECT * from USERS WHERE NAME = '" . $_GET['USER'] . "'";

  $r = $conn->query($q);

  if(!$r)
  {
   die('could not retrieve user ' . $conn->error);
  }

  $row = $r->fetch_assoc();

  $q_channels = "SELECT * from USERCHANNEL WHERE USERID = '" . $row['ID'] . "'";

  $r_channels = $conn->query($q_channels);

  if(!$r_channels)
  {
   die('could not retrieve channels ' . $conn->error);
  }

  $js_out = array();

  $js_out = $r_channels->fetch_all(MYSQLI_ASSOC);

  echo json_encode($js_out);

  $conn->close();

?>
