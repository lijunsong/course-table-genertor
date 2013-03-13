<?php
$title="北外国商通讯录首页";
include_once('header.php');
require_once('conn.php');

?>
<table class="table table-hover">
<?php 
fields_to_thead();
contacts_to_tbody();
?>    
</table>    
<? include('footer.php'); /*end*/?>