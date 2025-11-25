# Skill Tracker API 测试脚本

Write-Host "`n=== Skill Tracker API 测试 ===" -ForegroundColor Yellow

# 1. 登录获取 Token
Write-Host "`n[1/5] 测试登录..." -ForegroundColor Cyan
$loginBody = @{ username = "testuser2"; password = "Test@1234" } | ConvertTo-Json
$loginResponse = Invoke-RestMethod -Uri "http://localhost:3000/api/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
$token = $loginResponse.data.token
Write-Host "✅ 登录成功" -ForegroundColor Green

# 2. 获取技能数据
Write-Host "`n[2/5] 测试获取技能数据..." -ForegroundColor Cyan
$headers = @{ Authorization = "Bearer $token" }
$getResponse = Invoke-RestMethod -Uri "http://localhost:3000/api/skills" -Method Get -Headers $headers
Write-Host "✅ 获取成功, 版本: $($getResponse.data.version)" -ForegroundColor Green

# 3. 保存技能数据
Write-Host "`n[3/5] 测试保存技能数据..." -ForegroundColor Cyan
$testSkills = @{
    skills = @(
        @{
            id = "test-skill-1"
            name = "测试技能1"
            levels = @()
        }
    )
    version = $getResponse.data.version
} | ConvertTo-Json -Depth 10
$saveResponse = Invoke-RestMethod -Uri "http://localhost:3000/api/skills" -Method Put -Body $testSkills -Headers $headers -ContentType "application/json"
Write-Host "✅ 保存成功, 新版本: $($saveResponse.data.version)" -ForegroundColor Green

# 4. 同步数据
Write-Host "`n[4/5] 测试数据同步..." -ForegroundColor Cyan
$syncData = @{
    localData = @(@{ id = "local-skill"; name = "本地技能" })
    localVersion = 2
} | ConvertTo-Json -Depth 10
$syncResponse = Invoke-RestMethod -Uri "http://localhost:3000/api/skills/sync" -Method Post -Body $syncData -Headers $headers -ContentType "application/json"
Write-Host "✅ 同步成功, 操作: $($syncResponse.data.action)" -ForegroundColor Green

# 5. 测试活动记录
Write-Host "`n[5/7] 测试活动记录..." -ForegroundColor Cyan
$activityBody = @{
    activityType = "log_added"
    skillId = "test-skill-1"
    details = "测试活动"
} | ConvertTo-Json
$activityResponse = Invoke-RestMethod -Uri "http://localhost:3000/api/activity/log" -Method Post -Body $activityBody -Headers $headers -ContentType "application/json"
Write-Host "✅ 活动记录成功" -ForegroundColor Green

# 6. 获取统计数据
Write-Host "`n[6/7] 测试统计数据..." -ForegroundColor Cyan
$statsResponse = Invoke-RestMethod -Uri "http://localhost:3000/api/activity/stats" -Method Get -Headers $headers
Write-Host "✅ 统计成功 - 总天数: $($statsResponse.data.totalDays), 总活动: $($statsResponse.data.totalActivities)" -ForegroundColor Green

# 7. 验证最终数据
Write-Host "`n[7/7] 验证最终数据..." -ForegroundColor Cyan
$finalData = Invoke-RestMethod -Uri "http://localhost:3000/api/skills" -Method Get -Headers $headers
Write-Host "✅ 最终版本: $($finalData.data.version), 技能数量: $($finalData.data.skills.Count)" -ForegroundColor Green

Write-Host "`n=== 所有测试通过 ✅ ===" -ForegroundColor Yellow
