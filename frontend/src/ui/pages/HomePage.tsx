import { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

export function HomePage({ nickname }: { nickname: string }) {

    return (
        <div>
            <h1>Welcome {nickname}</h1>
        </div>
    );
}