<?php

//为区分编码
if (stripos($_SERVER['HTTP_USER_AGENT'],"Mac")){
    $OS = 'mac';
} else if (stripos($_SERVER['HTTP_USER_AGENT'],"Linux")){
    $OS = 'linux';
} else {
    $OS = 'windows';
}

function correct_encoding_when_reading($str)
{
    global $OS;
    
    if ($OS == 'windows')
        return iconv('gb2312', 'utf-8', $str);
    else
        return $str;
}

function correct_encoding_when_writing($str)
{
    global $OS;
    
    if ($OS == 'windows')
        return iconv('utf-8', 'gb2312', $str);
    else
        return $str;
}

function array_walk_deep(&$items,$func){
    //print_r($items);
    foreach ($items as &$item) {
        if(is_array($item))
          array_walk_deep($item,$func);
        else
          $item = $func($item);
    }
}

function correct_array_reading($arr)
{
    array_walk_deep($arr, 'correct_encoding_when_reading');
    return $arr;
    
}

function correct_array_writing($arr)
{
    array_walk_deep($arr, 'correct_encoding_when_writing');
    return $arr;
    
    /* if (gettype($arr) != "array"){ */
    /*     return correct_encoding_when_writing($arr); */
    /* } else { */
    /*     $res = array(); */
    /*     for($i = 0; $i<count($arr); $i++){ */
    /*         $res[$i] = correct_array_writing($arr[$i]); */
    /*     } */
    /*     return $res; */
        
    /* } */
    
}


function control_group($input_id, $label_text, $placeholder, $value=NULL)
{
    $groups = '<div class="control-group"><label class="control-label" for="' . $input_id . '">' . $label_text . '</label><div class="controls">';
    if ($value == NULL){
        $groups .=  "<input type=\"text\" name=\"$input_id\" id=\"$input_id\" placeholder=\"$placeholder\"></div></div>";
    } else {
        $groups .=  "<input type=\"text\" name=\"$input_id\" id=\"$input_id\" placeholder=\"$placeholder\" value=\"$value\"></div></div>";
    }
    return $groups;
}

function startsWith($haystack, $needle)
{
    return strpos($haystack, $needle) === 0;
}
function endsWith($haystack, $needle)
{
    return substr($haystack, -strlen($needle)) == $needle;
}

function wrap_text($text, $class="alert")
{
	return "<div class=\"$class\">$text</div>";
}

function get_alert($title, $text, $extra_class="")
{
    return wrap_text('<button type="button" class="close" data-dismiss="alert">&times;</button>
            <h4>' . $title . '</h4>' . "$text", "alert " . $extra_class);
}

function get_alert_info($text)
{
    return get_alert("完成！", $text, "alert-info");
}

function get_alert_error($text)
{
    return get_alert("出错啦！", $text, "alert-error");
}

function get_danger_button($text)
{
    return "<button class=\"btn btn-danger\">$text</button>";
}

function get_navs($current_nav, $navs, $extra_nav_tag = "")
{
    $res = "<ul class=\"nav $extra_nav_tag\">";
    foreach ($navs as $name => $link){
        if (basename($link, ".php") == $current_nav)
            $res = $res . "<li class=\"active\">";
        else
            $res = $res . "<li>";
        $res = $res . "<a href=\"$link\">$name</a></li>";
    }
    $res = $res . "</ul>";
    return $res;
}

function array_to_tr($inarray, $td_tag="td", $tr_style="")
{
    $res = '<tr '.$tr_style.'>';
    for($i = 0; $i < count($inarray); $i += 1){
        $res .= "<$td_tag>".$inarray[$i]."</$td_tag>";
    }
    $res .= '</tr>';
    return $res;   
}

function array_to_thead($inarray, $add_id=false, $add_op=false)
{
    if (count($inarray) == 0)
        return "";
    $id = array();
    $op = array();
    if ($add_id == true){
        $id = array('specialkey_23x' => '序号');
    }
    if ($add_op == true){
        $op = array('specialkey_24z' => '操作');
    }
    $ths = array_values($id+ $inarray + $op);

    return '<thead>'.array_to_tr($ths, $td_tag="th").'</thead>';
}

function array_to_tbody($inarrays, $add_id=false, $add_op=false)
{
    if (count($inarrays) == 0)
        return "";

    $id = array();
    $op = array();

    $res = '<tbody>';
    for($i = 0; $i < count($inarrays); $i += 1){
        if ($add_id == true){
            $id = array('specialkey_23x' => $i+1);
        }
        if ($add_op == true){
            $op = array('specialkey_24z' => '<a
            href="' . "?delete=" . $inarrays[$i][0] . '&name=' . $inarrays[$i][1] . '">' . get_danger_button('<i class="icon-remove icon-white"> </i>') . '</a>');
        }
        $new_line = array_values($id+$inarrays[$i]+$op);
        $res .= array_to_tr($new_line);
    }
    $res .= '</tbody>';
    return $res;
}

/* 在数据库中查找学号为 id 的记录 */
function get_contact_by_id($id, $contact_array)
{
    foreach($contact_array as $num => $contact_info){
        if ($id == $contact_info[0]){
            return $contact_info;
        }
    }
    return NULL;
}

function check_line($line)
{
    if (trim($line[0]) == "" || trim($line[1] == "") || trim($line[2] == "")){
        return array(false, "必填项为空");
    }
    if (!preg_match("/^\d+$/", $line[0])){
        return array(false, get_alert_error("第 1 列必须全为数字：当前为 “$line[0]”"));
    }
    if (!preg_match("/^(男|女)$/", $line[2])){
        return array(false, get_alert_error("第 3 列必须为'男'或者'女'：当前为 “$line[2]”"));
    }
    if ($line[5] != "" && !preg_match("/(\d|-)*/", $line[4])){
        return array(false, get_alert_error("第 5 列必须为横线与数字的组合：当前为 “$line[4]”"));
    }
        /*if ($line[6] != "" && !filter_var($line[6], FILTER_VALIDATE_EMAIL)){
            return array(false, get_alert_error("Csv 第 $line_num 行第 6 列必须为合法的邮箱地址：当前为 “$line[6]”"));
            }*/
    return array(true, "");
}

?>