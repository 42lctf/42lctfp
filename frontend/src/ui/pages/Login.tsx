import { useCallback } from "react"
// import { useEffect } from "react"
// import Cookies from "js-cookie";

export function Login() {

    const handleLogin = useCallback(() => {
        const url_code = `https://api.intra.42.fr/oauth/authorize?client_id=`+import.meta.env.VITE_FT_CID+`&redirect_uri=`+import.meta.env.VITE_REDIRECT_URI+`&response_type=code`;
        window.location.replace(url_code)
    }, [])

    return (
        <div>
            <button onClick={handleLogin}>Login</button>
        </div>
    )
}