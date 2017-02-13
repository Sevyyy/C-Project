<!--
	Manager_view_repair.php
	Function: get repair report from database and show them on the page
	Author: hyq, gyc
	Last Update: 2016 Nov 29
-->

<html>
	<head>
		<title>Manager Handle Repair Reports</title>
		<link rel="stylesheet" type="text/css" href="view_schedule.css">
	</head>

	<body>
		<div id='div1'>
			<h1 align="center">Handle Repair</h1>
<?php
	session_start();

	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: ' . $conn->connect_error);
	}

	$id = $_SESSION["user_id"];
	$query1 = "SELECT * FROM Report WHERE vertify = '0' or vertify = '-1'";
	$result = $conn->query($query1);

	if($result->num_rows == 0)
	{
		print<<<EOT
			There is not any repair reports to handle.<br>
EOT;
	}
	else
	{
		print<<<EOT
			<table>
				<tr align='center'>
					<td> Report ID </td>
					<td> Classroom </td>
					<td> Statement </td>
					<td> Vertify </td>
					<td> Check </td>
					<td> Handle </td>
				</tr>
EOT;
		while($row = $result->fetch_row())
		{
			print<<<EOT
				<tr align='center'>
					<td> $row[0] </td>
					<td> $row[3] </td>
					<td> $row[1] </td>
EOT;
			switch($row[2])
			{
				case '0': $vertify = 'Not checked';break;
				case '-1': $vertify = 'Checked but Not handled'; break;
			}

			print<<<EOT
					<td> $vertify </td>
					<td>
						<form action = 'check_repair.php' method='post'>
							<input type='hidden' name='report_id' value='$row[0]' >
							<input type='hidden' name='classroom_id' value='$row[3]'>
							<input type='hidden' name='reason' value='$row[1]'>
							<input type='submit' value='Check'>
						</form>
		     		</td>

				    <td>
						<form action = 'handle_repair.php' method='post'>
							<input type='hidden' name='report_id' value='$row[0]'>
							<input type='hidden' name='classroom_id' value='$row[3]'>
							<input type='hidden' name='reason' value='$row[1]'>
							<input type='submit' value='Handle'>
						</form>
				     </td>
				</tr>
EOT;
		}
		print<<<EOT
			</table>
EOT;
	}
	print<<<EOT
		<br>
		<a href = "Manager_menu.php"><input type="button" value="Go Back"></a>
EOT;
	$conn->close();
?>
		</div>
	</body>
</html>