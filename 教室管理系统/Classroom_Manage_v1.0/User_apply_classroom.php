<!--
	User_apply_classroom.html
	Function: post data to apply_classroom.php Add a button "Add" for user to make more applications.
	Author: gyc, wq
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
		<title>$user_type Apply Classroom</title>
	</head>
	<body>
		<div id='div1'>
		<h1 align="center">Apply Classroom</h1>
			<form action="apply_classroom.php" method="post" id="form">
				<table id = "table">
					<tr>
						<td colspan = 5>Reason:<input type = "text" name = "reason" size = "80"></td>
					</tr>

					<tr>
						<td>Week:
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

						<td>Day:
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

						<td>Course Begin:
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

						<td>Course End:
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

						<td>Size:
							<select name = "size">
								<option value = "big">BIG: 200</option>
								<option value = "medium big">MEDIUM BIG: 150</option>
								<option value = "medium small">MEDIUM SMALL: 100</option>
								<option value = "small">SMALL: 50</option>
							</select>
						</td>
					</tr>
					</table>
					<br>
					<input type = "hidden" name = "num_rows" value = "1" id = "num_rows">
					<input type = 'button' value = 'Add' onclick = "addrow()">
					<script language="JavaScript" type="text/JavaScript">
					var num_rows = 1;
					var weekArray = new Array();
					var dayArray = new Array();
					var course_beginArray = new Array();
					var course_endArray = new Array();
					var sizeArray = new Array();

				    function addrow()
				    {
				    	num_rows = num_rows + 1;
				    	var tr = document.createElement('tr');

				    	var tdweek = document.createElement('td');
				    	tdweek.innerText = 'Week: ';
						weekArray[num_rows] = document.createElement('select');
						weekArray[num_rows].name = "week".concat(num_rows.toString());
						weekArray[num_rows].options.add(new Option("1","1"));
						weekArray[num_rows].options.add(new Option("2","2"));
						weekArray[num_rows].options.add(new Option("3","3"));
						weekArray[num_rows].options.add(new Option("4","4"));
						weekArray[num_rows].options.add(new Option("5","5"));
						weekArray[num_rows].options.add(new Option("6","6"));
						weekArray[num_rows].options.add(new Option("7","7"));
						weekArray[num_rows].options.add(new Option("8","8"));
						weekArray[num_rows].options.add(new Option("9","9"));
						weekArray[num_rows].options.add(new Option("10","10"));
						weekArray[num_rows].options.add(new Option("11","11"));
						weekArray[num_rows].options.add(new Option("12","12"));
						weekArray[num_rows].options.add(new Option("13","13"));
						weekArray[num_rows].options.add(new Option("14","14"));
						weekArray[num_rows].options.add(new Option("15","15"));
						weekArray[num_rows].options.add(new Option("16","16"));
						weekArray[num_rows].options.add(new Option("17","17"));
						weekArray[num_rows].options.add(new Option("18","18"));
						weekArray[num_rows].options.add(new Option("19","19"));
						weekArray[num_rows].options.add(new Option("20","20"));
						tdweek.appendChild(weekArray[num_rows]);
						tr.appendChild(tdweek);

						var tdday = document.createElement('td');
						tdday.innerText = 'Day: ';
						dayArray[num_rows] = document.createElement('select');
						dayArray[num_rows].name = "day".concat(num_rows.toString());
						dayArray[num_rows].options.add(new Option("MON","mon"));
						dayArray[num_rows].options.add(new Option("TUE","tue"));
						dayArray[num_rows].options.add(new Option("WED","wed"));
						dayArray[num_rows].options.add(new Option("THU","thu"));
						dayArray[num_rows].options.add(new Option("FRI","fri"));
						dayArray[num_rows].options.add(new Option("SAT","sat"));
						dayArray[num_rows].options.add(new Option("SUN","sun"));
						tdday.appendChild(dayArray[num_rows]);
						tr.appendChild(tdday);

						var tdcourse_begin = document.createElement('td');
						tdcourse_begin.innerText = 'Course Begin: ';
						course_beginArray[num_rows] = document.createElement('select');
						course_beginArray[num_rows].name = "course_begin".concat(num_rows.toString());
						course_beginArray[num_rows].options.add(new Option("1","1"));
						course_beginArray[num_rows].options.add(new Option("2","2"));
						course_beginArray[num_rows].options.add(new Option("3","3"));
						course_beginArray[num_rows].options.add(new Option("4","4"));
						course_beginArray[num_rows].options.add(new Option("5","5"));
						course_beginArray[num_rows].options.add(new Option("6","6"));
						course_beginArray[num_rows].options.add(new Option("7","7"));
						course_beginArray[num_rows].options.add(new Option("8","8"));
						course_beginArray[num_rows].options.add(new Option("9","9"));
						course_beginArray[num_rows].options.add(new Option("10","10"));
						course_beginArray[num_rows].options.add(new Option("11","11"));
						course_beginArray[num_rows].options.add(new Option("12","12"));
						course_beginArray[num_rows].options.add(new Option("13","13"));
						course_beginArray[num_rows].options.add(new Option("14","14"));
						course_beginArray[num_rows].options.add(new Option("15","15"));
						tdcourse_begin.appendChild(course_beginArray[num_rows]);
						tr.appendChild(tdcourse_begin);

						var tdcourse_end = document.createElement('td');
						tdcourse_end.innerText = 'Course End: ';
						course_endArray[num_rows] = document.createElement('select');
						course_endArray[num_rows].name = "course_end".concat(num_rows.toString());
						course_endArray[num_rows].options.add(new Option("1","1"));
						course_endArray[num_rows].options.add(new Option("2","2"));
						course_endArray[num_rows].options.add(new Option("3","3"));
						course_endArray[num_rows].options.add(new Option("4","4"));
						course_endArray[num_rows].options.add(new Option("5","5"));
						course_endArray[num_rows].options.add(new Option("6","6"));
						course_endArray[num_rows].options.add(new Option("7","7"));
						course_endArray[num_rows].options.add(new Option("8","8"));
						course_endArray[num_rows].options.add(new Option("9","9"));
						course_endArray[num_rows].options.add(new Option("10","10"));
						course_endArray[num_rows].options.add(new Option("11","11"));
						course_endArray[num_rows].options.add(new Option("12","12"));
						course_endArray[num_rows].options.add(new Option("13","13"));
						course_endArray[num_rows].options.add(new Option("14","14"));
						course_endArray[num_rows].options.add(new Option("15","15"));
						tdcourse_end.appendChild(course_endArray[num_rows]);
						tr.appendChild(tdcourse_end);

						var tdsize = document.createElement('td');
						tdsize.innerText = 'Size: ';
						sizeArray[num_rows] = document.createElement('select');
						sizeArray[num_rows].name = "size".concat(num_rows.toString());
						sizeArray[num_rows].options.add(new Option("BIG: 200","big"));
						sizeArray[num_rows].options.add(new Option("MEDIUM BIG: 150","medium big"));
						sizeArray[num_rows].options.add(new Option("MEDIUM SMALL: 100","medium small"));
						sizeArray[num_rows].options.add(new Option("SMALL: 50","small"));
						tdsize.appendChild(sizeArray[num_rows]);
						tr.appendChild(tdsize);

						var table = document.getElementById('table');
						table.appendChild(tr);
						var rows = document.getElementById('num_rows');
						rows.value = num_rows.toString();					
				    }

				    </script>

				    <input type = "submit" value = "Submit">
					<a href = $user_menu><input type = "button" value = "Go Back"></a>
				
			</form>
		</div>
	</body>
EOT;
?>
		
</html>