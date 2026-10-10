import axios from "axios";

const messages = {
    "User not exists": "Неверный email или пароль.",
    "Invalid password": "Неверный email или пароль.",
    "User already exists": "Пользователь с таким email уже зарегистрирован.",
    "Passwords do not match": "Пароли не совпадают.",
};

const fields = {
    email: "email",
    login: "username",
    password: "password",
    repeat_password: "confirmPassword",
};

export function getAuthErrors(error, fallback) {
    if (!axios.isAxiosError(error)) return { form: fallback };
    if (!error.response) {
        return { form: "Сервер не отвечает. Проверьте подключение и попробуйте ещё раз." };
    }
    const detail = error.response.data?.detail;
    if (Array.isArray(detail)) {
        const errors = {};
        for (const issue of detail) {
            const field = fields[issue.loc?.at(-1)];
            const key = field || "form";
            if (errors[key]) continue;
            switch (issue.type) {
                case "missing":
                    errors[key] = "Заполните обязательное поле.";
                    break;
                case "string_too_short":
                    errors[key] = issue.ctx?.min_length === 1
                        ? "Заполните обязательное поле."
                        : `Минимум ${issue.ctx?.min_length} символов.`;
                    break;
                case "string_too_long":
                    errors[key] = `Максимум ${issue.ctx?.max_length} символов.`;
                    break;
                case "string_pattern_mismatch":
                    errors[key] = field === "email"
                        ? "Введите корректный email."
                        : "Проверьте формат значения.";
                    break;
                case "password_empty":
                case "password_mismatch":
                    errors[key] = issue.msg;
                    break;
                default:
                    errors[key] = "Проверьте введённое значение.";
            }
        }
        return Object.keys(errors).length ? errors : { form: fallback };
    }
    if (error.response.status === 401) {
        return { form: "Неверный email или пароль." };
    }
    return { form: messages[detail] || fallback };
}
