import { useAuth } from '@/providers/AuthProvider';
import { isDef } from '@/technical/isDef';

export function Home() {
    const { user } = useAuth();

    return (
        <div>
            <h1>Welcome {isDef(user) ? user.nickname : 'guest'}</h1>
        </div>
    );
}