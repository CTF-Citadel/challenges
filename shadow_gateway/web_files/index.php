<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["crypto_code"])) {
    $userInput = $_POST["crypto_code"];

    $searchResults = shell_exec("ls /opt/filestash/ | grep " . $userInput);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Vault</title>
    <style>
        body {
            background-color: black; 
            color: white;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0; 
        }

        h1 {
            font-size: 24px; 
        }

        form input[type="text"], form button {
            margin-top: 10px;
            display: block; 
            margin-bottom: 10px; 
            padding: 10px;
            font-size: 16px; 
        }

        label {
            margin-top: 10px;
            font-size: 35px;
            font-weight: 900;
        }

        button {
            margin-top: 10px;
            align-items: center;
            background-color: #007bff;
            color: white; 
            border: none; 
            cursor: pointer; 
            width: 100%;
        }

        button:hover {
            background-color: #0056b3; 
        }

        h2 {
            font-size: 20px; 
            margin-top: 20px; 
        }

        .search-result {
            margin-top: 10px; 
        }
    </style>
</head>
<body>
    <form action="index.php" method="POST">
        <label for="crypto_input">Crypto Vault</label>
        <input type="text" id="crypto_input" name="crypto_code" required>
        <button type="submit">Search</button>
    </form>
    
    <?php
    if (!empty($searchResults)) {
        echo "<h2>Search Results:</h2>";
        echo "<pre>" . $searchResults . "</pre>";
    } elseif (isset($_POST["crypto_code"])) {
        echo "<p>No matching items found.</p>";
    }
    ?>
</body>
</html>
