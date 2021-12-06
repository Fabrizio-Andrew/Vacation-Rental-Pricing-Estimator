document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#login-button').addEventListener('click', () => {
        document.cookie = "session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    })
}) 