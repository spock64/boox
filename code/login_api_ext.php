<?php

  header("Content-Type: application/json;charset=utf-8");

  // include('includes/json.php');

  $dbhost = 'mysql';
  $dbuser = 'root';
  $dbpass = 'pjr9npassword';
  $db = 'JTEST';

  // JSON results ...
  $js_out = array();

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

  $q_channels = "SELECT CHANNELID from USERCHANNEL WHERE USERID = '" . $row['ID'] . "'";

  $r_channels = $conn->query($q_channels);

  if(!$r_channels)
  {
   die('could not retrieve channels ' . $conn->error);
  }

  // Loop through the returned channels getting channel metadata for each
  if ($r_channels->num_rows < 1)
  {
    die('no channels for user '.$row['ID']);
  }

  // output metadata for each row
  while($row = $r_channels->fetch_assoc())
  {
    // run a query to get the metadata ...
    $q_meta = "SELECT * from CHANNELS WHERE ID = '" . $row['CHANNELID'] . "'";

    $r_meta = $conn->query($q_meta);

    if(!$r_meta)
    {
      die('could not get metadata for channel id '.$row['CHANNELID']);
    }

    if($r_meta->num_rows <> 1)
    {
      die('found multiple rows for channel id '.$row['CHANNELID'] . ' num = '. $r_channels->num_rows);
    }

    // So we have one row of metadata, retrive it and add to $js_out
    $meta = $r_meta->fetch_assoc();

    array_push($js_out, $meta);
  }


  echo json_encode($js_out);

  $conn->close();

?>
