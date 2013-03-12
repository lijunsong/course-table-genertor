<html>
<head>
  <title>个人信息</title>
  <link rel="stylesheet" type="text/css" href="main.css">
  <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
  <meta http-equiv="Content-Language" content="zh-cn" />
</head>
     <body>

<?php
require('conn.php');
?>

<table>
<tr>
<td>name</td>
<td>sex</td>
<td>birthday</td>
<td>qq</td>
<td>mobile</td>
<td>email</td>
<td>address</td>
</tr>
<?php
while($row = MySQL_fetch_row($result)){
    if ($row[2] == 0){
        $sex = 'Boy';
    } else { $sex = 'Girl'; }
?>
    <tr>
    <td><?php echo $row[1]; ?></td>
    <td><?php echo $sex; ?></td>
    <td><?php echo $row[3]; ?></td>
    <td><?php echo $row[4]; ?></td>
    <td><?php echo $row[5]; ?></td>
    <td><?php echo $row[6]; ?></td>
    <td><?php echo $row[7]; ?></td>
    </tr>
<?php
}
?>
</table>

</body>
</html>