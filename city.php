<?php
/**
by xiaoshangmin
**/
$url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/';
$s = file_get_contents($url);
$start = strpos($s, '<tr class=\'provincetr\'>');
$end = strpos($s, '</table>');
$m = $end - $start;
$ss = substr($s, $start, $m);
$ss = iconv('GBK', 'UTF-8', $ss);
preg_match_all('/<a href=\'(.*?)\'>([^<]+)/', $ss, $match);
foreach ($match[1] as $k => $v) {
    echo $v . '--' . $match[2][$k] . '<br/>';//省
    $num = substr($v, 0, 2);
    $city = file_get_contents($url . $v);
    $start = strpos($city, '<tr class=\'cityhead\'>');
    $end = strpos($city, '</table>');
    $m = $end - $start;
    $ss = substr($city, $start, $m);
    $ss = iconv('GBK', 'UTF-8', $ss);
    preg_match_all('/(\d+)<\/a><\/td><td><a href=\'(.*?)\'>([^<]+)/', $ss, $matchCity);
    foreach ($matchCity[1] as $k => $v) {
        echo $v . '--' . $matchCity[3][$k] . '--' . $matchCity[2][$k] . '<br/>';//市
        $county = file_get_contents($url . $matchCity[2][$k]);
        $start = strpos($county, '<table class=\'countytable\'>');
        $end = strpos($county, '</table>');
        $m = $end - $start;
        $ss = substr($county, $start, $m);
        $ss = iconv('GBK', 'UTF-8', $ss);
        preg_match_all('/(\d+)<\/a><\/td><td><a href=\'(.*?)\'>([^<]+)/', $ss, $matchCounty);
        foreach ($matchCounty[1] as $k => $v) {
            echo $v . '--' . $matchCounty[3][$k] . '--' . $matchCounty[2][$k] . '<br/>';//区
            $town = file_get_contents($url . $num . '/' . $matchCounty[2][$k]);
            $start = strpos($town, '<table class=\'towntable\'>');
            $end = strpos($town, '</table>');
            $m = $end - $start;
            $ss = substr($town, $start, $m);
            $ss = iconv('GBK', 'UTF-8', $ss);
            preg_match_all('/(\d+)<\/a><\/td><td><a href=\'(.*?)\'>([^<]+)/', $ss, $matchTown);
            foreach ($matchTown[1] as $k => $v) {
                echo $v . '--' . $matchTown[3][$k] . '--' . $matchTown[2][$k] . '<br/>';//办事处
                $y = explode('/', $matchTown[2][$k])[0];
                $villa = file_get_contents($url . $num . '/' . $y . '/' . $matchTown[2][$k]);
                $start = strpos($villa, '<table class=\'villagehead\'>');
                $end = strpos($villa, '</table>');
                $m = $end - $start;
                $ss = substr($villa, $start, $m);
                $ss = iconv('GBK', 'UTF-8', $ss);
                preg_match_all('/<td>(\d+)<\/td><td>(\d+)<\/td><td>([^<]+)<\/td>/', $ss, $matchVilla);
                foreach ($matchVilla[1] as $k => $v) {
                    echo $v .  '--'.$matchVilla[3][$k] . '<br/>';//居委会
                }
                ob_flush();
                flush();
            }

        }
    }
}
