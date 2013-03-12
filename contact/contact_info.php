<html>
<head>
  <title>个人信息</title>
  <link rel="stylesheet" type="text/css" href="main.css">
  <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
  <meta http-equiv="Content-Language" content="zh-cn" />
</head>
     <body>
<?php
include('conn.php');
if (isset($_GET['action'])){
    if ($_GET['action'] == 'add'){
        $action = '添加';
    } else if ($_GET['action'] == 'update'){
        $action = '更新';
    } else {
        die('非法操作');
    }
} else {
    die('非法操作');
}
     
if ($fields = mysql_query('select * from fields')){
?>
  <form name="ContactForm" method="post" action="modify_contact.php" onSubmit="return InputCheck(this)">
<?php
    while ($field_row = mysql_fetch_row($fields)){
        $field = $field_row[1];
        $field_name = $field_row[2];
?>
    <p><label for="<? echo $field;?>" class="label"><? echo $field_name;?></label> <br />
      <input id="<? echo $field;?>" name="<? echo $field?>" type="text" class="input" />
    </p>
<?php 
    } /*end of while */?>

      <input type="submit" name="<?echo $_GET['action']?>" value="<? echo $action;?>" class="left" />
  </form>
<?
} /*end of if*/ ?>
     </body>
</html>
