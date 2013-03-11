<?php

$sql = "select * from contact";
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
