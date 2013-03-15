<?php

require_once('util.php');


$sidebar = array('批量上传' => '/contact/upload.php',
                 '导出下载' => '/contact/export.php',
                 '全部更替' => '/contact/overwrite.php',
                 '添加' => '/contact/add_contact.php',
                 '搜索' => '/contact/search.php');
function get_basename($file)
{
    return basename($file, '.php');
}

$index_subentries = array_map("get_basename", array_values($sidebar));

function get_sidebar($current_file, $sidebar)
{
    return '<div class="well sidebar-nav">' . get_navs($current_file, $sidebar, "nav nav-list") . '</div>';
}


?>