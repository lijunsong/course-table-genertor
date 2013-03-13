<?php
$title="上传联系人信息";
include_once('header.php');
require_once('conn.php');
require_once('excel_reader_and_writer.php');
require_once('util.php');

if (!isset($_POST['file_upload']) && !isset($_POST['update_contact'])){
    //如果没有上传过东西，也没有需要更新联系人，那么显示上传按钮
?>
<form action="upload.php" method="post" enctype="multipart/form-data" class=".form-horizontal">
    <fieldset>
    <legend>上传联系人信息</legend>
    <lable for="file" >上传文件</label>
    <input type="file" name="file" id="file" />
    <button class="btn btn-primary" type="submit" name="file_upload">Upload</button>
    </fieldset>
</form>

<?php    
} else if (isset($_POST['file_upload'])){
    //如果上传了文件
    if ($_FILES["file"]["error"] > 0){
        echo "上传发生错误: " . $_FILES["file"]["error"] . "br />";
    } else {
        move_uploaded_file($_FILES["file"]["tmp_name"],
                           "/tmp/test.xsl");
        echo "Stored in: " . $_FILES["file"]["tmp_name"];
        echo "<br />type: " . $_FILES["file"]["type"];
        echo excel_html5_format("/tmp/test.xsl");
?>        
        <div class="form-actions">
        <form class="form-inline" method="post" name="update_contact" action="upload.php">
            <button type="submit" class="btn btn-danger" name="update_contact">UPDATE ALL</button>
        </form> 
        </div>        
<?php
    }
} else if (isset($_POST['update_contact'])){
    if (insertupdate_with_excel("/tmp/test.xsl")){
        //插入成功
        echo wrap_text('sucessfully update and insert!', 'alert alert-info');
    } else {
        //插入失败
        echo wrap_text('Failed!' . mysql_error(), 'alert alert-error');
    }
}
?>
<? include('footer.php'); /*end*/?>