<section align="center">
    <img src="https://invites.fun/assets/logo-uc19cs8i.png" alt="" width="210" />
</section>

<h2 align="center">邀玩（药丸）签到助手</h2>

## 如何使用
### 安装所需python库
```python
pip install requests
```
### 获取网站cookie
访问`hhttps://invites.fun/`
首页`F12`打开调试工具,在请求标头中找到并复制cookie的值，将`flarum_remember`与`flarum_session`值填入json

### 运行`main.py`

若签到成功，程序会输出类似如下的信息
```bash
💊签到成功，连续签到次数：2，药丸数量：443
```
## TODO
- [ ] 使用github actions 部署
- [ ] 集成到MP，Nastools等软件中