import { useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router";

import Button from "../components/ui/Button";
import Field from "../components/ui/Field";
import { useAuth } from "../hooks/useAuth";
import { getAuthErrors } from "../api/authErrors";
import { getAuthDestination } from "../utils/authRedirect";

export default function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {
        e.preventDefault();
        if (loading) return;

        const form = new FormData(e.currentTarget);

        const email = String(form.get("email") || "").trim();
        const password = String(form.get("password") || "");

        setErrors({});

        setLoading(true);

        try {
            await login({ email, password });
            navigate(getAuthDestination(location.state?.from), { replace: true });
        } catch (error) {
            setErrors(getAuthErrors(error, "Не удалось войти. Попробуйте ещё раз."));
        } finally {
            setLoading(false);
        }
    }

    return (
        <main>
            <div>
                <div>

                    <h1>
                        С возвращением!
                    </h1>

                    <p>
                        Войдите в свой аккаунт, чтобы продолжить
                    </p>
                </div>

                <div>
                    <form
                        onSubmit={handleSubmit}
                        noValidate
                        aria-busy={loading}
                    >
                        <Field
                            label="Email"
                            name="email"
                            type="email"
                            placeholder="example@mail.com"
                            autoComplete="email"
                            error={errors.email}
                        />

                        <Field
                            label="Пароль"
                            name="password"
                            type="password"
                            placeholder="Введите пароль"
                            autoComplete="current-password"
                            error={errors.password}
                        />

                        {errors.form && (
                            <p role="alert">
                                {errors.form}
                            </p>
                        )}

                        <Button
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Вход..." : "Войти"}
                        </Button>
                    </form>

                    <div>
                        <p>
                            Нет аккаунта?{" "}
                            <NavLink
                                to="/register"
                                state={location.state}
                            >
                                Зарегистрироваться
                            </NavLink>
                        </p>
                    </div>
                </div>
            </div>
        </main>
    );
}

