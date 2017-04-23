<html>
   <head>
      <title>Connect to MariaDB Server</title>
   </head>

   <body>
      <?php
         $dbhost = 'localhost:3036';
         $dbuser = 'root';
         $dbpass = 'pjr9npassword';
         $conn = mysqli_connect($dbhost, $dbuser, $dbpass);
      
	          if(! $conn ) {
			              die('Could not connect: ' . mysql_error());
				               }
	          
	          echo 'Connected successfully';
	          mysql_close($conn);
		        ?>
   </body>
</html>
