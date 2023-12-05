<?php
// Conectar a la base de datos
$conexion = mysqli_connect('localhost', 'usuario', 'contraseña', 'basededatos');

// Verificar si se ha enviado el formulario de registro
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Obtener la información del formulario y limpiar los datos
    $nombre = mysqli_real_escape_string($conexion, $_POST['nombre']);
    $email = mysqli_real_escape_string($conexion, $_POST['email']);
    $contraseña = mysqli_real_escape_string($conexion, $_POST['contraseña']);

    // Validar los datos ingresados por el usuario
    if (empty($nombre) || empty($email) || empty($contraseña)) {
        // Mostrar un mensaje de error si algún campo está vacío
        echo 'Por favor, complete todos los campos del formulario.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Mostrar un mensaje de error si el correo electrónico no es válido
        echo 'Por favor, ingrese un correo electrónico válido.';
    } else {
        // Encriptar la contraseña
        $contraseña_encriptada = password_hash($contraseña, PASSWORD_DEFAULT);

        // Insertar la información del usuario en la base de datos utilizando una sentencia preparada
        $query = "INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)";
        $stmt = mysqli_prepare($conexion, $query);
        mysqli_stmt_bind_param($stmt, 'sss', $nombre, $email, $contraseña_encriptada);
        mysqli_stmt_execute($stmt);

        // Redirigir al usuario a la página de inicio de sesión
        header('Location: inicio_de_sesion.php');
        exit;
    }
}
?>