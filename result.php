<?php

set_time_limit(600); // 10 menit
ini_set('max_execution_time', 600);
ini_set('max_input_time', 600);
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Ambil input dari form
$author  = $_POST['author']  ?? '';
$keyword = $_POST['keyword'] ?? '';
$limit   = $_POST['limit']   ?? 5;

// Path Python & Script
$python = '"C:\\Program Files\\Python312\\python.exe"';
$script = '"C:\\xampp\\htdocs\\IIRProject\\crawl.py"';

// Jalankan Python - redirect stderr ke file terpisah
$cmd = $python . " " . $script . " "
    . escapeshellarg($author) . " "
    . escapeshellarg($keyword) . " "
    . escapeshellarg($limit) . " 2>&1";

$output = shell_exec($cmd);

// Validasi output
if (!$output) {
    die("<h3>Error</h3><pre>Python tidak mengembalikan output</pre>");
}

// Coba decode JSON langsung
$data = json_decode(trim($output), true);

if (json_last_error() !== JSON_ERROR_NONE) {
    // Jika gagal, coba extract JSON dari output
    $json_start = strpos($output, '{');
    $json_end = strrpos($output, '}');

    if ($json_start !== false && $json_end !== false) {
        $json_str = substr($output, $json_start, $json_end - $json_start + 1);
        $data = json_decode($json_str, true);
    }

    if (json_last_error() !== JSON_ERROR_NONE) {
        echo "<h3>Error JSON Decode</h3>";
        echo "<p><strong>JSON Error:</strong> " . json_last_error_msg() . "</p>";
        echo "<p><strong>Raw Output (first 500 chars):</strong></p>";
        echo "<pre>" . htmlspecialchars(substr($output, 0, 500)) . "...</pre>";
        exit;
    }
}

if (isset($data['error'])) {
    die("<h3>Error</h3><pre>" . htmlspecialchars($data['error']) . "</pre>");
}

// Ambil data utama
$author_id = $data['author_id'] ?? '-';
$results   = $data['results']   ?? [];
$total_found = $data['total_found'] ?? 0;

if (!is_array($results)) {
    die("<h3>Error</h3><pre>Format data tidak valid</pre>");
}
?>

<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Hasil Pencarian</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        h2 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }

        .search-info {
            background: linear-gradient(135deg, #e8f4fc 0%, #d1e7ff 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 5px solid #3498db;
        }

        .search-info p {
            margin: 8px 0;
            font-size: 16px;
        }

        .search-info b {
            color: #2c3e50;
        }

        .stats-box {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            flex: 1;
            min-width: 200px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: transform 0.3s;
        }

        .stat-item:hover {
            transform: translateY(-5px);
        }

        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #7f8c8d;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        th {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 18px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
        }

        td {
            padding: 18px;
            border-bottom: 1px solid #ecf0f1;
            vertical-align: top;
        }

        tr:nth-child(even) {
            background: #f8f9fa;
        }

        tr:hover {
            background: #e8f4fc;
            transition: background 0.3s;
        }

        .similarity-cell {
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        }

        .similarity-high {
            color: #27ae60;
            background: #e8f6ef;
            padding: 8px 12px;
            border-radius: 6px;
            display: inline-block;
            min-width: 80px;
        }

        .similarity-medium {
            color: #f39c12;
            background: #fef5e7;
            padding: 8px 12px;
            border-radius: 6px;
            display: inline-block;
            min-width: 80px;
        }

        .similarity-low {
            color: #e74c3c;
            background: #fdedec;
            padding: 8px 12px;
            border-radius: 6px;
            display: inline-block;
            min-width: 80px;
        }

        .btn-journal {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 10px 18px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            display: inline-block;
            box-shadow: 0 2px 5px rgba(52, 152, 219, 0.2);
        }

        .btn-journal:hover {
            background: linear-gradient(135deg, #2980b9 0%, #1f639e 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
        }

        .btn-journal:active {
            transform: translateY(0);
        }

        .btn-journal i {
            margin-right: 5px;
        }

        .keyword-match {
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 5px;
            vertical-align: middle;
        }

        .btn-back {
            display: inline-block;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 8px;
            margin-top: 30px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }

        .btn-back:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }

        .no-results {
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-radius: 10px;
            margin: 20px 0;
            border: 2px dashed #ffb300;
        }

        .no-results h3 {
            color: #f39c12;
            margin-bottom: 20px;
        }

        .citation-count {
            font-weight: bold;
            padding: 5px 10px;
            border-radius: 4px;
            display: inline-block;
            min-width: 40px;
            text-align: center;
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
        }

        .title-cell {
            font-weight: 500;
            line-height: 1.5;
        }

        .author-cell {
            color: #555;
            font-size: 14px;
            line-height: 1.4;
        }

        .date-cell {
            color: #7f8c8d;
            font-size: 14px;
        }

        .journal-cell {
            color: #3498db;
            font-weight: 500;
        }

        @media (max-width: 1200px) {
            .container {
                padding: 20px;
            }

            table {
                font-size: 14px;
            }

            th,
            td {
                padding: 12px;
            }

            .stat-item {
                min-width: 150px;
            }

            .btn-journal {
                padding: 8px 14px;
                font-size: 13px;
            }
        }

        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .container {
                padding: 15px;
            }

            table {
                display: block;
                overflow-x: auto;
            }

            .stats-box {
                flex-direction: column;
            }
        }
    </style>
    <!-- Font Awesome untuk icon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>

