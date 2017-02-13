<!--
	Professor_view_schedule.php
	Function: view schedule
	Author: hyq
	Last Update: 2016 Nov 29
-->

<html>
	<head>
		<title>Professor View Schedule</title>
		<link rel="stylesheet" type="text/css" href="view_schedule.css">
	</head>

	<body>
		<div id='div1'>
			<h1>Schedule</h1>

<?php
	session_start();

	$conn = new mysqli("localhost", "root", "", "Classroom_Manage");
	if($conn->connect_error)
	{
		die('Could not connect: '. $conn->connect_erro);
	}

	$id = $_SESSION['user_id'];
	$query1 = "SELECT * FROM Course WHERE professor_id = '$id'";
	$result = $conn->query($query1);

	if($result->num_rows == 0)
	{
		echo"No Result!";
	}	
	else
	{
		echo "<table>
			<tr align='center'>
				<td> Course ID </td>
				<td> Course Name </td>
				<td> Classroom </td>
				<td> week time </td>
				<td> week </td>
				<td> class time </td> 
			</tr>";

		while($row = $result->fetch_row())
		{
			echo "<tr>
					<td> $row[0] </td>
					<td> $row[1] </td>
					<td>" . $row[3] . "</td>
					<td>" . $row[4] . "-" . $row[5] ."</td>";

			switch($row[6])
			{
				case '1': echo"<td> Mon </td>";break;
				case '2': echo"<td> Tue </td>";break;
				case '3': echo"<td> Wed </td>";break;
				case '4': echo"<td> Thu </td>";break;
				case '5': echo"<td> Fri </td>";break;
				case '6': echo"<td> Sat </td>";break;
				case '7': echo"<td> Sun </td>";break;
			}
			echo "<td>" . $row[7] . "-" . $row[8] . "</td>"; 
			echo "</tr>";
		}
		echo"</table>";
	}
	$conn->close();
?>
		<br>
		<a href="Professor_menu.php"><input type='button' value="Go Back"></a>
		</div>
	</body>
</html>
