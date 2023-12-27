import { Login } from "./Login";
import { HomePage } from "./HomePage";
import Cookies from "js-cookie";

export function Home() {
    const access_token = Cookies.get("access_token");

    return (
        <div>
            {access_token ? <HomePage /> : <Login /> }
        </div>
    )
}