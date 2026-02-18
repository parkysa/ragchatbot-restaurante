async function enviarPergunta() {
    const input = document.getElementById('usuario-input');
    const chatBox = document.getElementById('chat-box');
    const pergunta = input.value;

    if (!pergunta.trim()) return;

    // Adiciona pergunta do usuário
    chatBox.innerHTML += `<div class="message user">${pergunta}</div>`;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // Mostra um indicador de carregamento simples
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message bot";
    loadingDiv.innerText = "...";
    chatBox.appendChild(loadingDiv);

    try {
        const response = await fetch('http://localhost:5000/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pergunta: pergunta })
        });

        const dados = await response.json();
        
        // Remove o "..." e adiciona a resposta real
        chatBox.removeChild(loadingDiv);
        chatBox.innerHTML += `<div class="message bot">${dados.resposta}</div>`;
        
    } catch (error) {
        chatBox.removeChild(loadingDiv);
        chatBox.innerHTML += `<div class="message bot" style="color: red;">Desculpe, tive um problema ao conectar com o servidor.</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Escuta a tecla Enter
document.getElementById('usuario-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        enviarPergunta();
    }
});