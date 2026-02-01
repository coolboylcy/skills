---
name: spool
description: "Threads CLI - Read, post, reply, and search on Meta's Threads using OpenClaw browser tool. Use when the user wants to interact with Threads: posting, reading timeline, viewing profiles, replying to threads, or searching."
homepage: https://github.com/zizi-cat/spool
metadata: {"clawdhub":{"emoji":"🧵"}}
---

# spool

OpenClaw browser 도구로 Threads (threads.net) 조작하기.

## Prerequisites

### 1. Xvfb (가상 디스플레이) 설치 - headless 서버용

GUI 없는 서버에서 browser 도구를 사용하려면 Xvfb가 필요:

```bash
# Xvfb 설치
sudo apt install -y xvfb

# systemd 서비스로 등록
sudo tee /etc/systemd/system/xvfb.service << 'EOF'
[Unit]
Description=X Virtual Frame Buffer
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable xvfb
sudo systemctl start xvfb
```

### 2. OpenClaw Gateway에 DISPLAY 환경변수 추가

```bash
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
echo '[Service]
Environment=DISPLAY=:99' > ~/.config/systemd/user/openclaw-gateway.service.d/display.conf

systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

### 3. Threads 로그인

```
browser action=start profile=openclaw
browser action=open profile=openclaw targetUrl="https://www.threads.net/login"
```
수동으로 로그인 후 세션 유지됨.

## Commands

### 로그인 확인 (whoami)

```
browser action=open profile=openclaw targetUrl="https://www.threads.net"
browser action=snapshot profile=openclaw compact=true
```
→ Profile 링크에서 `/@username` 확인

### 타임라인 읽기

```
browser action=open profile=openclaw targetUrl="https://www.threads.net"
browser action=snapshot profile=openclaw compact=true
```

### 프로필 읽기

```
browser action=open profile=openclaw targetUrl="https://www.threads.net/@username"
browser action=snapshot profile=openclaw compact=true
```

### 포스팅

1. 새 글 영역 클릭:
```
browser action=snapshot profile=openclaw compact=true
# "What's new?" 또는 "Empty text field" 버튼 찾기
browser action=act profile=openclaw request={"kind":"click","ref":"<버튼ref>"}
```

2. 다이얼로그에서 텍스트 입력:
```
browser action=snapshot profile=openclaw compact=true
# textbox ref 찾기
browser action=act profile=openclaw request={"kind":"type","ref":"<textbox-ref>","text":"내용"}
```

3. 게시:
```
browser action=act profile=openclaw request={"kind":"click","ref":"<Post버튼ref>"}
```

4. 확인:
```
browser action=snapshot profile=openclaw compact=true
# "Posted" + "View" 링크 확인
```

### 답글 달기

1. 스레드 열기:
```
browser action=open profile=openclaw targetUrl="https://www.threads.net/@user/post/XXXXX"
browser action=snapshot profile=openclaw compact=true
```

2. Reply 버튼 클릭 → 텍스트 입력 → Post

### 검색

```
browser action=open profile=openclaw targetUrl="https://www.threads.net/search?q=검색어"
browser action=snapshot profile=openclaw compact=true
```

## Tips

- `compact=true`로 스냅샷 찍으면 토큰 절약
- 포스팅 전 **반드시 사용자 확인** 받을 것
- ref는 snapshot마다 달라지니까 항상 새로 찾기
- `targetId` 유지하면 같은 탭에서 계속 작업 가능

## Troubleshooting

### browser 도구 안 됨
1. Xvfb 실행 중인지 확인: `systemctl status xvfb`
2. DISPLAY 환경변수 확인: Gateway 서비스에 `Environment=DISPLAY=:99` 있는지
3. Gateway 재시작: `systemctl --user restart openclaw-gateway`

### 로그인 풀림
1. `browser action=open profile=openclaw targetUrl="https://www.threads.net/login"`
2. 수동 로그인 또는 사용자에게 요청

### 요소 못 찾음
- snapshot 다시 찍고 ref 확인
- Threads UI 업데이트됐을 수 있음
