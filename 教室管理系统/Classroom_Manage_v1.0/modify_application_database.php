<!--
	modufy_application_database.php
	Function: After getting available classrooms, manager can agree or disagree this application, and corresponding modifications were done in this .php, for Manager
	Author: gyc, wq
	Last Update: 2016 Nov 30(Add email system by wq)
-->

<?php
	session_start();

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	//get data posted from get_available_classroom.php
	$vertify = $_POST['vertify'];
	$application_id = $_POST['application_id'];

	//find the type of applyer
	$query = "SELECT user_type FROM Application WHERE Application.application_id = '$application_id'";
	$result = $conn->query($query);
	$result->data_seek(0);
	$row = $result->fetch_assoc();
	$user_type = $row['user_type'];

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

	$email_attr = $user_type . '.email';
	$user_type_id = $user_type . '.' . lcfirst($user_type) . '_id';

	//get email of applyer
	$query = "SELECT $email_attr
				FROM Application, $user_type 
				WHERE Application.application_id = '$application_id' AND  Application.user_id = $user_type_id";
	$result = $conn->query($query);
	
	$result->data_seek(0);
	$row = $result->fetch_assoc();
		
	if($row['email'])
	{
		$email = $row['email'];
	}
	else
	{
		$email = "???";
	}

	//pass the application
	if($vertify == 1)
	{
		//update values in Application set vertify = 1 
		$classroom_id = $_POST['classroom_id'];
		$query = "UPDATE Application SET vertify = '1', classroom_id = '$classroom_id' WHERE application_id = '$application_id'";
		$result = $conn->query($query);
		if(!$result)
		{
			die('result error');
		}

		$week = $_POST["week"];
		$day = $_POST["day"];
		$course_begin = $_POST["course_begin"];
		$course_end = $_POST["course_end"];

		//get the time schedule of selected classroom, week and day
		$query = "SELECT $day FROM Sparetime WHERE classroom_id = '$classroom_id' AND week = '$week'";
		$result = $conn->query($query);
		if(!$result)
		{
			die('result error');
		}

		$result->data_seek(0);
		$row = $result->fetch_assoc();
		
		$vacant_number = $row[$day];
		
		$vacant = decbin($vacant_number);
		while(strlen($vacant) < 15)
		{
			$vacant = '0' . $vacant;
		}


		$course_length = $course_end - $course_begin + 1;
		$ones = '';
		for($i = 0 ; $i < $course_length ; $i++)
		{
			$ones = $ones . '1';
		}

		//replace its bits occupied by this application and put new value into database
		$vacant = substr_replace($vacant, $ones, $course_begin - 1, $course_length);
		$vacant_number = bindec($vacant);

		$query = "UPDATE Sparetime SET $day = '$vacant_number' WHERE classroom_id = '$classroom_id' AND week = '$week'";
		$result = $conn->query($query);
		if(!$result)
		{
			die('result error');
		}

		if($email == "???")
		{
			print<<<EOT
			<html>
				<head>
					<title>Modifying</title>
				<head>
				<body bgcolor="pink">
					<div style="margin-top:100px;" align = "center">
					<p>Application was accepted, but no Email was sent.</p>
					<a href="Manager_handle_application.php"><input type="button" value="Go Back"></a>
					</div>
				</body>
			</html>
EOT;
		}
		else
		{
			$message = "Your application with the ID N0." . $application_id . " was accepted with Classroom : " . $classroom_id;

			// In case any of our lines are larger than 70 characters, we should use wordwrap()
			$message = wordwrap($message, 150, "\r\n");

			// Send
			mail($email, 'Application Reply', $message);

			print<<<EOT
				<html>
					<head>
						<title>Modifying</title>
					<head>
					<body bgcolor="pink">
						<div style="margin-top:100px;" align = "center">
							<p>Application was accepted AND This message has been tent to $email</p>
							<p>(Message : $message)</p>
							<a href="Manager_handle_application.php"><input type="button" value="Go Back"></a>
						</div>
					</body>
				</html>
EOT;
		}
	}
	//reject the application
	else
	{
		//set vertify = -1, and no other information was changed
		$query = "UPDATE Application SET vertify = '-1' WHERE application_id = '$application_id'";
		$result = $conn->query($query);
		if(!$result)
		{
			die('result error');
		}
		
		if($email == "???")
		{
			print<<<EOT
			<html>
				<head>
					<title>Modifying</title>
				<head>
				<body bgcolor="pink">
					<div style="margin-top:100px;" align = "center">
						<p>Application was rejected, but no Email was sent</p>
						<a href="Manager_handle_application.php"><input type="button" value="Go Back"></a>
					</div>
				</body>
			</html>
EOT;
		}
		else
		{
			$message = "Your application with the ID N0." . $application_id ."Rejected!";

			// In case any of our lines are larger than 70 characters, we should use wordwrap()
			$message = wordwrap($message, 120, "\r\n");

			// Send
			mail($email, 'Application Reply', $message);

			print<<<EOT
			<html>
				<head>
					<title>Modifying</title>
				<head>
				<body bgcolor="pink">
					<div style="margin-top:100px;" align = "center">
						<p>Application was rejected AND This message has been sent to $email</p>
						<p>(Message : $message)</p>
						<a href="Manager_handle_application.php"><input type="button" value="Go Back"></a>
					</div>
				</body>
			</html>
EOT;
		}
	}

	$conn->close();
?>