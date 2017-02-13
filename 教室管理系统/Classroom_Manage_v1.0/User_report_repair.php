<!--
	User_report_repair.php
	Function: For different users to report repair
	Author: hyq, gyc
	Last Update: 2016 Nov 29
-->

<!doctype html>
<html>
	<head>
		<meta charset="UTF-8">
		<link rel="stylesheet" type="text/css" href="home.css">
<?php
	session_start();  //for the _SESSION, something like cookie

	$user_type = $_SESSION["user_type"];
	$id = $_SESSION["user_id"];
	if($user_type == "External" or $user_type == 'Manager')
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
		<title>$user_type Report Repair</title>
	</head>
	<body>
		<div id='div1'>
		<h1 align = "center">Report Repair</h1>
			<form action="report_repair.php" method="post">
				<table>
					<tr>
						<td>Classroom:</td>
						<td align="left"><input type = "text" name = "classroom" id = "classroom" size = "5" /></td>
					</tr>

					</tr>
						<td>Statement:</td>
						<td><input type = "text" name = "statement" id = "statement" size = "20" /></td>
						
					</tr>

					<tr>
						<td><input type = "submit" value = "Submit"></td>
						<td>
							<a href=$user_menu><input type = "button" value = "Go Back"></a>
						</td>
					</tr>
				</table>
			</form>
		</div>
	</body>
EOT;
?>		
	
</html>