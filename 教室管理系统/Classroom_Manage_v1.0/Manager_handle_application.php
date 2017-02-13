<!--
	get_unhandled_application.php
	Function: Get un-handled applications from database and show them on page, for Manager
	Author: gyc,wq 
	Last Update: 2016 Nov 30
-->

<?php
	session_start();

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	//get user type and user id
	$user_type = $_SESSION["user_type"];
	if($user_type != 'Manager')
	{
		print<<<EOT
				<script>
					alert('user_type error');
					location.href='home.html';
				</script>
EOT;
	}
	$id = $_SESSION["user_id"];

	//get applications with vertify equals to 0, which means these applications were not handled
	$query = "SELECT * FROM Application WHERE vertify = '0'";
	$result = $conn->query($query);
	if(!$result)
	{
		die('Connect Error');
	}

	//show all items in a table
	print<<<EOT
	<head>
		<title>Manager Handle Applications</title>
		<link rel="stylesheet" type="text/css" href="view_schedule.css">
	</head>

	<body>
		<div id = 'div1'>
			<h1 align="center">Handle Application</h1>
			<table>
				<tr>
					<td>Application ID</td>
					<td>User Type</td>
					<td>Size</td>
					<td>Week</td>
					<td>Day</td>
					<td>Course Begin</td>
					<td>Course End</td>
					<td>Reason</td>
					<td>Action</td>
				</tr>
EOT;
	for ($i = 0 ; $i < $result->num_rows ; $i++)
	{
		$result->data_seek($i);
		$row = $result->fetch_assoc();

		$application_id = $row['application_id'];
		$user_type = $row['user_type'];
		$size = $row['size'];
		$week = $row['week'];
		$day = $row['day'];
		$course_begin = $row['course_begin'];
		$course_end = $row['course_end'];
		$reason = $row['reason'];

		switch ($user_type) 
		{
			case 's':
				$user_type = 'Student';
				break;

			case 'p':
				$user_type = 'Professor';
				break;

			case 'e':
				$user_type = 'External';
				break;
			
			default:
				break;
		}

		//Here, for each item, I used post method to jump to another page(get_available_classroom.php)
		print<<<EOT
			<tr>
				<td>$application_id</td>
				<td>$user_type</td>
				<td>$size</td>
				<td>$week</td>
				<td>$day</td>
				<td>$course_begin</td>
				<td>$course_end</td>
				<td>$reason</td>
				<td>
					<form action="get_available_classroom.php" method="post">
						<input type="hidden" name="application_id" value="$application_id">
						<input type="hidden" name="size" value="$size">
						<input type="hidden" name="week" value="$week">
						<input type="hidden" name="day" value="$day">
						<input type="hidden" name="course_begin" value="$course_begin">
						<input type="hidden" name="course_end" value="$course_end">
						<input type="submit" value="Handle">
					</form>
				</td>
			</tr>
EOT;
	}
	print<<<EOT
			</table>
			<br>
			<a href="Manager_menu.php"><input type="button" value="Go Back"></a>
		</div>
	</body>	
EOT;
	
	$conn->close();
?>
