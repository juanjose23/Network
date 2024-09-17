function toggleLike(postId) {
    console.log(postId);
    fetch(`/posts/${postId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                console.log('Error:', result.error);
                return;
            }

            const likesCountElement = document.querySelector(`#likes-count-${postId}`);
            const likeButton = document.querySelector(`#like-button-${postId}`);

            if (result.liked) {
                likesCountElement.textContent = parseInt(likesCountElement.textContent) + 1;
                likeButton.textContent = 'Unlike 👎';
            } else {
                likesCountElement.textContent = parseInt(likesCountElement.textContent) - 1;
                likeButton.textContent = 'Like 👍';
            }
        })
        .catch(error => console.error('Error:', error));  // Manejar errores
}
function toggleFollow(userId) {
    console.log(userId)
    fetch(`/users/${userId}/follow`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                console.log('Error:', result.error);
                return;
            }
            console.log('success', result.message);

            const followButtons = document.querySelectorAll(`[id^="follow-button-"]`);

            followButtons.forEach(button => {
                const buttonUserId = button.id.split('-').pop();
                if (parseInt(buttonUserId) === userId) {
                    button.textContent = result.following ? 'Unfollow' : 'Follow';
                }
            });
        })
        .catch(error => console.error('Error:', error));
}


function openEditModal(postId) {

const postContentElement = document.getElementById(`post-content-${postId}`);
const currentContent = postContentElement ? postContentElement.textContent.trim() : '';

// Actualizar el contenido del textarea en el modal
document.getElementById('post-id').value = postId;
document.getElementById('post-content').value = currentContent;

// Mostrar el modal
const editModal = new bootstrap.Modal(document.getElementById('editModal'));
editModal.show();
}

// Función para manejar la actualización del post
document.getElementById('editPostForm').addEventListener('submit', function (event) {
event.preventDefault();

const postId = document.getElementById('post-id').value;
const content = document.getElementById('post-content').value.trim();

// Validar que el contenido no esté vacío
if (content === '') {
    alert('Content cannot be empty. Please enter some text.');
    return;
}

fetch(`/posts/${postId}/edit`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ content })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Actualizar el contenido de la publicación en la página
        const postContentElement = document.getElementById(`post-content-${postId}`);
        if (postContentElement) {
            postContentElement.textContent = content;
        }

        // Ocultar el modal
        const editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
        editModal.hide();
    } else {
        console.error('Error:', data.error);
    }
})
.catch(error => console.error('Error:', error));
});
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}