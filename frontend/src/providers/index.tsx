import { ReactNode } from 'react';
import { AuthProvider } from './AuthProvider';

type Props = {
    children?: ReactNode
}

export function Providers({ children }: Props) {
    return (
        <AuthProvider>
            {children}
        </AuthProvider>
    );
}