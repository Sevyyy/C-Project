<!--
	report_repair.php
	Function: get report data from last page and modify database
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

	$classroom_id = $_POST["classroom"];
	$statement = $_POST["statement"];

	$query1 = "SELECT * FROM Classroom WHERE classroom_id = '$classroom_id'";
	$result1 = $conn->query($query1);

	$query2 = "SELECT * FROM Report WHERE classroom_id = '$classroom_id' AND vertify = '0'";
	$result2 = $conn->query($query2);

	$user_type = $_SESSION['user_type'];
	$user_menu = $user_type . '_menu.php';
	$user_report_repair = $user_type . '_report_repair.html';
	$user_report_repair = 'User_report_repair.php';
	if($result1->num_rows == 0)
	{
		print<<<EOT
			<script>
				alert('This classroom does not exist!');
				location.href = '$user_report_repair';
			</script>
EOT;
	}
	else if($result2->num_rows != 0)
	{
		print<<<EOT
			<script>
				alert('This classroom have been report!');
				location.href = '$user_report_repair';
			</script>
EOT;
	}
	else
	{
		$query3 = "INSERT INTO Report(statement, vertify, classroom_id) VALUES('$statement', '0', '$classroom_id')";
		if($conn->query($query3))
		{
			print<<<EOT
				<script>
					alert('Your report was successfully submitted!');
					location.href = '$user_menu';
				</script>
EOT;
		} 
		else
		{
			print<<<EOT
				<script>
					alert('Your report was failed!');
					location.href = '$user_report_repair';
				</script>
EOT;
		}
	}
	$conn->close();
?>
