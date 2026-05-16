# دليل تشغيل Hermes Agent + Hermes Workspace

هذا الدليل خاص بمشروع Hermes المستقل داخل:

- Hermes Agent: `/mnt/d/GOCOLEX/hermes-agent`
- Hermes Workspace: `/mnt/d/GOCOLEX/hermes-workspace`

> ملاحظة مهمة: إذا كنت داخل WSL وتظهر لك صيغة مثل `seo@DESKTOP...` فلا تكتب `wsl -d Ubuntu`. هذا الأمر يستخدم من PowerShell فقط.

## 1. المنافذ المستخدمة

| الخدمة | المنفذ | رابط الفحص |
|---|---:|---|
| Hermes API Gateway | `8642` | `http://127.0.0.1:8642/health` |
| Hermes Dashboard | `9120` | `http://127.0.0.1:9120` |
| Hermes Workspace | `3001` | `http://localhost:3001` |

استخدم `3001` بدل `3000` لتجنب جلسات Vite القديمة أو العالقة.

## 2. أمر الفحص الصحيح

لا تكتب:

```bash
url http://127.0.0.1:8642/health
```

الأمر الصحيح هو:

```bash
curl http://127.0.0.1:8642/health
```

النتيجة الصحيحة:

```json
{"status": "ok", "platform": "hermes-agent"}
```

## 3. تثبيت إعداد الموديل الصحيح

قبل تشغيل Gateway، تأكد أن Hermes لا يستخدم `OpenRouter/hermes-agent` بالخطأ.

داخل WSL:

```bash
cd /mnt/d/GOCOLEX/hermes-agent

.venv-wsl/bin/hermes config set model digital-state
.venv-wsl/bin/hermes config set provider openai-codex
```

تحقق:

```bash
.venv-wsl/bin/hermes status | sed -n '/◆ Environment/,/◆ API Keys/p'
```

المفروض يظهر:

```text
Model:        digital-state
Provider:     OpenAI Codex
```

## 4. تشغيل Hermes API Gateway

افتح Terminal 1 داخل WSL:

```bash
cd /mnt/d/GOCOLEX/hermes-agent

API_SERVER_ENABLED=true \
API_SERVER_HOST=127.0.0.1 \
API_SERVER_PORT=8642 \
API_SERVER_MODEL_NAME=digital-state \
.venv-wsl/bin/hermes gateway run
```

اترك هذه النافذة مفتوحة.

تحذير `No API key configured` مقبول في التشغيل المحلي فقط.

## 5. اختبار Gateway

افتح Terminal 2 داخل WSL:

```bash
curl http://127.0.0.1:8642/health
```

ثم اختبر قائمة الموديلات:

```bash
curl http://127.0.0.1:8642/v1/models
```

يجب أن يظهر `digital-state` وليس `hermes-agent`.

اختبار الشات المباشر:

```bash
curl -sS http://127.0.0.1:8642/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"digital-state","messages":[{"role":"user","content":"say exactly OK"}],"stream":false}'
```

الرد الصحيح يحتوي على:

```text
OK
```

## 6. تشغيل Hermes Dashboard اختياريًا

افتح Terminal آخر داخل WSL:

```bash
cd /mnt/d/GOCOLEX/hermes-agent

.venv-wsl/bin/hermes dashboard --skip-build --tui --no-open --host 127.0.0.1 --port 9120
```

افتح:

```text
http://127.0.0.1:9120
```

للشات داخل Dashboard:

```text
http://127.0.0.1:9120/chat
```

إذا استخدمت `curl -I http://127.0.0.1:9120` وظهر `405 Method Not Allowed` فهذا طبيعي لأن Dashboard لا يقبل `HEAD`. استخدم `GET` بدلًا منه:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9120
```

## 7. ضبط Hermes Workspace

افتح Terminal جديد داخل WSL:

```bash
cd /mnt/d/GOCOLEX/hermes-workspace

sed -i '/^CLAUDE_AGENT_PATH=/d' .env
sed -i '/^CLAUDE_API_URL=/d' .env
sed -i '/^HERMES_API_URL=/d' .env
sed -i '/^HERMES_DASHBOARD_URL=/d' .env
sed -i '/^CLAUDE_DEFAULT_MODEL=/d' .env
sed -i '/^HERMES_DEFAULT_MODEL=/d' .env

printf '\nCLAUDE_API_URL=http://127.0.0.1:8642\n' >> .env
printf 'HERMES_API_URL=http://127.0.0.1:8642\n' >> .env
printf 'HERMES_DASHBOARD_URL=http://127.0.0.1:9120\n' >> .env
printf 'CLAUDE_DEFAULT_MODEL=digital-state\n' >> .env
printf 'HERMES_DEFAULT_MODEL=digital-state\n' >> .env
```

لا تضف `CLAUDE_AGENT_PATH` هنا. مع نسخة Hermes الحالية قد يجعل Workspace يبحث عن مجلد `webapi` غير موجود ويظهر خطأ `hermes-agent not found`.

## 8. تشغيل Hermes Workspace

شغل Workspace على `3001`:

```bash
cd /mnt/d/GOCOLEX/hermes-workspace

