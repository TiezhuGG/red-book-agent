FROM node:20-alpine AS build

WORKDIR /app

# 设置 npm 镜像为国内源，加速安装
ENV NPM_CONFIG_REGISTRY=https://registry.npmmirror.com
ENV NPM_CONFIG_FUND=false

# 安装必要的系统依赖（git 用于某些 npm 包）
RUN apk add --no-cache git

# 先复制 package.json，利用 Docker 缓存
COPY package*.json ./

# 使用 npm install 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 执行构建
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
