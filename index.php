<html><head></head><body>
<a href="index.php?a=infos">Infos</a><a href=""></a><hr/>
<?php
	if(isset($_GET['a'])) {
		$a = $_GET['a'];
	}else{
		$a = '';
	}
	
	if($a == 'infos') {
		$d = opendir("info/");
		while($f = readdir($d)) {
			if(!is_dir("info/".$f)) {
				echo $f .'<br/>';
			}
		}
	}
?>
