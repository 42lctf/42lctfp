import { useAuth } from '@/providers/AuthProvider';
import { isDef } from '@/technical/isDef';
import { useCallback } from 'react';
import { Paths } from '@/technical/Paths';
import { redirect } from 'react-router';

export function Header() {
    const { user } = useAuth();

    const handleLogin = useCallback(() => {
        redirect(Paths.AuthAuthorize);
    }, []);

    return (
        <div style={{ display: 'flex' }}>
            {
                isDef(user) ? <span>{user.id} - {user.nickname}</span> : <button onClick={handleLogin}>LOGIN</button>
            }
        </div>
    );
}