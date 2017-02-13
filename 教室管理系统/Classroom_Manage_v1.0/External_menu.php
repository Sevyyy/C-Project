<!--
	External_menu.php
	Function: Menu for External
	Author: gyc
	Last Update: 2016 Nov 30
-->

<!doctype html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>External Home Page</title>
		<link rel="stylesheet" type="text/css" href="menu.css">
	</head>

	<body>
		<div id = 'div1'>
			<h1 align="center">Classroom Management System</h1>
		
<?php
	session_start();  //for the _SESSION, something like cookie

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	$id = $_SESSION["user_id"];
	$query = "SELECT * FROM External WHERE external_id = '$id'";
	$result = $conn->query($query);

	$result->data_seek(0);
	$row = $result->fetch_assoc();

	$name = $row['name'];
	$email = $row['email'];

	print<<<EOT
	<div id = 'div2'>
		<tp>
			Welcome, $name
		</p>

		<tp>
			Email: $email
		</p>
	</div>
EOT;
	$conn->close();
?>
			<table>
				<tr>
					<!--
					<td>
						<a href="User_view_vacant_classroom.php"><input type="button" value="View Vacant Classroom" style="width:150px;height:50px"></input></a> 
					</td>
					-->
			
					<td>
						<a href="User_apply_classroom.php"><input type="button" value="Apply Classroom" style="width:150px;height:50px"></input></a>
					</td>

					<td>
						<a href="view_application.php"><input type="button" value="View Your Applications" style="width:150px;height:50px"></input></a> 
					</td>
				
					<td>
						<a href="home.html"><input type="button" value="Log Out" style="width:150px;height:50px"></input></a>
					</td>
				</tr>
			</table>
		</div>
	</body>
</html>