# 🚀 Render Deployment Checklist

## Pre-Deployment Checklist ✅

### Code Preparation

- [ ] All code committed to Git
- [ ] All tests passing locally
- [ ] Docker build successful locally
- [ ] Environment variables documented
- [ ] Sensitive data removed from code
- [ ] .env file in .gitignore
- [ ] Dependencies updated in requirements.txt

### Configuration Files

- [ ] `render.yaml` created and configured
- [ ] `Dockerfile` optimized for production
- [ ] `.dockerignore` includes unnecessary files
- [ ] `.env.example` documented all variables
- [ ] Health check endpoint (`/health`) working
- [ ] Keep-alive endpoint (`/ping`) working

### Documentation

- [ ] README.md updated with deployment info
- [ ] API documentation complete
- [ ] Environment variables documented
- [ ] Deployment guides created

---

## Deployment Steps 🌐

### Step 1: Prepare Repository

```powershell
# Make sure everything is committed
git status

# Add all changes
git add .

# Commit with meaningful message
git commit -m "Ready for Render deployment with keep-alive endpoints"

# Push to GitHub
git push origin main
```

- [ ] Code pushed to GitHub

### Step 2: Create Render Account

1. Go to https://dashboard.render.com/
2. Sign up (free account)
3. Verify email

- [ ] Render account created

### Step 3: Create Web Service

1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub account
4. Authorize Render to access repositories

- [ ] Repository connected

### Step 4: Configure Service

**Basic Settings:**

- [ ] Name: `rcm-recipe-api` (or your choice)
- [ ] Region: Singapore (or closest to users)
- [ ] Branch: `main`
- [ ] Root Directory: (leave empty)

**Build Settings:**

- [ ] Runtime: Docker
- [ ] Dockerfile Path: `./Dockerfile`
- [ ] Docker Context: `.`
- [ ] Docker Command: (leave empty, using CMD from Dockerfile)

**Instance Settings:**

- [ ] Instance Type: Free (or select paid plan)
- [ ] Auto-Deploy: Yes

**Advanced Settings:**

- [ ] Health Check Path: `/health`
- [ ] Health Check Interval: 30s
- [ ] Health Check Timeout: 10s

### Step 5: Environment Variables

Add these in the "Environment" tab:

**Required:**

- [ ] `GEMINI_API_KEY` = (your Gemini API key)

**Recommended:**

- [ ] `DATABASE_URL` = (MongoDB connection string)
- [ ] `REDIS_URL` = (Redis connection string)

**Optional:**

- [ ] `YOUTUBE_API_KEY` = (YouTube API key)
- [ ] `LOG_LEVEL` = INFO
- [ ] `ENVIRONMENT` = production

**Auto-set by Render:**

- [ ] `PORT` = (automatically set)

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait for initial build (5-10 minutes)
3. Watch logs for errors

- [ ] First deployment successful
- [ ] Service is live

---

## Post-Deployment Checklist 🎯

### Step 7: Verify Deployment

**Test Root Endpoint:**

```bash
curl https://your-service.onrender.com/
```

- [ ] Returns service info

**Test Health Endpoint:**

```bash
curl https://your-service.onrender.com/health
```

- [ ] Returns `{"status": "healthy"}`

**Test Ping Endpoint:**

```bash
curl https://your-service.onrender.com/ping
```

- [ ] Returns `{"status": "pong"}`

**Test API Documentation:**

- [ ] Visit `https://your-service.onrender.com/docs`
- [ ] Swagger UI loads correctly

**Test Main API:**

```bash
curl -X POST "https://your-service.onrender.com/api/v1/recipes/generate" \
  -H "Content-Type: application/json" \
  -d '{"ingredients": ["chicken", "tomato"]}'
```

- [ ] Recipe generation works

### Step 8: Setup Keep-Alive Service

Choose ONE method:

**Option A: Cron-Job.org (Recommended)**

1. Go to https://cron-job.org/
2. Create free account
3. Add new cronjob:
   - Title: RCM Recipe Keep Alive
   - URL: `https://your-service.onrender.com/ping`
   - Schedule: Every 5 minutes
4. Enable and save

- [ ] Cron-Job.org configured

**Option B: UptimeRobot**

1. Go to https://uptimerobot.com/
2. Create free account (50 monitors)
3. Add new monitor:
   - Type: HTTP(s)
   - Name: RCM Recipe API
   - URL: `https://your-service.onrender.com/ping`
   - Interval: 5 minutes
4. Create monitor

- [ ] UptimeRobot configured

**Option C: GitHub Actions**

1. Copy `.github/workflows/keep-alive.yml` to your repo
2. Push to GitHub
3. Go to repo Settings → Secrets → Actions
4. Add secret: `RENDER_SERVICE_URL` = your service URL
5. Enable Actions in repo settings

- [ ] GitHub Actions configured

### Step 9: Configure Monitoring & Alerts

**Render Dashboard:**

- [ ] Check Metrics tab (CPU, Memory usage)
- [ ] Review Logs tab
- [ ] Set up log alerts (if on paid plan)

**External Monitoring:**

- [ ] UptimeRobot alerts configured
- [ ] Email notifications enabled
- [ ] Slack integration (optional)

