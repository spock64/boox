<html>
   <head>
      <title>Login Test ... </title>
   </head>

   <body>
      <?php
         $dbhost = 'mysql';
         $dbuser = 'root';
         $dbpass = 'pjr9npassword';
         $db = 'JTEST';

         $conn = new mysqli($dbhost, $dbuser, $dbpass, $db);

	       if( $conn->connect_errno ) {
			              die('Could not connect: ' . $conn->connect_errno);
				               }

	       echo '<p>Connected successfully</p>';

         $q = "SELECT * from USERS WHERE NAME = '" . $_GET['USER'] . "'";


         $r = $conn->query($q);

         if(!$r)
         {
           die('could not retrieve user ' . $conn->error);
         }

         echo '<p>' . $r->num_rows . ' Selected</p><p>';

         while($row = $r->fetch_assoc())
         {
           echo 'Name ' . $row['NAME'] . ' pw ' . $row['PW'] . '<br>';
         }

         echo 'Done</p>';

	       $conn->close();

         echo '<p>DB Closed</p>';
		   ?>
   </body>
</html>
