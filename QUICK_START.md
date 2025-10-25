# 🎯 Quick Start Guide - Deploy to Render

## 📝 TL;DR (Tóm Tắt)

```bash
# 1. Cập nhật code
git add .
git commit -m "Ready for Render deployment"
git push origin main

# 2. Deploy trên Render Dashboard
# - Tạo Web Service mới
# - Connect GitHub repo
# - Chọn Docker runtime
# - Thêm environment variables
# - Deploy!

# 3. Setup Keep-Alive (chọn 1 trong các cách):
# - Cron-Job.org (khuyến nghị)
# - UptimeRobot
# - GitHub Actions
```

---

## 🚀 3 Bước Deploy Nhanh

### Bước 1: Push Code Lên GitHub ✅

```bash
git add .
git commit -m "Prepare for Render deployment with keep-alive"
git push origin main
```

### Bước 2: Deploy Trên Render (5 phút) 🌐

1. **Đi tới**: https://dashboard.render.com/
2. **New +** → **Web Service**
3. **Connect repository** → Chọn repo RCM_RECIPE_2
4. **Cấu hình**:
   - Name: `rcm-recipe-api`
   - Runtime: **Docker**
   - Health Check Path: `/health`
5. **Environment Variables** (tab Environment):
   ```
   GEMINI_API_KEY = your_api_key_here
   DATABASE_URL = your_mongodb_url (optional)
   REDIS_URL = your_redis_url (optional)
   PORT = 8000
   ```
6. **Create Web Service** ✅

### Bước 3: Setup Keep-Alive (2 phút) ⏰

**Cách Dễ Nhất - Sử dụng Cron-Job.org:**

1. Đi tới: https://cron-job.org/
2. Đăng ký (miễn phí)
3. **Create cronjob**:
   - Title: `RCM Recipe Keep Alive`
   - URL: `https://your-service.onrender.com/ping`
   - Schedule: **Every 5 minutes**
   - Save ✅

**Hoặc Sử dụng UptimeRobot:**

1. Đi tới: https://uptimerobot.com/
2. Đăng ký (miễn phí - 50 monitors)
3. **Add Monitor**:
   - Type: `HTTP(s)`
   - URL: `https://your-service.onrender.com/ping`
   - Interval: **5 minutes**
   - Create ✅

---

## ✅ Kiểm Tra Deployment

### Test Health Endpoint

```bash
curl https://your-service.onrender.com/health
```

✅ **Kết quả mong đợi:**

```json
{
  "status": "healthy",
  "service": "RCM Recipe Generator",
  "version": "1.0.0"
}
```

### Test Ping Endpoint

```bash
curl https://your-service.onrender.com/ping
```

✅ **Kết quả mong đợi:**

```json
{
  "status": "pong",
  "message": "Service is alive",
  "timestamp": "2025-10-25T10:30:00.123456"
}
```

### Xem API Docs

Truy cập: `https://your-service.onrender.com/docs`

---

## 🔑 Lấy API Keys

### GEMINI_API_KEY (BẮT BUỘC)

1. Truy cập: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy và paste vào Render Environment Variables

### MongoDB (Optional)

- **Miễn phí**: https://www.mongodb.com/cloud/atlas
- Tạo cluster → Get connection string
- Format: `mongodb+srv://user:pass@cluster.mongodb.net/db`

### Redis (Optional)

- **Upstash Redis**: https://upstash.com/ (miễn phí)
- **Render Redis**: Dashboard → New → Redis

---

## 🎯 Files Đã Tạo

✅ `render.yaml` - Render configuration
✅ `Dockerfile` - Container configuration (updated)
✅ `.dockerignore` - Ignore files for Docker
✅ `RENDER_DEPLOYMENT_GUIDE.md` - Hướng dẫn chi tiết
✅ `QUICK_START.md` - Hướng dẫn nhanh (file này)
✅ `keep_alive.py` - Script Python để ping service
✅ `.github/workflows/keep-alive.yml` - GitHub Actions workflow

---

## 🔧 Endpoints Mới

| Endpoint  | Method | Mô Tả                   |
| --------- | ------ | ----------------------- |
| `/health` | GET    | Health check cho Render |
| `/ping`   | GET    | Keep-alive endpoint     |
| `/`       | GET    | API info                |
| `/docs`   | GET    | Swagger UI              |

---

## 🆘 Troubleshooting Nhanh

### ❌ Service không start

**→ Check Logs**: Dashboard → Your Service → Logs tab

### ❌ "GEMINI_API_KEY not found"

**→ Fix**: Environment tab → Add variable → Save Changes → Redeploy

### ❌ Service bị spin down

**→ Fix**: Setup keep-alive ping (Bước 3 ở trên)

### ❌ 502 Bad Gateway

**→ Wait**: Service đang deploy (2-3 phút)
**→ Check**: Logs để xem lỗi

---

## 📊 Monitor Service

### Render Dashboard

- **Metrics**: CPU, Memory usage
- **Logs**: Real-time application logs
- **Events**: Deployment history

### Custom Monitoring

```python
# Test từ terminal
watch -n 10 'curl -s https://your-service.onrender.com/ping | jq'
```

---

## 💡 Tips

1. **Sử dụng environment variables** cho sensitive data (API keys)
2. **Monitor logs** trong lần deploy đầu tiên
3. **Setup alerts** với UptimeRobot để biết khi service down
4. **Check quota** của free tier: 750 hours/month
5. **Upgrade plan** nếu cần:
   - No spin down: $7/month
   - More resources: scaling options

---

## 🔗 Quick Links

- **Render Dashboard**: https://dashboard.render.com/
- **Cron-Job.org**: https://cron-job.org/
- **UptimeRobot**: https://uptimerobot.com/
- **Google AI Studio**: https://makersuite.google.com/
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas

---

## ✨ Next Steps

Sau khi deploy thành công:

1. ✅ Test tất cả API endpoints
2. ✅ Setup monitoring
3. ✅ Configure custom domain (optional)
4. ✅ Setup CI/CD auto-deploy
5. ✅ Add more features!

---

**Cần thêm thông tin?** → Xem file `RENDER_DEPLOYMENT_GUIDE.md` để có hướng dẫn chi tiết hơn!

---

🎉 **Good luck with your deployment!** 🚀
