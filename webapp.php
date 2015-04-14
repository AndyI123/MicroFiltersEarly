<html>
<head>
    <title>MicroFilters App</title>
<script type="text/javascript">
    function validateForm()
    {
    var x=document.forms["myForm"]["filePath"].value;
    $.ajax({
        url: x
        success: function(data){
            alert('exists');
        },
        error: function(data){
            alert('does not exist');
        },
    }
})
</script>
</head>
<body>
<style type="text/css">
label {
    display: inline-block;
    cursor: pointer;
    position: relative;
    padding-left: 25px;
    margin-right: 15px;
    font-size: 18px;
    font-family: HelveticaNeue-UltraLight, Arial, Helvetica;
}



.wrapper {
    width: 500px;
    margin: 50px auto;
}
input[type=radio],
input[type=checkbox] {
    display: none;
    margin: 20%;
}
label:before {
    content: "";
    display: inline-block;

    width: 16px;
    height: 16px;

    margin-right: 10px;
    position: absolute;
    left: 0;
    bottom: 1px;
    background-color: #aaa;
    box-shadow: inset 0px 2px 3px 0px rgba(0, 0, 0, .3), 0px 1px 0px 0px rgba(255, 255, 255, .8);
}

.radio label:before {
    border-radius: 8px;
}
.checkbox label {
    margin-bottom: 10px;
}
.checkbox label:before {
    border-radius: 3px;
}

input[type=radio]:checked + label:before {
    content: "\2022";
    color: #f3f3f3;
    font-size: 30px;
    text-align: center;
    line-height: 18px;
}

.checkbox{
    margin-left: 20%;
}

input[type=checkbox]:checked + label:before {
    content: "\2713";
    text-shadow: 1px 1px 1px rgba(0, 0, 0, .2);
    font-size: 15px;
    color: #f3f3f3;
    text-align: center;
    line-height: 15px;
    float: left;
}

 #bigDiv{
    text-align: center;
    border-radius: 3px;
    width: 100%;
    background-color: #FFF;
 }

#title{
    font-family: HelveticaNeue-UltraLight, HelveticaNeue, Helvetica, Arial, sans-serif;
    font-size: 36pt;
}
 body{
    background-color: #55ACEE;
 }

 input[type=text] label:before{
    content: "";
    display: inline-block;

    width: 16px;
    height: 16px;

    margin-right: 10px;
    position: absolute;
    left: 0;
    bottom: 1px;
    box-shadow: none;
}

#sub, #train{
    background-color: #55ACEE;
    border-radius: 5px;
    border: none;
    font-size: 25px;
    color: #FFF;
    font-family: HelveticaNeue-UltraLight, Roboto, Helvetica, Arial;
    padding: 10px 10px 10px 10px;
    margin: 10px 10px;
}

#sub:hover{
    background-color: #72A1EE;
}

input[type=text]{
    background-color: #BBB;
    border-radius: 5px;
    border: none;
    font-size: 25px;
    color: #FFF;
    font-family: HelveticaNeue-UltraLight, Roboto, Helvetica, Arial;
    padding: 10px 10px 10px 10px;
    margin: 10px 10px;
}

input[type=text]:focus{
    background-color: #DDD;
    border-radius: 5px;
    border: none;
    font-size: 25px;
    color: #000;
    font-family: HelveticaNeue-UltraLight, Roboto, Helvetica, Arial;
    padding: 10px 10px 10px 10px;
    margin: 10px 10px;
}

</style>
<div id="bigDiv">
<div id="title">MicroFilters</div>
<div style="text-align: left; width:100%">
<p style="font-family: Helvetica-Light, Helvetica, Arial, sans-serif; font-size: 18pt; margin-left: 2em;" ><strong>Choose your options:</strong></p>
<div class="checkbox">
<form action="backend.php" method="post"  enctype="multipart/form-data" onsubmit="return validateForm()">
    <input id="check1" type="checkbox" name="1" value="check1">
    <label for="check1">Remove Retweets</label>
    <br>
    <input id="check2" type="checkbox" name="2" value="check2">
    <label for="check2">Remove Duplicates</label><br />
    <input id="check3" type="checkbox" name="3" value="check2">
    <label for="check3">Remove Non-English Tweets</label><br />
    <font face="HelveticaNeue-UltraLight" size="+2">Include:</font><br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="check6" type="checkbox" name="6" value="check2"> <label for="check6">Small Images</label> <input id="check7" type="checkbox" name="7" value="check2"> <label for="check7">Medium Images</label> <input id="check8" type="checkbox" name="8" value="check2"> <label for="check8">Large Images</label>
    <input id="check4" type="checkbox" name="4" value="check2">
    <label for="check4">Include Videos</label><br />
    <input id="check5" type="checkbox" name="5" value="check2">
    <label for="check5">Sort Chronologically</label><br />
    <p style="font-family: HelveticaNeue-UltraLight, HelveticaNeue-Light, Helvetica, Arial, Sans-Serif">Upload Input file (Filled CSV):<input type="file" name="filePath"/></p>
    <input type="text" name="emailTXT" placeholder="Email">
    <div style="margin-left: 15em; width:100%;"><input id="sub" type="submit" name="Submit"></div>

    </form>
</div>
</div>
</body>
</html
