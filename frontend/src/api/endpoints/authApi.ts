
import { privateApi } from "../privateApi";
import { User, RegisterPayload, LoginPayload } from "../../types/auth";
import { publicApi } from "../publicApi";


export const authApi = {
    login(payload: LoginPayload): Promise<User> {
        return publicApi.post<User>("/api/auth/login", payload);
    },

    register(payload: RegisterPayload): Promise<User> {
        return publicApi.post<User>("/api/auth/register", payload);
    },

    refresh(): Promise<void> {
        return publicApi.post<void>("/api/auth/refresh");
    },

    me(): Promise<User> {
        return privateApi.get<User>("/api/auth/me");
    },

    logout(): Promise<void> {
        return privateApi.post<void>("/api/auth/logout");
    },
};
