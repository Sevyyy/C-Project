<!--
	check_repair.php
	Function: check repair and modify database
	Author: hyq
	Last Update: 2016 Nov 29
-->

<?php
	session_start();

	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	$report_id = $_POST['report_id'];
	$classroom_id = $_POST['classroom_id'];
	$reason = $_POST['reason'];

	$query = "UPDATE Classroom SET facility = '0' WHERE classroom_id = '$classroom_id'";
	$query1 = "UPDATE Report SET vertify = '-1' WHERE report_id = '$report_id'";

	echo"$query<br>";
	if($conn->query($query) && $conn->query($query1))
	{
		print<<<EOT
			<script>
				alert('This report was checked successfully!');
				location.href = 'Manager_view_repair.php';
			</script>
EOT;
	}
	else
	{
		print<<<EOT
			<script>
				alert('Checking failed!');	
			</script>
EOT;
	}
	$conn->close();
?>
