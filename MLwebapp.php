<?php

function chmod_R($path, $filemode, $dirmode) {
    if (is_dir($path) ) {
        if (!chmod($path, $dirmode)) {
            $dirmode_str=decoct($dirmode);
            print "Failed applying filemode '$dirmode_str' on directory '$path'\n";
            print "  `-> the directory '$path' will be skipped from recursive chmod\n";
            return;
        }
        $dh = opendir($path);
        while (($file = readdir($dh)) !== false) {
            if($file != '.' && $file != '..') {  // skip self and parent pointing directories
                $fullpath = $path.'/'.$file;
                chmod_R($fullpath, $filemode,$dirmode);
            }
        }
        closedir($dh);
    } else {
        if (is_link($path)) {
            print "link '$path' is skipped\n";
            return;
        }
        if (!chmod($path, $filemode)) {
            $filemode_str=decoct($filemode);
            print "Failed applying filemode '$filemode_str' on file '$path'\n";
            return;
        }
    }
}

if($_FILES["zip_file"]["name"]) {
    $filename = $_FILES["zip_file"]["name"];
    $source = $_FILES["zip_file"]["tmp_name"];
    echo $filename;
    $type = $_FILES["zip_file"]["type"];

    $name = explode(".", $filename);
    $accepted_types = array('application/zip', 'application/x-zip-compressed', 'multipart/x-zip', 'application/x-compressed');
    foreach($accepted_types as $mime_type) {
        if($mime_type == $type) {
            $okay = true;
            break;
        }
    }

    $continue = strtolower($name[1]) == 'zip' ? true : false;
    if(!$continue) {
        $message = "The file you are trying to upload is not a .zip file. Please try again.";
    }

    $target_path = "zips/".$filename;  // change this to the correct site path
    if(move_uploaded_file($source, $target_path)) {
        $zip = new ZipArchive();
        $x = $zip->open($target_path);
        if ($x === true) {
            $zip->extractTo("zips/"); // change this to the correct site path
            $zip->close();
            unlink($target_path);
        }
        $message = "Your .zip file was uploaded and unpacked.";
    } else {
        $message = "There was a problem with the upload. Please try again.";
    }
    chmod_R('zips/'.substr($filename, 0, -4), 0777, 0777);
    exec("python zips/ImageClassifier.py zips/".substr($filename, 0, -4)." zips/".uniqid()." ".$_POST["email"]);
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Machine Learning</title>

</head>

<body>

<style type="text/css">
label {
    display: inline-block;
    cursor: pointer;
    position: relative;
    padding-left: 25px;
    margin-right: 15px;
    font-size: 25px;
    text-align: center;
    font-family: HelveticaNeue-UltraLight, Arial, Helvetica;
}
input[type=submit]{
    background-color: #55ACEE;
    border-radius: 5px;
    border: none;
    font-size: 25px;
    color: #FFF;
    font-family: HelveticaNeue-UltraLight, Roboto, Helvetica, Arial;
    padding: 10px 10px 10px 10px;
    margin: 10px 10px;
}

body{
    background-color: #55ACEE;
 }

  #bigDiv{
    text-align: center;
    border-radius: 3px;
    width: 100%;
    background-color: #FFF;
 }
</style>
<?php if($message) echo "<p>$message</p>"; ?>
<div id="bigDiv">
<form enctype="multipart/form-data" method="post" action="">
<label>Choose a zip file to upload: <input type="file" name="zip_file" /></label>
<label>Enter your email: <input type="text" placeholder="Email" name="email"></label>
<br />
<input type="submit" name="submit" value="Upload" />
</form>
<div style="margin-right: 30%; margin-left: 30%;">
<p id="info" style="width:100%; text-align: left; margin-right: 30%; font-family: HeleveticaNeue-Light, Roboto, sans-serif;">Remember, the file being uploaded should be a .zip file, with three folders inside: a Yes folder, containing a certain amount of positive training data images, a No folder containing negative training samples <strong>(we reccommend approximately 150-200 training samples total to ensure the right balance of accuracy and training expense)</strong>, and a Test folder, containing the unlabeled images. This process will return a text file containing your labeled data. <strong>You will recieve an email with a link to your file. This will be given in pairs of lines: the first line will be a local URL to the image, with the second line being a 0 or a 1, depending on whether the image shows damage.</strong></p>
</div>
</div>
</body>
</html>
