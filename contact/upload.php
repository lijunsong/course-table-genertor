<?php
$title="上传联系人信息";
include_once('header.php');
require_once('conn.php');
require_once('excel_reader_and_writer.php');

if (!isset($_POST['file_upload'])){
    //如果没有上传过东西，显示上传按钮
?>
<form action="upload.php" method="post" enctype="multipart/form-data" class=".form-horizontal">
    <fieldset>
    <legend>上传联系人信息</legend>
    <lable for="file" >上传文件</label>
    <input type="file" name="file" id="file" />
    <button type="submit" name="file_upload">Upload</button>
    </fieldset>
</form>

<?php    
} else {
    //如果上传了文件
    if ($_FILES["file"]["error"] > 0){
        echo "上传发生错误: " . $_FILES["file"]["error"] . "br />";
    } else {
        move_uploaded_file($_FILES["file"]["tmp_name"],
                           "/tmp/test.xsl");
        echo "Stored in: " . $_FILES["file"]["tmp_name"];
        echo "<br />type: " . $_FILES["file"]["type"];
        $excel_data = get_data_from_excel("/tmp/test.xsl");
    }
}

?>
<? include('footer.php'); /*end*/?>