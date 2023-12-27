import { useCallback } from "react"

export function Home() {

    const handleLogin = useCallback(() => {
        const url_code = `https://api.intra.42.fr/oauth/authorize?client_id=`+import.meta.env.VITE_FT_CID+`&redirect_uri=`+import.meta.env.VITE_REDIRECT_URI+`&response_type=code`;
        window.location.replace(url_code)
    }, [])

    return (
        <button onClick={handleLogin}>Login</button>
    )
}