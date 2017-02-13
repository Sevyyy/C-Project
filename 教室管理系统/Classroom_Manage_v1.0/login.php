<!--
	login.php
	Function: For all kinds of users to login the system
	Author: wq
	Last Update: 2016 Nov 30
-->

<?php
	session_start();  //for the _SESSION, something like cookie

	//connect to the database
	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	//get the var from home.html
	$account = $_POST["account"];
	$password = $_POST["password"];
	$user_type = $_POST["user_type"];

	$user_type_id = lcfirst($user_type) . '_id';
	$query = "SELECT * FROM $user_type WHERE $user_type_id = '$account' AND password = '$password'";
	$result = $conn->query($query);
	if($result->num_rows == 0)
	{
		print<<<EOT
			<script>
				alert('Password Error');
				location.href='home.html';
			</script>
EOT;
	}
	$_SESSION["user_id"] = $account;
	$_SESSION["user_type"] = $user_type;
	$url = $user_type . '_menu.php';
	print<<<EOT
		<script>
			location.href='$url';
		</script>
EOT;

	$conn->close();
?>