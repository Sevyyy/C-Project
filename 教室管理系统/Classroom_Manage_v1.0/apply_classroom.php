<!--
	apply_classroom.php
	Function: get data from last page and insert an application into database, for Student and Professor. Add a button "Add" for user to make more applications.
	Author: gyc, wq
	Last Update: 2016 Nov 27
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

	//get data posted from Student or Professor_apply_classroom.html	
	$reason = $_POST["reason"];
	$num_rows = $_POST["num_rows"];
	
	for($i = 0 ; $i < $num_rows ; $i ++)
	{
		if($i == 0)
		{
			$week = $_POST["week"];
			$day = $_POST["day"];
			$course_begin = $_POST["course_begin"];
			$course_end = $_POST["course_end"];
			$size = $_POST["size"];
		}
		else
		{
			$week = $_POST["week" . strval($i + 1)];
			$day = $_POST["day". strval($i + 1)];
			$course_begin = $_POST["course_begin". strval($i + 1)];
			$course_end = $_POST["course_end". strval($i + 1)];
			$size = $_POST["size". strval($i + 1)];
		}

		//Reject if course_end < course_begin
		if($course_end < $course_begin)
		{
			print<<<EOT
				<script>
					alert('Course End must be greater than Course Begin');
					location.href = 'User_apply_classroom.php';	
				</script>
EOT;
		}
		else
		{
			//insert an application into database 
			$query = "INSERT INTO Application (user_type, user_id, size, week, day, course_begin, course_end, reason) VALUES ('$user_type_abbr', '$id', '$size', '$week', '$day', '$course_begin', '$course_end', '$reason')";
			$result = $conn->query($query);
			if(!$result)
			{
				die('Connect Error');
			}

			//response
			$user_menu = $user_type . '_menu.php';
			print<<<EOT
				<script>
					alert('Your application was submitted sucessfully.');
					location.href = '$user_menu';	
				</script>
EOT;
		}
	}
	$conn->close();
?>
