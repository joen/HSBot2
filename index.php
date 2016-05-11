<?php


if($_SERVER['REMOTE_USER'] == 'gastwlan'){
	$zeichen = "abcedfghijklmnopqrstuvwxyz0123456789";
	$pw = "";

	@mt_srand ((double) microtime() * 1000000);
	for ($i = 0; $i < 12; $i++ ) {
		$r = mt_rand(0,strlen($zeichen)-1);
		$pw .= $zeichen{$r};
	}
	
	$h = fopen('info/GastWLAN.txt',w);
	flock($h,2);
	fputs($h,$pw);
	flock($h,3);
	fclose($h);
	echo $pw;
	
	
}else{
	error_reporting(E_ALL); 
	ini_set('error_reporting', E_ALL);
	echo '<html><head></head><body>
		<a href="index.php?a=infos">Infos</a><a href=""></a><hr/>';

	if(isset($_GET['a'])) {
		$a = $_GET['a'];
	}else{
		$a = '';
	}
	
	if($a == 'infos') {
		if(isset($_GET['s'])) {
			if($_GET['s'] == 'del') {
				$f = str_replace('/','_',$_GET['f']);
				unlink('info/'.$f.'.txt');
				unset($_GET['f']);
			}
			
			if($_GET['s'] == 'act') {
				$f = str_replace('/','_',$_GET['f']);
				if(substr($f,0,1) == '.') {
					rename('info/'.$f.'.txt','info/'.substr($f,1) .'.txt');
				}else{
					rename('info/'.$f.'.txt','info/.'. $f .'.txt');
				}
				unset($_GET['f']);
			}
		}
		
		if(isset($_GET['f'])) {
			$f = str_replace('/','_',$_GET['f']);
			if(isset($_POST['submit'])) {
				$h = fopen('info/'.$f.'.txt','w');
				$content = str_replace("\r",'',$_POST['content']);
				flock($h,2);
				fputs($h, $content);
				flock($h,3);
				fclose($h);
			}else{
				$content = file('info/'.$f.'.txt');
				echo '<h2>'.$f.'</h2><form action="index.php?a=infos&f='. $f .'" method="post">
					<textarea name="content" cols="30" rows="10">'. implode('',$content) .'</textarea><br/>
					<input type="submit" name="submit" value="Editieren" />
				</form>';
			}
		}else{
			$d = opendir("info/");
			while($f = readdir($d)) {
				if(!is_dir("info/".$f)) {
					$f = substr($f,0,-4);
					echo '<a href="index.php?a=infos&f='. $f .'">'.$f.'</a> [<a href="index.php?a=infos&f='. $f .'&s=del">L&ouml;schen</a> <a href="index.php?a=infos&f='. $f .'&s=act">(De)Aktivieren</a>]<br/>';
				}
			}
			echo '<form action="index.php" method="get">
				<input type="hidden" name="a" value="infos" />
				<input type="text" name="f" /> <input type="submit" value="Anlegen" />
			</form';
		}
	}
}
?>
