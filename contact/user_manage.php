<?php
$title="用户管理";
include_once('header.php');
require_once('conn.php');
require_once('util.php');

?>

<div class="span2">
</div>
<div class="span8">
    <form class="form" method="get" action="download.php">
      <fieldset>
        <legend><?echo $title?></legend>
<?php
    //列出所有用户
    

?>    
      </fieldset>
    </form>
</div>
<div class="span2">
</div>

<?php include('footer.php'); /*end*/?>