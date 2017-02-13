<!--
	view_vacant_classroom.php
	Function: get data from database with specific week, day, course begin and end, for Student and Professor.
	Author: gyc
	Last Update: 2016 Nov 29
-->

<?php
	session_start();

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	//get user type and id
	$user_type = $_SESSION["user_type"];
	$id = $_SESSION["user_id"];
	$user_type_id = lcfirst($user_type) . '_id';
	$user_menu = $user_type . "_menu.php";

	//get data posted from Student or professor view_vacant_classroom.html
	$week = $_POST["week"];
	$day = $_POST["day"];
	$course_begin = $_POST["course_begin"];
	$course_end = $_POST["course_end"];

	//ERROR if course_begin > course_end
	if($course_end < $course_begin)
	{
		$url = 'User_view_vacant_classroom.php';
		print<<<EOT
			<script>
				alert('Course End must be greater than Course Begin');
				location.href = 'User_view_vacant_classroom.php';
			</script>
EOT;
	}

	//get data from database
	$day_column = 'Sparetime.' . $day;
	$query = "SELECT Classroom.classroom_id, Classroom.size, Classroom.facility, Sparetime.week, $day_column FROM Classroom, Sparetime 
	    WHERE Classroom.classroom_id = Sparetime.classroom_id AND Sparetime.week = '$week'";
	$result = $conn->query($query);
	if(!$result)
	{
		die('Connect Error');
	}

	//print results
	print<<<EOT
	<head>
		<title>View Vacant Classroom</title>
		<link rel="stylesheet" type="text/css" href="view_schedule.css">
	<head>

	<body>
		<div id='div1'>
			<h1>Vacant Classroom</h1>
			<table>
				<tr>
					<td align="center">Classroom</td>
					<td align="center">Size</td>
					<td align="center">Facility State</td>
				</tr>
EOT;
	for ($i = 0 ; $i < $result->num_rows ; $i++)
	{
		$result->data_seek($i);
		$row = $result->fetch_assoc();
		$vacant_number = $row[$day];
		
		//handle the schedule
		$vacant = decbin($vacant_number);
		while(strlen($vacant) < 15)
		{
			$vacant = '0' . $vacant;
		}

		$time_string = substr($vacant, $course_begin - 1, $course_end - $course_begin + 1);
		if(bindec($time_string) != 0)
		{
			continue;
		}

		$classroom_id = $row['classroom_id'];
		$size = $row['size'];
		$facility = $row['facility'];
		if($facility == 1)
			$state = 'GOOD';
		else
			$state = 'BAD';

		//print a row
		print<<<EOT
			<tr>
				<td align="center">$classroom_id</td>
				<td align="center">$size</td>
				<td align="center">$state</td>
			</tr>
EOT;
	}
	print<<<EOT
			</table>
			<br>
			<a href = "User_view_vacant_classroom.php"><input type = "button" value = "Go Back"></a>
		</div>
	</body>
EOT;

	$conn->close();
?>
