<?php

$title="北外国商通讯录首页";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');


$extra_info = NULL;

if (isset($_GET['delete']) && isset($_GET['name'])){
    $id = $_GET['delete'];
    $name = $_GET['name'];
    if (trim($id) == "" || trim($name) == ""){
        $extra_info = get_alert_error("删除联系人 $name 时产生错误");
    } else {
        $result = mysql_query("delete from contacts where studentid='$id'");
        if ($result){
            $extra_info = get_alert_info("删除联系人 $name");
        } else {
            $extra_info = get_alert_error("删除联系人 $name 时产生错误");            
        }
    }
}

?>
<div class="span2">
<?php echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">    
<table class="table table-bordered">
<?php
    if ($extra_info != NULL){
        echo $extra_info;
    }
$fields = get_fields_array();
$contacts = get_contacts_array();
echo array_to_thead($fields, $add_id=true, $add_op=true);
echo array_to_tbody($contacts, $add_id=true, $add_op=true);
?>    
</table>
</div>
<?php include('footer.php'); /*end*/?>