function converter() {
    const valor = document.getElementById('valor').value;
    if (valor <= 0) {
        alert("Por favor, insira um valor válido.");
        return;
    }
    
    // Desabilitar o botão enquanto a conversão está sendo feita
    const button = document.querySelector('button');
    button.disabled = true;
    button.innerText = "Convertendo...";

    fetch('/converter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `valor=${valor}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.valor_convertido) {
            const resultadoDiv = document.getElementById('resultado');
            resultadoDiv.textContent = `Valor em dólares: $${data.valor_convertido}`;
            resultadoDiv.style.opacity = 0;
            setTimeout(() => {
                resultadoDiv.style.opacity = 1;
                resultadoDiv.style.transition = "opacity 0.5s ease-in-out";
            }, 100);
        } else {
            document.getElementById('resultado').textContent = `Erro: ${data.error}`;
        }
    })
    .catch(error => console.log("Erro ao converter:", error))
    .finally(() => {
        // Reabilitar o botão após a conversão
        button.disabled = false;
        button.innerText = "Converter";
    });
}

// Adicionando evento para o pressionamento da tecla Enter
document.getElementById('valor').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        converter();
    }
});
