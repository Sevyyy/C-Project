<!--
	Student_menu.php
	Function: Menu for Student
	Author: gyc
	Last Update: 2016 Nov 29
-->

<!doctype html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Student Home Page</title>
		<link rel="stylesheet" type="text/css" href="menu.css">
	</head>

	<body>
		<div id = 'div1'>
			<h1 align="center">Classroom Managerment System</h1>

<?php
	session_start();  //for the _SESSION, something like cookie

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	$id = $_SESSION["user_id"];
	$query = "SELECT * FROM Student WHERE student_id = '$id'";
	$result = $conn->query($query);

	$result->data_seek(0);
	$row = $result->fetch_assoc();

	$name = $row['name'];
	$grade = $row['grade'];
	$major = $row['major'];
	$email = $row['email'];

	print<<<EOT
	<div id = 'div2'>
		<tp>
			Welcome, $name
		</p>

		<tp>
			Grade: $grade
		</p>

		<tp>
			Major: $major
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
					<td>
						<a href="User_change_password.php"><input type="button" value="Change Password" style="width:150px;height:50px"></input></a>
					</td>

					<td>
						<a href="Student_view_schedule.php"><input type="button" value="View Schedule" style="width:150px;height:50px"></input></a>
					</td>

					<td>
						<a href="User_view_vacant_classroom.php"><input type="button" value="View Vacant Classroom" style="width:150px;height:50px"></input></a> 
					</td>
				</tr>

				<tr>
					<td>
						<a href="User_apply_classroom.php"><input type="button" value="Apply Classroom" style="width:150px;height:50px"></input></a>
					</td>

					<td>
						<a href="view_application.php"><input type="button" value="View Your Applications" style="width:150px;height:50px"></input></a>
					</td>

					<td>
						<a href="User_report_repair.php"><input type="button" value="Report Repair" style="width:150px;height:50px"></input></a>
					</td>
				</tr>

				<tr>
					<td>
					</td>
					<td>
						<a href="home.html"><input type="button" value="Log Out" style="width:150px;height:50px;"></input></a>
					</td>
				</tr>
			</table>
		</div>	
	</body>
</html>