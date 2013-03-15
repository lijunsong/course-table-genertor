<?php
$title="添加联系人";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

$extra_info = NULL;

?>
<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">    
<form class="form-horizontal" name="contact_info">
<?php
    if ($extra_info != NULL){
        echo $extra_info;
    }
if (isset($_GET['action']) && $_GET['action'] == 'add_contact'){
    $fields = get_fields_array();
    foreach ($fields as $f=>$field_name){
        $field_info = "";
        if ($f == 'studentid' || $f == 'gender' || $f == 'name'){
            $field_info = '必填';
        }
        echo control_group("$f",  $field_name, "$field_info");
}
    
}

?>
<div class="control-group">
    <div class="controls">
    <button type="submit" class="btn btn-primary" name="add_contact" value="1">添加</button>
    </div>
</div>    
</form>
    
</div>
<? include('footer.php'); /*end*/?>