import { useCallback } from "react"
// import { useEffect } from "react"
// import Cookies from "js-cookie";

export function Login() {

    const handleLogin = useCallback(() => {
        window.location.href = "/api/v1/users/auth/authorize" ;
    }, [])

    return (
        <div>
            <button onClick={handleLogin}>Login</button>
        </div>
    )
}