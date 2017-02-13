<!--
	User_change_password.php
	Function: For different users to input old and new password
	Author: gyc
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
	if($user_type == "External")
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
		<title>$user_type Change Password</title>
	</head>
	<body>
		<div id='div1'>
			<h1>Change Password</h1>
			<form action="change_password.php" method="post">
				<table>
					<tr>
						<td>Old Password:</td>
						<td><input type = "password" name = "old_password" size = "20"/></td>
					</tr>
					
					<tr>
						<td>New Password:</td>
						<td><input type = "password" name = "new_password" size = "20"/></td>
					</tr>

					<tr>
						<td>Password Verification:</td>
						<td><input type = "password" name = "ver_password" size = "20"/></td>
					</tr>

					<tr>
						<td align = 'right'><input type = "submit" value = "Submit"></td>
						<td><a href = $user_menu><input type = "button" value = "Go Back"></a></td>
					</tr>
				</table>
			</form>
		</div>
	</body>
EOT;
?>		
	
</html>