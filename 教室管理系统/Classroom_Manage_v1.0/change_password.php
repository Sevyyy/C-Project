<!--
	change_password.php
	Function: Change password, for Student, Professor and Manager
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

	//get data from session
	$user_type = $_SESSION["user_type"];
	$id = $_SESSION["user_id"];
	$user_type_id = lcfirst($user_type) . '_id';

	//get data from database
	$query = "SELECT * FROM $user_type WHERE $user_type_id = '$id'";
	$result = $conn->query($query);

	$result->data_seek(0);
	$row = $result->fetch_assoc();

	$password = $row['password'];

	//get old, new, ver_password from pages
	$old_password = $_POST["old_password"];
	$new_password = $_POST["new_password"];
	$ver_password = $_POST["ver_password"];

	//reject changing password if old_password were not correct

	if($old_password != $password)
	{
		$url = 'User_change_password.php';
		print<<<EOT
		<script>
			alert('Wrong Password');
			location.href = '$url';	
		</script>
EOT;
	}

	//reject changing password if ver_password were not new_password
	else if($new_password != $ver_password)
	{
		$url = 'User_change_password.php';
		print<<<EOT
		<script>
			alert('Password Verification Error');
			location.href = '$url';	
		</script>
EOT;
	}

	//else password can be changed	
	else
	{
		$query = "UPDATE $user_type SET password = '$new_password' WHERE $user_type_id = '$id'";
		$conn->query($query);
		if($conn->connect_error)
		{
			die('Could not connect: ' . $conn->connect_error);
		}

		$url = $user_type . '_menu.php';
		print<<<EOT
		<script>
			alert('Password Sucessfully Changed');
			location.href = '$url';	
		</script>
EOT;
	}
	
	//close database
	$conn->close();
?>