<body>
    <div class="container">

        <h2>🔍 Hasil Pencarian Artikel Ilmiah</h2>

        <div class="search-info">
            <p><b>👤 Nama Penulis:</b> <?= htmlspecialchars($author) ?></p>
            <p><b>🆔 Author ID:</b> <?= htmlspecialchars($author_id) ?></p>
            <p><b>🔎 Keyword Pencarian:</b> <span style="background:#ffeb3b; padding:5px 12px; border-radius:5px; font-weight:bold;"><?= htmlspecialchars($keyword) ?></span></p>
            <p><b>📊 Limit Artikel:</b> <?= htmlspecialchars($limit) ?></p>
        </div>

        <div class="stats-box">
            <div class="stat-item">
                <div class="stat-value"><?= $total_found ?></div>
                <div class="stat-label">Total Artikel</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">
                    <?php
                    if ($total_found > 0) {
                        $avg_similarity = array_sum(array_column($results, 'similarity')) / $total_found;
                        echo number_format($avg_similarity, 3);
                    } else {
                        echo "0.000";
                    }
                    ?>
                </div>
                <div class="stat-label">Rata-rata Similarity</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">
                    <?php
                    $high_similarity = count(array_filter($results, function ($r) {
                        return ($r['similarity'] ?? 0) >= 0.7;
                    }));
                    echo $high_similarity;
                    ?>
                </div>
                <div class="stat-label">Similarity Tinggi (≥0.7)</div>
            </div>
        </div>

        <?php if ($total_found > 0): ?>

            <table>
                <thead>
                    <tr>
                        <th width="30%">📚 Judul Artikel</th>
                        <th width="15%">👤 Penulis</th>
                        <th width="10%">📅 Tanggal</th>
                        <th width="15%">🏛️ Jurnal</th>
                        <th width="8%">📊 Sitasi</th>
                        <th width="12%">🔗 Link Jurnal</th>
                        <th width="10%">📈 Similarity</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results as $row):
                        $similarity = $row['similarity'] ?? 0;
                        $similarityClass = 'similarity-low';
                        if ($similarity >= 0.7) $similarityClass = 'similarity-high';
                        elseif ($similarity >= 0.3) $similarityClass = 'similarity-medium';

                        $citation_count = $row['sitasi'] ?? '0';
                        $contains_keyword = $row['contains_keyword'] ?? false;
                        
                        // Escape JavaScript untuk keamanan
                        $link = isset($row['link']) && $row['link'] != '-' ? htmlspecialchars($row['link'], ENT_QUOTES, 'UTF-8') : '';
                        $button_text = isset($row['link_text']) ? htmlspecialchars($row['link_text'], ENT_QUOTES, 'UTF-8') : 'Buka Jurnal';
                        
                        // Pendekkan teks jika terlalu panjang
                        if (strlen($button_text) > 20) {
                            $button_text = substr($button_text, 0, 17) . '...';
                        }
                    ?>
                        <tr>
                            <td class="title-cell">
                                <?= htmlspecialchars($row['judul'] ?? '-') ?>
                                <?php if ($contains_keyword): ?>
                                    <span class="keyword-match" title="Judul mengandung keyword">✓ match</span>
                                <?php endif; ?>
                            </td>
                            <td class="author-cell">
                                <?php
                                $authors = $row['penulis'] ?? '-';
                                echo htmlspecialchars($authors);
                                ?>
                            </td>
                            <td class="date-cell"><?= htmlspecialchars($row['tanggal'] ?? '-') ?></td>
                            <td class="journal-cell">
                                <?php
                                $journal = $row['jurnal'] ?? '-';
                                echo htmlspecialchars($journal);
                                ?>
                            </td>
                            <td style="text-align: center;">
                                <span class="citation-count" title="Jumlah sitasi"><?= htmlspecialchars($citation_count) ?></span>
                            </td>
                            <td>
                                <?php if (!empty($link)): ?>
                                    <button type="button" 
                                            class="btn-journal" 
                                            onclick="window.open('<?= $link ?>', '_blank')"
                                            title="Buka jurnal di tab baru: <?= htmlspecialchars($row['link'] ?? '') ?>">
                                        <i class="fas fa-external-link-alt"></i> <?= $button_text ?>
                                    </button>
                                <?php else: ?>
                                    <span style="color: #95a5a6; font-style: italic;">Tidak tersedia</span>
                                <?php endif; ?>
                            </td>
                            <td class="similarity-cell">
                                <span class="<?= $similarityClass ?>" title="Nilai similarity: <?= number_format($similarity, 4) ?>">
                                    <?= number_format($similarity, 4) ?>
                                </span>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>

        <?php else: ?>
            <div class="no-results">
                <h3>⚠️ Tidak ada artikel yang ditemukan</h3>
                <p>Tidak ada artikel yang ditemukan untuk penulis <b>"<?= htmlspecialchars($author) ?>"</b></p>
                <p>Coba gunakan nama penulis yang berbeda atau periksa koneksi internet Anda.</p>
            </div>
        <?php endif; ?>

        <div style="margin-top: 30px; text-align: center;">
            <button onclick="window.location.href='index.html'" class="btn-back">
                <i class="fas fa-arrow-left"></i> Kembali ke Halaman Pencarian
            </button>
        </div>

    </div>

    <script>
        function openJournal(url) {
            if (url && url !== '-') {
                window.open(url, '_blank');
            }
        }
    </script>
</body>

</html>