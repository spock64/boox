<html>
   <head>
      <title>Connect to DB </title>
   </head>

   <body>
      <?php
         $dbhost = 'localhost';
         $dbuser = 'root';
         $dbpass = 'pjr9npassword';
         $db = 'JTEST';

         $conn = new mysqli($dbhost, $dbuser, $dbpass, $db);

	       if( $conn->connect_errno ) {
			              die('Could not connect: ' . $conn->connect_errno);
				               }

	       echo 'Connected successfully';
	       $conn->close();
		   ?>
   </body>
</html>
