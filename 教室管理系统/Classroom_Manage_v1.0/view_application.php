<!--
	view_application.php
	Function: get aplications from database for Student and Professor.
	Author: gyc
	Last Update: 2016 Nov 24
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
	$user_type_abbr = $user_type_id[0];
	$user_menu = $user_type . '_menu.php';

	//get data from database
	$query = "SELECT * FROM Application WHERE user_type = '$user_type_abbr' AND user_id = '$id'";
	$result = $conn->query($query);
	if(!$result)
	{
		die('Connect Error');
	}

	//print results
	print<<<EOT
	<head>
		<title>$user_type View Applications</title>
		<link rel="stylesheet" type="text/css" href="view_schedule.css">
	</head>

	<body>
		<div id='div1'>
			<h1>Your Applications</h1>
			<table>
				<tr>
					<td align="center">Application ID</td>
					<td align="center">Size</td>
					<td align="center">Week</td>
					<td align="center">Day</td>
					<td align="center">Course Begin</td>
					<td align="center">Course End</td>
					<td align="center">Reason</td>
					<td align="center">Vertify</td>
					<td align="center">Classroom</td>
				</tr>
EOT;
	for ($i = 0 ; $i < $result->num_rows ; $i++)
	{
		$result->data_seek($i);
		$row = $result->fetch_assoc();

		$application_id = $row['application_id'];
		$size = $row['size'];
		$week = $row['week'];
		$day = $row['day'];
		$course_begin = $row['course_begin'];
		$course_end = $row['course_end'];
		$reason = $row['reason'];
		$vertify = $row['vertify'];
		$classroom_id = $row['classroom_id'];

		switch ($vertify) 
		{
			case '1':
				$vertify_string = 'PASSED';
				break;

			case '0':
				$vertify_string = 'NOT HANDLED';
				break;

			case '-1':
				$vertify_string = 'REJECTED';
				break;
			
			default:
				break;
		}

		$day = strtoupper($day);

		//print a line 
		print<<<EOT
			<tr>
				<td align="center">$application_id</td>
				<td align="center">$size</td>
				<td align="center">$week</td>
				<td align="center">$day</td>
				<td align="center">$course_begin</td>
				<td align="center">$course_end</td>
				<td align="center">$reason</td>
				<td align="center">$vertify_string</td>
				<td align="center">$classroom_id</td>
			</tr>
EOT;
	}
	print<<<EOT
			</table>
			<br>
			<a href = $user_menu><input type = "button" value = "Go Back"></a>
		</div>
	</body>
EOT;

	
	$conn->close();
?>
