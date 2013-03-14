<?php
$title="北外国商通讯录首页";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

?>
<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">    
<table class="table table-bordered">
<?php 
$fields = get_fields_array();
$contacts = get_contacts_array();
echo array_to_thead($fields, $add_id=true, $add_op=true);
echo array_to_tbody($contacts, $add_id=true, $add_op=true);
?>    
</table>
</div>
<? include('footer.php'); /*end*/?>