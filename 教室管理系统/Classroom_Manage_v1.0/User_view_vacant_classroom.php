<!--
	User_view_vacant_classroom.php
	Function: post data with specific week, day, course begin and end, for Student and Professor.
	Author: gyc
	Last Update: 2016 Nov 29
-->

<!doctype html>
<html>
	<head>
		<meta charset="UTF-8">
		<link rel="stylesheet" type="text/css" href="view_vacant.css">

<?php
	session_start();  //for the _SESSION, something like cookie

	$user_type = $_SESSION["user_type"];
	$id = $_SESSION["user_id"];

	//For Student and Professor
	if($user_type == "Manager")
	{
		print<<<EOT
			<script>
				alert('User type error')
				location.href='home.html';
			</script>
EOT;
	}
	$user_menu = $user_type . "_menu.php";

	print<<<EOT
		<title>$user_type View Vacant Classroom</title>
	</head>
	<body>
		<div id='div1'>
			<h1>
				View Vacant Classroom
			</h1>
			<form action="view_vacant_classroom.php" method="post">
				<table>
					<tr>
						<td colspan="2">Week:</td>
						<td>
							<select name = "week">
								<option value = "1">1</option>
								<option value = "2">2</option>
								<option value = "3">3</option>
								<option value = "4">4</option>
								<option value = "5">5</option>
								<option value = "6">6</option>
								<option value = "7">7</option>
								<option value = "8">8</option>
								<option value = "9">9</option>
								<option value = "10">10</option>
								<option value = "11">11</option>
								<option value = "12">12</option>
								<option value = "13">13</option>
								<option value = "14">14</option>
								<option value = "15">15</option>
								<option value = "16">16</option>
								<option value = "17">17</option>
								<option value = "18">18</option>
								<option value = "19">19</option>
								<option value = "20">20</option>
							</select>
						</td>
					</tr>

					<tr>
						<td colspan="2">Day:</td>
						<td>
							<select name = "day">
								<option value = "mon">MON</option>
								<option value = "tue">TUE</option>
								<option value = "wed">WED</option>
								<option value = "thu">THU</option>
								<option value = "fri">FRI</option>
								<option value = "sat">SAT</option>
								<option value = "sun">SUN</option>
							</select>
						</td>
					</tr>

					<tr>
						<td colspan="2">Course Begin:</td>
						<td>
							<select name = "course_begin">
								<option value = "1">1</option>
								<option value = "2">2</option>
								<option value = "3">3</option>
								<option value = "4">4</option>
								<option value = "5">5</option>
								<option value = "6">6</option>
								<option value = "7">7</option>
								<option value = "8">8</option>
								<option value = "9">9</option>
								<option value = "10">10</option>
								<option value = "11">11</option>
								<option value = "12">12</option>
								<option value = "13">13</option>
								<option value = "14">14</option>
								<option value = "15">15</option>
							</select>
						</td>
					</tr>

					<tr>
						<td colspan="2">Course End:</td>
						<td>
							<select name = "course_end">
								<option value = "1">1</option>
								<option value = "2">2</option>
								<option value = "3">3</option>
								<option value = "4">4</option>
								<option value = "5">5</option>
								<option value = "6">6</option>
								<option value = "7">7</option>
								<option value = "8">8</option>
								<option value = "9">9</option>
								<option value = "10">10</option>
								<option value = "11">11</option>
								<option value = "12">12</option>
								<option value = "13">13</option>
								<option value = "14">14</option>
								<option value = "15">15</option>
							</select>
						</td>
					</tr>

					<tr>
						<td><input type = "submit" value = "Submit"></td>
						<td><a href = $user_menu><input type = "button" value = "Go Back"></a></td>
					</tr>
				</table>
			</form>
		</div>
	</body>
EOT;
?>
		
</html>