# Model Ministry Routing

هذه الوثيقة تحدد توزيع الموديلات على وزارات الدولة الرقمية بدون الاعتماد على fallback عام.

## No fallback-by-default

كل وزارة لها موديل محدد. إذا فشل موديل وزارة أثناء الاختبار، نسجل أن الوزارة فشلت أو أصبحت غير جاهزة، ولا نستبدله تلقائياً بموديل آخر.

الهدف ليس أن “أي موديل يرد بدلاً من الآخر”، بل أن نعرف صحة كل وزارة وموديلها بدقة قبل إطلاق GitHub.

## القاعدة الأساسية

كل وزارة لها موديل محدد:

- Strategy Ministry: `openai-codex:gpt-5.5`
- Operations Ministry: `nvidia:meta/llama-4-maverick-17b-128e-instruct`
- Signals Ministry: `nvidia:mistralai/mistral-large-3-675b-instruct-2512`
- Audit Office: `nvidia:z-ai/glm-5.1`
- Governance Office: `nvidia:deepseek-ai/deepseek-v4-flash`
- Citizen Services: `nvidia:minimaxai/minimax-m2.7`
- Research and Space Planning: `nvidia:moonshotai/kimi-k2.6`

## الموديل غير الجاهز

`deepseek-ai/deepseek-v4-pro` ليس مخصصاً لأي وزارة في أول إطلاق لأنه فشل في فحوصات pre-GitHub السابقة حتى مع timeout طويل.

لا يتم حذفه من المعرفة بالنظام، لكنه يبقى reserve/not_launch_ready حتى يجتاز اختبار readiness مستقل.

## طريقة الاختبار قبل GitHub

قبل إطلاق التوزيعة:

1. نرسل prompt قصير مناسب لكل وزارة إلى موديلها المحدد.
2. نسجل `returned` أو `timeout_or_error` لكل وزارة.
3. لا نستخدم fallback أو substitution.
4. إذا فشلت وزارة launch-critical، لا نطلق إصدار stable.
5. إذا فشلت وزارة غير حرجة، إما نؤجلها أو نطلقها كـ experimental بشرط توثيق ذلك.

## لماذا هذا أفضل من fallback؟

fallback مفيد للشات العام، لكنه يخفي فشل وزارة معينة. نظام الدولة الرقمية يحتاج شفافية: إذا وزارة audit بطيئة أو وزارة governance فشلت، يجب أن نعرف ذلك لا أن يخفيه موديل آخر.

## مصدر الحقيقة

العقد القابل للتحقق موجود هنا:

`specs/003-portable-digital-state-distribution/fixtures/model-ministry-routing.json`

والـ schema هنا:

`specs/003-portable-digital-state-distribution/schemas/model-ministry-routing-v1.json`
