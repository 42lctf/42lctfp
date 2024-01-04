import { Login } from "./Login";
import { HomePage } from "./HomePage";
import { useAuth } from "@/providers/AuthProvider";

export function Home() {
    const { isLogged } = useAuth()

    return (
        <div>
            {isLogged ? <HomePage /> : <Login />}
        </div>
    );
}