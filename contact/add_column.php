<html>
<head>
  <title>北外商学院通讯录管理员登录</title>
  <link rel="stylesheet" type="text/css" href="main.css">
  <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
  <meta http-equiv="Content-Language" content="zh-cn" />
</head>
     <body>
<?php
include('conn.php');
mysql_query("set names gbk");

if ($result = mysql_query('select * from contacts')){
    while ($row = mysql_fetch_row($result)){
        print_r($row);
    }
}

if ($result = mysql_query('select * from fields')){
    while ($row = mysql_fetch_row($result)){
        print_r($row);
    }
}

?>
看编码
     </body>
</html>

