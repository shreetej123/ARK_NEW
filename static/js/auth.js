const SUPABASE_URL = 'https://xomxlaylzvklvhnwuvjq.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhvbXhsYXlsenZrbHZobnd1dmpxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNjMwNDQsImV4cCI6MjA4NTkzOTA0NH0.zj_NLY_A2LjTWqVPdN0vB13seLloa0A_1Iydb-nybS4';

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let isLoginMode = true;

async function checkAuth() {
    const { data: { user } } = await supabase.auth.getUser();
    updateAuthUI(user);
    return user;
}

function updateAuthUI(user) {
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    if (user) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (signupBtn) signupBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (signupBtn) signupBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();

    const modal = document.getElementById('authModal');
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const closeBtn = document.querySelector('.close');
    const authForm = document.getElementById('authForm');
    const toggleMode = document.getElementById('toggleMode');

    if (loginBtn) {
        loginBtn.onclick = () => {
            isLoginMode = true;
            updateModalMode();
            modal.style.display = 'block';
        };
    }

    if (signupBtn) {
        signupBtn.onclick = () => {
            isLoginMode = false;
            updateModalMode();
            modal.style.display = 'block';
        };
    }

    if (logoutBtn) {
        logoutBtn.onclick = async () => {
            await supabase.auth.signOut();
            window.location.href = '/';
        };
    }

    if (closeBtn) {
        closeBtn.onclick = () => {
            modal.style.display = 'none';
        };
    }

    if (toggleMode) {
        toggleMode.onclick = (e) => {
            e.preventDefault();
            isLoginMode = !isLoginMode;
            updateModalMode();
        };
    }

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    if (authForm) {
        authForm.onsubmit = async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const fullName = document.getElementById('fullName').value;

            try {
                if (isLoginMode) {
                    const { data, error } = await supabase.auth.signInWithPassword({
                        email: email,
                        password: password,
                    });

                    if (error) throw error;
                    alert('Login successful!');
                    modal.style.display = 'none';
                    await checkAuth();
                    window.location.reload();
                } else {
                    const { data, error } = await supabase.auth.signUp({
                        email: email,
                        password: password,
                        options: {
                            data: {
                                full_name: fullName,
                            }
                        }
                    });

                    if (error) throw error;

                    if (data.user) {
                        const { error: profileError } = await supabase
                            .from('profiles')
                            .insert([
                                {
                                    id: data.user.id,
                                    email: email,
                                    full_name: fullName,
                                }
                            ]);

                        if (profileError) console.error('Profile creation error:', profileError);
                    }

                    alert('Account created successfully!');
                    modal.style.display = 'none';
                    isLoginMode = true;
                    updateModalMode();
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        };
    }
});

function updateModalMode() {
    const modalTitle = document.getElementById('modalTitle');
    const toggleText = document.getElementById('toggleText');
    const toggleMode = document.getElementById('toggleMode');
    const nameGroup = document.getElementById('nameGroup');

    if (isLoginMode) {
        modalTitle.textContent = 'Login';
        toggleText.textContent = "Don't have an account?";
        toggleMode.textContent = 'Sign up';
        nameGroup.style.display = 'none';
    } else {
        modalTitle.textContent = 'Sign Up';
        toggleText.textContent = 'Already have an account?';
        toggleMode.textContent = 'Login';
        nameGroup.style.display = 'block';
    }
}

supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN') {
        updateAuthUI(session.user);
    } else if (event === 'SIGNED_OUT') {
        updateAuthUI(null);
    }
});
