'use client';
import React from 'react';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from '@/app/firebase/config';
import { useRouter } from 'next/navigation';

const Signin = () => {
    const router = useRouter();

    const signInWithGoogle = async () => {
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
            router.push('/');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h1 style={styles.title}>Sign In</h1>
                <button onClick={signInWithGoogle} style={styles.button}>
                    <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google Logo" style={styles.logo} />
                    <span style={styles.buttonText}>Sign in with Google</span>
                </button>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f5f5f5'
    },
    card: {
        textAlign: 'center',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
        backgroundColor: '#fff'
    },
    title: {
        marginBottom: '20px',
        fontSize: '24px',
        color: '#333'
    },
    button: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '4px',
        backgroundColor: '#4285F4',
        color: '#fff',
        fontSize: '16px',
        cursor: 'pointer',
        outline: 'none',
        fontWeight: 'bold'
    },
    logo: {
        width: '20px',
        height: '20px',
        marginRight: '10px'
    },
    buttonText: {
        marginLeft: '10px'
    }
};

export default Signin;
