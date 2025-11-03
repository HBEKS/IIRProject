<?php
echo '<h1>PENCARIAN DATA ARTIKEL ILMIAH</h1>';
echo '<form action="result.php" method="POST">';
echo '<label for="penulis">Input Nama Penulis : </label>';
echo '<input type="text" name="namaPenulis"><br><br>';
echo '<label for="penulis">Input Keyword Artikel : </label>';
echo '<input type="text" name="keywordArtikel"><br><br>';
echo '<label for="penulis">Jumlah Data : </label>';
echo '<input type="text" name="jumlahData"><br><br>';
echo '<input type="submit" name="crawl" value="Search">';
echo '</form>';
?>