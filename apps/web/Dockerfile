# apps/web/Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@10.15.0 --activate
# nur Manifeste kopieren, damit der Layer cachen kann
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile

FROM node:20-alpine AS build
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@10.15.0 --activate
# zuerst node_modules aus deps übernehmen
COPY --from=deps /app/node_modules ./node_modules
# dann den Rest des Codes kopieren
COPY . .
# Standalone Build für schlanken Runner
RUN pnpm build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Standalone enthält Runtime, keine prod-deps nötig
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./public/_next/static
# falls du ein /public hast:
COPY --from=build /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]

