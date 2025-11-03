<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <?php
    // Periksa apakah halaman ini diakses dari formulir (via method POST)
    if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['crawl'])) {

        // 1. Ambil data dari formulir (index.php)
        // htmlspecialchars() adalah untuk keamanan, mencegah XSS
        $namaPenulis = htmlspecialchars($_POST['namaPenulis']);
        $keywordArtikel = htmlspecialchars($_POST['keywordArtikel']);
        $jumlahData = (int)$_POST['jumlahData']; // Ubah ke angka

        // --- Mulai Output Sesuai Gambar Anda ---
        // 2. Tampilkan link "< Back to Home"
        echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";

        // 3. Tampilkan data yang diinput
        echo '<div class="info-pencarian">';
        echo "<p>Nama Penulis : <span>{$namaPenulis}</span></p>";
        echo "<p>Keyword Artikel : <span>{$keywordArtikel}</span></p>";
        echo "<p>Jumlah data = <span>{$jumlahData}</span></p>";
        echo '</div>';

        // 4. Tampilkan judul "Hasil Pencarian"
        echo "<h2>Hasil Pencarian</h2>";

        // ... (Di sinilah kode cURL untuk SerpApi dan
        // ...  pembuatan tabel akan diletakkan,
        // ...  seperti pada jawaban saya sebelumnya) ...

    } else {
        // Jika ada yang membuka result.php secara langsung
        echo "<p>Silakan lakukan pencarian dari <a href='index.php'>halaman utama</a>.</p>";
    }
    ?>
</body>

</html>