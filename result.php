<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT IIR - Pencarian Artikel Ilmiah</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }

        .header h1 {
            color: #333;
            font-size: 32px;
            margin-bottom: 15px;
        }

        .search-info {
            color: #666;
            font-size: 18px;
            margin-bottom: 20px;
        }

        .btn-back {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s ease;
        }

        .btn-back:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .results-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #f5c6cb;
        }

        .success-message {
            background: #d1edff;
            color: #004085;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #b3d7ff;
        }

        .warning-message {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #ffc107;
        }

        .method-info {
            background: #d1f7e6;
            color: #0f5132;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #28a745;
        }

        .table-container {
            overflow-x: auto;
            margin-top: 20px;
        }

        .results-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        .results-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        .results-table td {
            padding: 15px;
            border-bottom: 1px solid #e1e5e9;
        }

        .results-table tr:hover {
            background-color: #f8f9fa;
        }

        .similarity-high {
            color: #28a745;
            font-weight: bold;
            background: #d4edda;
            padding: 5px 10px;
            border-radius: 20px;
            text-align: center;
        }

        .similarity-medium {
            color: #ffc107;
            font-weight: bold;
            background: #fff3cd;
            padding: 5px 10px;
            border-radius: 20px;
            text-align: center;
        }

        .similarity-low {
            color: #dc3545;
            font-weight: bold;
            background: #f8d7da;
            padding: 5px 10px;
            border-radius: 20px;
            text-align: center;
        }

        .journal-link {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 14px;
            transition: background 0.3s ease;
        }

        .journal-link:hover {
            background: #218838;
        }

        .processing-info {
            background: #e2f0ff;
            color: #004085;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header fade-in'>
            <h1>PROJECT IIR - Pencarian Data Artikel Ilmiah</h1>
            <div class='search-info'>
                <?php
                if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                    $author = htmlspecialchars($_POST['author']);
                    $keyword = htmlspecialchars($_POST['keyword']);
                    $count = htmlspecialchars($_POST['count']);
                    
                    echo "Penulis: <strong>{$author}</strong> | ";
                    echo "Keyword: <strong>{$keyword}</strong> | ";
                    echo "Jumlah: <strong>{$count} artikel</strong>";
                } else {
                    echo "<strong>Silakan gunakan form pencarian terlebih dahulu</strong>";
                }
                ?>
            </div>
            <a href='index.php' class='btn-back'>Kembali ke Pencarian</a>
        </div>
    </div>
</body>
</html>