### Step 10: DNS & Custom Domain (Optional)

If you have a custom domain:

1. Go to service Settings → Custom Domains
2. Add your domain
3. Update DNS records as instructed
4. Wait for SSL certificate provisioning

- [ ] Custom domain configured
- [ ] SSL certificate active

---

## Security Checklist 🔒

### Environment Security

- [ ] No sensitive data in code
- [ ] All API keys in environment variables
- [ ] DEBUG mode disabled in production
- [ ] Strong SECRET_KEY generated
- [ ] CORS configured correctly (not "\*" in production)

### API Security

- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (if using SQL)
- [ ] XSS protection enabled

### Infrastructure Security

- [ ] HTTPS enforced (automatic on Render)
- [ ] Health check endpoint is public (OK)
- [ ] Admin endpoints protected (if any)
- [ ] Logs don't contain sensitive data

---

## Performance Checklist ⚡

### Optimization

- [ ] Docker image optimized (.dockerignore used)
- [ ] Unused dependencies removed
- [ ] Caching enabled (Redis if available)
- [ ] Database queries optimized
- [ ] Static files served efficiently

### Monitoring

- [ ] Response times monitored
- [ ] Error rates tracked
- [ ] Resource usage acceptable
- [ ] No memory leaks detected

---

## Maintenance Checklist 🔧

### Regular Tasks

- [ ] Check logs weekly
- [ ] Monitor error rates
- [ ] Review resource usage
- [ ] Update dependencies monthly
- [ ] Backup database (if using)

### Monthly Review

- [ ] Check free tier usage (750 hours)
- [ ] Review bandwidth usage (100GB limit)
- [ ] Assess need for paid plan
- [ ] Review and optimize costs

---

## Troubleshooting Checklist 🆘

### If Deployment Fails

- [ ] Check build logs in Render dashboard
- [ ] Verify Dockerfile syntax
- [ ] Test Docker build locally
- [ ] Check all dependencies in requirements.txt
- [ ] Verify environment variables are set

### If Health Check Fails

- [ ] Check `/health` endpoint exists
- [ ] Verify port binding (use $PORT)
- [ ] Check application logs
- [ ] Test endpoint locally
- [ ] Verify timeout settings

### If Service Spins Down

- [ ] Verify keep-alive service is running
- [ ] Check cron-job execution logs
- [ ] Verify ping endpoint responds
- [ ] Consider upgrading to paid plan

### If API Errors Occur

- [ ] Check application logs
- [ ] Verify environment variables
- [ ] Test endpoints with curl
- [ ] Check database connection
- [ ] Verify API keys are valid

---

## Rollback Plan 🔄

### If Deployment Issues Occur

**Immediate Rollback:**

1. Go to Render Dashboard
2. Select your service
3. Go to "Events" tab
4. Find previous successful deployment
5. Click "Rollback to this version"

- [ ] Rollback procedure documented

**Fix and Redeploy:**

1. Fix issues locally
2. Test thoroughly
3. Commit and push
4. Monitor deployment
5. Verify functionality

- [ ] Fix and redeploy procedure tested

---

## Success Criteria ✨

Your deployment is successful when:

- ✅ Service is accessible via HTTPS
- ✅ All endpoints respond correctly
- ✅ Health check passes
- ✅ Keep-alive service running
- ✅ No errors in logs
- ✅ API documentation accessible
- ✅ Recipe generation works
- ✅ Response times acceptable
- ✅ Monitoring configured
- ✅ Alerts working

---

## Next Steps After Deployment 🎯

### Immediate (Week 1)

- [ ] Monitor logs daily
- [ ] Test all features thoroughly
- [ ] Share API with initial users
- [ ] Gather feedback
- [ ] Fix any issues

### Short Term (Month 1)

- [ ] Add more features
- [ ] Optimize performance
- [ ] Improve documentation
- [ ] Setup analytics
- [ ] Consider custom domain

### Long Term (3+ Months)

- [ ] Scale based on usage
- [ ] Add new integrations
- [ ] Implement CI/CD pipeline
- [ ] Add automated testing
- [ ] Plan for growth

---

## Resources 📚

**Essential Links:**

- [ ] Render Dashboard: https://dashboard.render.com/
- [ ] Service URL: https://your-service.onrender.com
- [ ] API Docs: https://your-service.onrender.com/docs
- [ ] GitHub Repo: (your repo URL)

**Documentation:**

- [ ] Render Docs: https://render.com/docs
- [ ] FastAPI Docs: https://fastapi.tiangolo.com/
- [ ] Project README: `README.md`
- [ ] Deployment Guide: `RENDER_DEPLOYMENT_GUIDE.md`
- [ ] Quick Start: `QUICK_START.md`

**Support:**

- [ ] Render Community: https://community.render.com/
- [ ] FastAPI Discussions: https://github.com/fastapi/fastapi/discussions
- [ ] Stack Overflow: Tag questions with `render` and `fastapi`

---

## 🎉 Congratulations!

If all items are checked, your deployment is complete and production-ready!

**Date Completed:** ********\_********

**Deployed By:** ********\_********

**Service URL:** ********\_********

**Notes:**

---

---

---

---

**Keep this checklist for future deployments and maintenance!** 📋
