<!--
	get_available_classroom.php
	Function: Get all available classrooms for an application, for Manager
	Author: gyc, wq
	Last Updare: 2016 Nov 30
-->

<?php
	session_start();

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	//get data posted from get_unhandled_application.php
	$application_id = $_POST["application_id"];
	$demand_size = $_POST["size"];
	$week = $_POST["week"];
	$day = $_POST["day"];
	$course_begin = $_POST["course_begin"];
	$course_end = $_POST["course_end"];

	//get available classrooms and show them on page
	$day_column = 'Sparetime.' . $day;
	$query = "SELECT Classroom.classroom_id, Classroom.size, Classroom.facility, Sparetime.week, $day_column FROM Classroom, Sparetime WHERE Classroom.classroom_id = Sparetime.classroom_id AND Sparetime.week = $week";
	$result = $conn->query($query);
	if(!$result)
	{
		die('Connect Error');
	}

	//I set the Reject button here, and it will jump to modify_application_database.php to update some values in our database if user click it
	print<<<EOT
	<head>
		<title>Application Handling</title>
		<link rel="stylesheet" type="text/css" href="view_schedule.css">
	</head>

	<body>
	<div id='div1'>
		<form action="modify_application_database.php" method="post">
			<input type="hidden" name="vertify" value="-1">
			<input type="hidden" name="application_id" value="$application_id">
			<input type="submit" value="Reject This Application">
		</form>

		<p>Available Classroom(s)</p>
		<table>
			<tr>
				<td align="center">Classroom</td>
				<td align="center">Facility State</td>
				<td align="center">Handle</td>
			</tr>
EOT;
	
	for ($i = 0 ; $i < $result->num_rows ; $i++)
	{
		$result->data_seek($i);
		$row = $result->fetch_assoc();

		$vacant_number = $row[$day];
		
		//get schedule for selected week and day
		$vacant = decbin($vacant_number);
		while(strlen($vacant) < 15)
		{
			$vacant = '0' . $vacant;
		}

		$time_string = substr($vacant, $course_begin - 1, $course_end - $course_begin + 1);
		if(bindec($time_string) != 0) //continue if it were not vacant
		{
			continue;
		}
		
		$c_size = $row['size'];
		switch ($demand_size) 
		{
			case 'big':
				$demand_size = 4;
				break;

			case 'medium big':
				$demand_size = 3;
				break;

			case 'medium small':
				$demand_size = 2;
				break;

			case 'small':
				$demand_size = 1;
				break;
			
			default:
				break;
		}

		switch ($c_size) 
		{
			case 'big':
				$c_size = 4;
				break;

			case 'medium big':
				$c_size = 3;
				break;

			case 'medium small':
				$c_size = 2;
				break;

			case 'small':
				$c_size = 1;
				break;
			
			default:
				break;
		}
		if($c_size < $demand_size) //continue if the demand size was smaller than classroom size
		{
			continue;
		}

		$classroom_id = $row['classroom_id'];
		$facility = $row['facility'];
		if($facility == 1)
			$state = 'GOOD';
		else
			$state = 'BAD';

		//print each available classroom
		print<<<EOT
			<tr>
				<td align="center">$classroom_id</td>
				<td align="center">$state</td>
				<td>
					<form action="modify_application_database.php" method="post">
						<input type="hidden" name="vertify" value="1">
						<input type="hidden" name="application_id" value="$application_id">
						<input type="hidden" name="classroom_id" value="$classroom_id">
						<input type="hidden" name="week" value="$week">
						<input type="hidden" name="day" value="$day">
						<input type="hidden" name="course_begin" value="$course_begin">
						<input type="hidden" name="course_end" value="$course_end">
						<input type="submit" value="Apply This Classroom">
					</form>
				</td>
			</tr>
EOT;
	}
	print<<<EOT
		</table>
		<a href="Manager_handle_application.php"><input type="button" value="Go Back"></a>	
	</div>
	</body>
EOT;
	
	$conn->close();
?>
