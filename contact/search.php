<?php
$title="搜索联系人";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

$extra_info = NULL;

if (isset($_POST['search'])){
    
}

?>
<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">
<?
if ($extra_info != NULL){
    echo $extra_info;
}
?>

<form class="form-horizontal" method="post" name="search">
    <fieldset>
    <legend>搜索联系人信息</legend>
    <!--<div class="alert alert-block">
      <h4>注意！</h4>
      <ul>
    <li>
      </ul>
    </div>-->
    
<?php
    $fields = get_fields_array();
    foreach ($fields as $f=>$field_name){
        echo control_group("$f",  $field_name, "");
    }
?>
<div class="control-group">
    <div class="controls">
    <button type="submit" class="btn btn-primary" name="search" value="1">搜索</button>
    </div>
</div>
        </fieldset>
</form>
</div>
<? include('footer.php'); /*end*/?>