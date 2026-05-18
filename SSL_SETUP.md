# SSL 证书配置指南

## 方案一: 使用 Let's Encrypt 免费证书（推荐）

### 1. 安装 Certbot

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot

# CentOS/RHEL
sudo yum install certbot
```

### 2. 生成证书

```bash
# 停止 Nginx 容器（如果正在运行）
cd /opt/red-book-agent
docker-compose down

# 生成证书
sudo certbot certonly --standalone -d redbook.fffup.asia

# 证书生成位置
# /etc/letsencrypt/live/redbook.fffup.asia/fullchain.pem
# /etc/letsencrypt/live/redbook.fffup.asia/privkey.pem
```

### 3. 复制证书到项目目录

```bash
# 创建 SSL 目录
mkdir -p /opt/red-book-agent/nginx/ssl

# 复制证书文件
sudo cp /etc/letsencrypt/live/redbook.fffup.asia/fullchain.pem /opt/red-book-agent/nginx/ssl/
sudo cp /etc/letsencrypt/live/redbook.fffup.asia/privkey.pem /opt/red-book-agent/nginx/ssl/

# 设置权限
sudo chmod 644 /opt/red-book-agent/nginx/ssl/fullchain.pem
sudo chmod 600 /opt/red-book-agent/nginx/ssl/privkey.pem
```

### 4. 设置自动续期

```bash
# 创建续期脚本
sudo nano /usr/local/bin/renew-ssl.sh
```

添加以下内容：

```bash
#!/bin/bash
cd /opt/red-book-agent
docker-compose down
sudo certbot renew --quiet
sudo cp /etc/letsencrypt/live/redbook.fffup.asia/fullchain.pem /opt/red-book-agent/nginx/ssl/
sudo cp /etc/letsencrypt/live/redbook.fffup.asia/privkey.pem /opt/red-book-agent/nginx/ssl/
docker-compose up -d
```

```bash
# 设置执行权限
sudo chmod +x /usr/local/bin/renew-ssl.sh

# 添加到 crontab（每月1号凌晨3点自动续期）
sudo crontab -e
```

添加以下行：

```
0 3 1 * * /usr/local/bin/renew-ssl.sh >> /var/log/ssl-renew.log 2>&1
```

---

## 方案二: 使用已有的 SSL 证书

如果你已经购买了 SSL 证书，直接将证书文件放到项目目录：

```bash
# 创建 SSL 目录
mkdir -p /opt/red-book-agent/nginx/ssl

# 上传证书文件到服务器
# fullchain.pem - 完整证书链
# privkey.pem - 私钥文件

# 设置权限
chmod 644 /opt/red-book-agent/nginx/ssl/fullchain.pem
chmod 600 /opt/red-book-agent/nginx/ssl/privkey.pem
```

---

## 部署 HTTPS 版本

```bash
cd /opt/red-book-agent

# 使用 HTTPS 模式部署
chmod +x deploy.sh
./deploy.sh https
```

---

## 验证 HTTPS 配置

部署完成后，访问以下地址验证：

- 前端: https://redbook.fffup.asia
- 后端API: https://redbook.fffup.asia/api
- 健康检查: https://redbook.fffup.asia/health

---

## 常见问题

### 1. 证书生成失败

确保：
- 域名 DNS 已正确解析到服务器 IP
- 服务器 80 和 443 端口已开放
- 防火墙允许 HTTP/HTTPS 流量

### 2. 证书权限错误

```bash
sudo chmod 644 /opt/red-book-agent/nginx/ssl/fullchain.pem
sudo chmod 600 /opt/red-book-agent/nginx/ssl/privkey.pem
```

### 3. HTTPS 无法访问

检查：
- 证书文件是否正确放置
- Nginx 配置是否正确
- 防火墙是否开放 443 端口

```bash
# 检查 Nginx 配置
docker-compose logs nginx-proxy

# 检查端口监听
netstat -tlnp | grep 443
```
