async function loginAsAdmin(email: string, password: string) {
    const baseUrl = 'https://127.0.0.1:8000';
    const endpoint = '/admins/login'

    const response = await fetch(`${baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    return response.json();
}

export {
    loginAsAdmin
};