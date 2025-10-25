# 🚀 Hướng Dẫn Deploy RCM_RECIPE_2 Lên Render

## 📋 Mục Lục

1. [Chuẩn Bị](#chuẩn-bị)
2. [Deploy Lên Render](#deploy-lên-render)
3. [Cấu Hình Environment Variables](#cấu-hình-environment-variables)
4. [Giữ Service Luôn Hoạt Động](#giữ-service-luôn-hoạt-động)
5. [Kiểm Tra Deployment](#kiểm-tra-deployment)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Chuẩn Bị

### 1. Đảm Bảo Code Đã Commit

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Files Quan Trọng Đã Tạo

- ✅ `render.yaml` - Cấu hình deployment
- ✅ `Dockerfile` - Container configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `/health` endpoint - Health check
- ✅ `/ping` endpoint - Keep-alive endpoint

---

## 🌐 Deploy Lên Render

### Cách 1: Deploy Từ Dashboard (Khuyến Nghị)

1. **Truy cập Render Dashboard**

   - Đi tới: https://dashboard.render.com/
   - Đăng nhập hoặc tạo tài khoản mới

2. **Tạo Web Service Mới**

   - Click nút **"New +"** → Chọn **"Web Service"**
   - Hoặc click **"New Web Service"**

3. **Kết Nối Repository**

   - Chọn **"Connect a repository"**
   - Authorize Render truy cập GitHub/GitLab của bạn
   - Chọn repository chứa RCM_RECIPE_2

4. **Cấu Hình Service**

   **Basic Settings:**

   - **Name**: `rcm-recipe-api` (hoặc tên bạn muốn)
   - **Region**: `Singapore` (hoặc region gần nhất)
   - **Branch**: `main`
   - **Root Directory**: để trống (nếu project ở root)

   **Build & Deploy:**

   - **Runtime**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.`

   **Instance:**

   - **Instance Type**: `Free` (hoặc paid plan)

   **Advanced:**

   - **Health Check Path**: `/health`
   - **Auto-Deploy**: `Yes` (tự động deploy khi push code)

5. **Click "Create Web Service"**

---

### Cách 2: Deploy Với render.yaml (Nhanh Hơn)

1. **Push file render.yaml lên GitHub**

   ```bash
   git add render.yaml
   git commit -m "Add render.yaml configuration"
   git push origin main
   ```

2. **Trên Render Dashboard**
   - Click **"New +"** → **"Blueprint"**
   - Chọn repository của bạn
   - Render sẽ tự động phát hiện `render.yaml`
   - Click **"Apply"**

---

## 🔐 Cấu Hình Environment Variables

Sau khi tạo service, cần thêm các biến môi trường:

### 1. Vào Service Settings

- Dashboard → Your Service → **"Environment"** tab

### 2. Thêm Các Environment Variables Sau:

| Key               | Value                 | Ghi Chú                                   |
| ----------------- | --------------------- | ----------------------------------------- |
| `GEMINI_API_KEY`  | `your_gemini_api_key` | ⚠️ BẮT BUỘC - API key từ Google AI Studio |
| `DATABASE_URL`    | `your_mongodb_url`    | MongoDB connection string                 |
| `REDIS_URL`       | `your_redis_url`      | Redis connection string (nếu có)          |
| `YOUTUBE_API_KEY` | `your_youtube_key`    | YouTube API key (nếu cần)                 |
| `PORT`            | `8000`                | Port mà FastAPI sẽ chạy                   |

### 3. Lấy API Keys

**GEMINI_API_KEY:**

1. Truy cập: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy key và paste vào Render

**MongoDB (DATABASE_URL):**

- Sử dụng MongoDB Atlas miễn phí: https://www.mongodb.com/cloud/atlas
- Format: `mongodb+srv://username:password@cluster.mongodb.net/database`

**Redis (REDIS_URL):**

- Sử dụng Upstash Redis miễn phí: https://upstash.com/
- Hoặc tạo Redis trên Render: New → Redis

### 4. Save Changes

- Click **"Save Changes"**
- Service sẽ tự động redeploy

---

## ⏰ Giữ Service Luôn Hoạt Động

### ⚠️ Vấn Đề với Free Tier

- Render Free tier sẽ **spin down** (tắt) service sau **15 phút không hoạt động**
- Khi có request mới, service sẽ **cold start** (khởi động lại) mất ~30-60 giây

### ✅ Giải Pháp: Auto Ping Service

#### Cách 1: Sử dụng Cron-Job.org (Khuyến Nghị - Miễn Phí)

1. **Truy cập**: https://cron-job.org/
2. **Đăng ký tài khoản miễn phí**
3. **Tạo Cron Job mới:**
   - **Title**: `RCM Recipe Keep Alive`
   - **URL**: `https://your-service.onrender.com/ping`
   - **Schedule**: `Every 5 minutes` hoặc `*/5 * * * *`
   - **Enabled**: ✅ Yes
4. **Save**

#### Cách 2: Sử dụng UptimeRobot (Miễn Phí - 50 monitors)

1. **Truy cập**: https://uptimerobot.com/
2. **Đăng ký tài khoản**
3. **Add New Monitor:**
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `RCM Recipe API`
   - **URL**: `https://your-service.onrender.com/ping`
   - **Monitoring Interval**: `5 minutes`
4. **Create Monitor**

#### Cách 3: Sử dụng GitHub Actions (Cho Developers)

Tạo file `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Alive

on:
  schedule:
    - cron: "*/5 * * * *" # Chạy mỗi 5 phút
  workflow_dispatch: # Cho phép chạy manual

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Service
        run: |
          curl -f https://your-service.onrender.com/ping || exit 1
```

#### Cách 4: Chạy Script Python Trên Máy Local (Development)

File `keep_alive.py` đã được tạo sẵn:

```bash
python keep_alive.py
```

**Chạy nền với nohup (Linux/Mac):**

```bash
nohup python keep_alive.py > keep_alive.log 2>&1 &
```

**Chạy với Task Scheduler (Windows):**

1. Mở Task Scheduler
2. Create Basic Task
3. Trigger: Repeat every 5 minutes
4. Action: Start a program → `python.exe`
5. Arguments: `path\to\keep_alive.py`

---

## ✅ Kiểm Tra Deployment

### 1. Check Service Status

```bash
curl https://your-service.onrender.com/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "RCM Recipe Generator",
  "version": "1.0.0"
}
```

### 2. Test Ping Endpoint

```bash
curl https://your-service.onrender.com/ping
```

**Expected Response:**

```json
{
  "status": "pong",
  "message": "Service is alive",
  "timestamp": "2025-10-25T10:30:00.123456"
}
```

### 3. Check API Documentation

- Truy cập: `https://your-service.onrender.com/docs`
- Sẽ thấy Swagger UI với tất cả endpoints

### 4. Test Recipe Generation

```bash
curl -X POST "https://your-service.onrender.com/api/v1/recipes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": ["chicken", "tomato", "garlic"],
    "dietary_preferences": ["low-carb"]
  }'
```

---

## 🔍 Troubleshooting

### ❌ Service Không Start

**1. Check Logs:**

- Dashboard → Your Service → **"Logs"** tab
- Xem error messages

**2. Common Issues:**

**Error: "Port already in use"**

```yaml
# Trong Dockerfile, đảm bảo sử dụng PORT từ env
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Error: "Module not found"**

```bash
# Check requirements.txt có đầy đủ dependencies
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

**Error: "GEMINI_API_KEY not found"**

- Kiểm tra lại Environment Variables trong Settings
- Đảm bảo đã Save Changes
- Redeploy service

### ❌ Health Check Failed

**Check endpoint response:**

```bash
curl -i https://your-service.onrender.com/health
```

**Expected Status Code:** `200 OK`

**Fix:**

- Đảm bảo `/health` endpoint trả về status code 200
- Check logs để xem lỗi

### ❌ Service Bị Spin Down

**Triệu chứng:**

- First request mất 30-60s để response
- Subsequent requests nhanh

**Giải pháp:**

- Setup auto-ping như hướng dẫn ở trên
- Hoặc nâng cấp lên Paid plan (không bị spin down)

### ❌ 502 Bad Gateway

**Nguyên nhân:**

- Service đang deploy
- Service crashed
- Health check failed nhiều lần

**Giải pháp:**

1. Check Logs
2. Check Environment Variables
3. Redeploy service
4. Contact Render support nếu vẫn lỗi

---

## 📊 Monitoring

### 1. Render Dashboard

- **Metrics**: CPU, Memory usage
- **Logs**: Real-time logs
- **Events**: Deploy history

### 2. Setup Alerts (Paid Plans)

- Email notifications
- Slack integration
- PagerDuty integration

### 3. Custom Monitoring

```python
# Thêm vào app/main.py
from prometheus_client import Counter, Histogram
import time

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_metrics(request, call_next):
    request_count.inc()
    start_time = time.time()
    response = await call_next(request)
    request_duration.observe(time.time() - start_time)
    return response
```

---

## 💰 Cost Optimization

### Free Tier Limits

- ✅ 750 hours/month (đủ cho 1 service chạy 24/7)
- ✅ Auto-deploy from Git
- ✅ Free SSL certificates
- ⚠️ Spin down after 15 mins inactivity
- ⚠️ 100GB bandwidth/month

### Khi Nào Nên Upgrade?

- ❌ Không muốn service bị spin down
- ❌ Cần nhiều hơn 512MB RAM
- ❌ Cần auto-scaling
- ❌ Cần priority support

### Paid Plans (Starting at $7/month)

- ✅ No spin down
- ✅ More resources (RAM, CPU)
- ✅ Auto-scaling
- ✅ Priority support

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com/
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Docker Docs**: https://docs.docker.com/

---

## 📝 Checklist Trước Khi Deploy

- [ ] Code đã commit và push lên GitHub
- [ ] `render.yaml` đã được tạo
- [ ] `Dockerfile` hoạt động đúng
- [ ] `requirements.txt` đầy đủ dependencies
- [ ] Đã có GEMINI_API_KEY
- [ ] Đã có MongoDB connection (nếu cần)
- [ ] `/health` endpoint hoạt động
- [ ] `/ping` endpoint hoạt động
- [ ] Đã setup auto-ping service
- [ ] Đã test locally với Docker

---

## 🎉 Chúc Mừng!

Service của bạn đã sẵn sàng deploy lên Render! 🚀

**Questions?** Check [Render Community](https://community.render.com/) hoặc [FastAPI Discussions](https://github.com/fastapi/fastapi/discussions)
