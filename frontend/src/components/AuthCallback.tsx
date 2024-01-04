import { useCallback, useEffect, useRef } from 'react';
import { axiosClient } from '@/services/axiosInstance';
import { useAuth } from '@/providers/AuthProvider';

export function AuthCallback() {
    const { login } = useAuth();
    const code = window.location.href.split('code=')[1];
    const renderAfterCalled = useRef(false);

    const handleAuthorize = useCallback(async () => {
        await axiosClient.get(`/users/auth/callback?code=${code}`);
        login();
    }, [code, login]);

    useEffect(() => {
        if (renderAfterCalled.current) {
            return;
        }
        handleAuthorize();
        renderAfterCalled.current = true;
    }, [code, handleAuthorize, login]);

    return (
        <div>
            <h1>Waiting...</h1>
        </div>
    );
}