<html>
<head>

<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.min.js"></script>




  <style type="text/css">
  #bigDiv{
    background-color: #FFF;
    border-radius: 3px;
    width: 100%;
    height: 500px;
    overflow: hidden;
    text-align: center;

  }
  body
  {
    background-color: #55ACEE;
  }
  a{
    text-decoration: none;
    color: #000;
    text-align: center;
  }
  p
  {
        margin-left: 20%;
    margin-right: 20%;
  }
  </style>
</head>
<body>
<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);



if ($_FILES['filePath']['size'] > 22*1024*1024) {
  print "<script type=\"text/javascript\">";
  print "alert('File Too Large. Must be under 22 MB')";
  print "</script>";
  die("");
}
if ($_FILES['filePath']['type'] != 'text/csv' && $_FILES['filePath']['type'] != 'application/vnd.ms-excel') {
  print "<script type=\"text/javascript\">";
  print "alert('File is not a CSV. Please read the usage instructions at microfilter.cs.uwaterloo.ca')";
  print "</script>";
  die("");
}


if ( $_SERVER['REQUEST_METHOD'] == 'POST' && empty($_POST) &&
     empty($_FILES) && $_SERVER['CONTENT_LENGTH'] > 0 )
{
  $displayMaxSize = ini_get('post_max_size');

  switch ( substr($displayMaxSize,-1) )
  {
    case 'G':
      $displayMaxSize = $displayMaxSize * 1024;
    case 'M':
      $displayMaxSize = $displayMaxSize * 1024;
    case 'K':
       $displayMaxSize = $displayMaxSize * 1024;
  }

  $error = 'Posted data is too large. '.
           $_SERVER[CONTENT_LENGTH].
           ' bytes exceeds the maximum size of '.
           $displayMaxSize.' bytes.';
  die($error);
}


$uniqueString = uniqid();
$string = "";
for ($x=1; $x<=5; $x++)
{
  if(isset($_POST[strval($x)]))
  {
    $string .= "y";
  }
  else
  {
    $string .= "n";
  }
}

$sizes = "";
if (isset($_POST["6"])) {
  $sizes .= "S";
}
if (isset($_POST["7"])) {
  $sizes .= "M";
}
if (isset($_POST["8"])) {
  $sizes .= "L";
}

$myFile = "/var/www/MF/testtoinst.sh";
$fh = fopen($myFile, 'w');
fwrite($fh, "curl localhost:6800/schedule.json -d project=default -d spider=MicroFiltersApp -d setting=IMAGES_STORE="."'../TARS/".$uniqueString."/' -d FP='../files/hi.csv' -d FP2='../files/hi.txt' -d ID=".$uniqueString." -d SIZES='".$sizes."'");
$strlen = strlen($string);
$varNames = $arrayName = array("RT", "D", "ENG","VID", "SORT");
for($i = 0; $i <= $strlen - 1; $i++)
{
    $char = substr($string, $i, 1);
    fwrite($fh, " -d ".$varNames[$i]."=");
    fwrite($fh, $char);
    // $char contains the current character, so do your processing here
}
fclose($fh);

if( $_FILES['filePath']['name'] != "" )
{
    copy( $_FILES['filePath']['tmp_name'], "files/hi.csv" ) or
           die( "Could not copy file!");
}
else
{
    die("No file specified!");
}


$fh2 = fopen("files/hi.txt", "w+");
fclose($fh2);
$jobid = "";
$stringT = exec("sh testtoinst.sh");
$arrayT = explode(" ", $stringT);
for ($i=0; $i < count($arrayT); $i++)
{
  if ($arrayT[$i] == '"jobid":')
  {
    $jobid = $arrayT[$i+1];
    break;

  }
}
$emailString = $_POST["emailTXT"];

$execVar = exec("python fileSaver.py "."'".$jobid."' "."'".$uniqueString."' "."'".$emailString."' "." > /dev/null 2>/dev/null &");
// $phar = new PharData('TARS/'.$uniqueString.'.tar');
// // add all files in the project
// $phar->buildFromDirectory('TARS/'.$uniqueString);
?>

<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
<div id="bigDiv">
<p>
<font size="+3">Your file is being processed and will be available soon (within the next few minutes or hours) at http://microfilter.cs.uwaterloo.ca/MF/TARS/. The download code you will enter is <?php echo $uniqueString ?>. An email will be sent to <?php echo $emailString ?> at the exact time when the file is ready, with a copy of these instructions</font></p>
</div>


</body>
</html>
