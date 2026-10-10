export interface User {
    id: number;
    email: string;
    login: string;
}

export interface LoginPayload {
    email: string;
    password: string;
}

export interface RegisterPayload {
    repeat_password: string;
    email: string;
    login: string;
    password: string;
}