pnpm exec vite --host 0.0.0.0 --port 3001
```

افتح:

```text
http://localhost:3001/chat/new
```

إذا ظهر اختيار موديل، اختر:

```text
digital-state
```

ابدأ برسالة اختبار قصيرة:

```text
Reply only OK. Do not use tools.
```

## 9. تشغيل كامل من الصفر

افتح نافذتين أو ثلاث داخل WSL.

### Terminal 1: Gateway

```bash
cd /mnt/d/GOCOLEX/hermes-agent

.venv-wsl/bin/hermes config set model digital-state
.venv-wsl/bin/hermes config set provider openai-codex

API_SERVER_ENABLED=true \
API_SERVER_HOST=127.0.0.1 \
API_SERVER_PORT=8642 \
API_SERVER_MODEL_NAME=digital-state \
.venv-wsl/bin/hermes gateway run
```

### Terminal 2: Workspace

```bash
cd /mnt/d/GOCOLEX/hermes-workspace

pnpm exec vite --host 0.0.0.0 --port 3001
```

### Terminal 3: Dashboard اختياري

```bash
cd /mnt/d/GOCOLEX/hermes-agent

.venv-wsl/bin/hermes dashboard --skip-build --tui --no-open --host 127.0.0.1 --port 9120
```

## 10. فحص سريع

```bash
curl http://127.0.0.1:8642/health
curl http://127.0.0.1:8642/v1/models
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3001
```

المتوقع:

- health يرجع `ok`
- models يحتوي `digital-state`
- Workspace يرجع `200`

## 11. أخطاء شائعة

### `Command 'url' not found`

استخدم `curl` وليس `url`.

### `hermes-agent not found`

احذف `CLAUDE_AGENT_PATH` من `.env`:

```bash
cd /mnt/d/GOCOLEX/hermes-workspace
sed -i '/^CLAUDE_AGENT_PATH=/d' .env
```

ثم شغل Workspace من جديد.

### `The 'hermes-agent' model is not supported when using Codex`

هذا يعني أن الطلب يستخدم موديل خطأ. نفذ:

```bash
cd /mnt/d/GOCOLEX/hermes-agent
.venv-wsl/bin/hermes config set model digital-state
.venv-wsl/bin/hermes config set provider openai-codex
```

ثم أعد تشغيل Gateway.

### Workspace لا يرد أو يبدو متوقفًا

افتح محادثة جديدة جدًا:

```text
http://localhost:3001/chat/new
```

ثم أرسل:

```text
Reply only OK. Do not use tools.
```

إذا أرسلت سياق مشروع كبير، Hermes قد يستخدم أدوات مثل `read_file`, `search_files`, `terminal` وقد يستغرق عدة دقائق.

### `mode=portable`

هذا طبيعي. يعني أن الشات الأساسي يعمل عبر Gateway، لكن بعض مزايا Dashboard المتقدمة غير متاحة.

## 12. قاعدة التشغيل

لا تغلق نوافذ التشغيل:

- نافذة Gateway يجب أن تبقى مفتوحة.
- نافذة Workspace يجب أن تبقى مفتوحة.
- نافذة Dashboard اختيارية، لكنها يجب أن تبقى مفتوحة إذا أردت `/chat` الخاص بالـ Dashboard.
## 13. الموديلات المطلوبة فقط

القائمة التي نريد اعتمادها يدويًا هي:

| الدور | الموديل | المزود | ملاحظات |
|---|---|---|---|
| الأساسي | `digital-state` | `openai-codex` | الافتراضي للشات والتشغيل اليومي |
| مساعد/ضغط | `glm-5.1` | `nvidia` | مناسب كـ auxiliary/compression أو مراجعات مساعدة |
| اختياري | `kimi-k2.6` | `nvidia` | يستخدم فقط عند اختياره صراحة |
| اختياري | `llama-4-maverick-17b-128e-instruct` | `nvidia` | اسم llama maverick الكامل |

لا تستخدم هذه الأسماء كموديل أساسي مع `openai-codex`:

```text
hermes-agent
glm5
z-aiglm5
llama-3.1-8b-instruct
llama-3.3-70b-instruct
```

مهم: Hermes API Gateway الحالي يعلن موديلًا واحدًا فقط عبر:

```bash
curl http://127.0.0.1:8642/v1/models
```

لذلك اجعله يعلن `digital-state` فقط عند تشغيل Workspace:

```bash
API_SERVER_MODEL_NAME=digital-state
```

أما صفحة Dashboard `/models` فقد تعرض موديلات قديمة من history/usage، وهذا لا يعني أنها مفعلة أو مسموحة حاليًا. المرجع الحقيقي للشات هو `/v1/models` واختيار الموديل داخل Workspace.
