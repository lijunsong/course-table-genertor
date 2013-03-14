<?php 

ob_start(); // to avoid 'Warning: Cannot modify header information - headers already sent by ...'

$title="下载联系人信息";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');




?>
<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">
    <form class="form" method="get" action="download.php">
      <fieldset>
        <legend><?echo $title?></legend>
        <div class="alert alert-info">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          您可以将通讯录导出成为 csv 格式并下载。
        </div>  
        <button type="submit" class="btn btn-primary" name="download" value="export_db">下载</button>
      </fieldset>
    </form>
</div>
<? include('footer.php'); /*end*/?>
