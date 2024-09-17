document.querySelector('#submit-post').addEventListener('click', function () {
    const content = document.querySelector('#new-post-content').value;
    if (!user_id) {
        alert('Por favor, inicia sesión para publicar.');
        return;
    }
    if (!content) {
        alert('The post content cannot be empty.');
        return;
    }

    fetch('/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
            content: content
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});


function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;  // Asegurarse de que el token esté en el HTML
}

