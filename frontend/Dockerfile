FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve static files
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN npm install serve --omit=dev
COPY --from=builder /app/build ./build
USER node
EXPOSE 3000
CMD ["npx", "serve", "build", "-l", "3000"]