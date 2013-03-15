<?php
$title="增添修改通讯录项目";
include_once('header.php');
require_once('conn.php');
require_once('util.php');

print_r($_POST);

if (isset($_POST['update'])){
    update_fields($_POST);
} else if (isset($_POST['add'])){
    add_fields($_POST);
}



$fields = get_fields_array();
?>
<form class="form-horizontal" method="post" name="UpdateField" action="field_manage.php">
    
<?php
$item = 1;
foreach ($fields as $f=>$field_name){
    echo control_group($f, "Item $item", $field_name);
    $item += 1;
}
//echo control_group("field_new", "New Item", "type in here");
?>
<div class="control-group">
    <div class="controls">
    <button type="submit" class="btn btn-primary" name="update">更新</button>
    </div>
</div>    
</form>

<form class="form-horizontal" method="post" name="AddField" action="field_manage.php">
<?php
    echo control_group("field_$item", "New Item", "New Item");
?>
<div class="control-grpu">
    <div class="controls">
    <button type="submit" class="btn" name="add">Add</button>
    </div>
<div>    
</form>    
<? include('footer.php'); /*end*/?>