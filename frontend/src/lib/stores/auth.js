import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function createAuthStore() {
    const { subscribe, set, update } = writable({
        user: null,
        loading: true
    });

    const store = {
        subscribe,
        login: async (email, password) => {
            try {
                const response = await fetch('http://localhost:3000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.message || 'Đăng nhập thất bại');
                }

                const userData = await response.json();
                set({ user: userData, loading: false });
                return { success: true };
            } catch (error) {
                set({ user: null, loading: false });
                return { success: false, message: error.message };
            }
        },
        register: async (name, email, password) => {
            try {
                const response = await fetch('http://localhost:3000/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, email, password })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.message || 'Đăng ký thất bại');
                }

                const userData = await response.json();
                set({ user: userData, loading: false });
                return { success: true };
            } catch (error) {
                return { success: false, message: error.message };
            }
        },
        logout: async () => {
            try {
                const response = await fetch('http://localhost:3000/api/logout', {
                    method: 'POST'
                });
                
                if (!response.ok) {
                    throw new Error('Đăng xuất thất bại');
                }
            } finally {
                set({ user: null, loading: false });
            }
        },
        checkSession: async () => {
            try {
                const response = await fetch('http://localhost:3000/api/check-session');
                if (response.ok) {
                    const userData = await response.json();
                    set({ user: userData, loading: false });
                } else {
                    set({ user: null, loading: false });
                }
            } catch {
                set({ user: null, loading: false });
            }
        }
    };

    // Check session on store creation if in browser
    if (browser) {
        store.checkSession();
    }

    return store;
}

export const { subscribe, login, register, logout, checkSession } = createAuthStore();
