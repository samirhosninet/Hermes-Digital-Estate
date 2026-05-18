# دليل تشغيل الدولة الرقمية Hermes Digital State

هذا الدليل يشرح طريقة تشغيل **Hermes Digital State** كحزمة حوكمة محمولة فوق Hermes Agent الرسمي. الدولة الرقمية ليست محركا بديلا، ولا fork من Hermes، ولا واجهة مستقلة. هي **Hermes Profile Distribution** تحتوي وثائق حوكمة، مهارات، مواصفات Spec Kit، أدوات فحص، ومعالج إعداد محلي للمستخدم غير التقني.

القاعدة الصارمة: أسرارك وملفات الجلسات والذاكرة والسجلات تبقى محلية على جهازك، ولا تدخل في المستودع أو حزمة التوزيع.

## 1. المسار الرسمي للتثبيت

ابدأ بتثبيت Hermes Agent الرسمي من مصدره المعتمد. بعد ذلك ثبت الدولة الرقمية كملف تعريف Profile Distribution:

```bash
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate --alias
```

هذا هو مصدر GitHub الرسمي المعتمد للحزمة. لا تستبدله بمسار محلي في تعليمات الإنتاج.

بعد التثبيت:

```bash
hermes profile show digital-state
hermes -p digital-state config check
```

للتشغيل:

```bash
hermes -p digital-state chat
```

## 2. مسار Windows للمستخدم غير التقني

على جهاز Windows جديد، ابدأ من PowerShell بهذا الأمر:

```powershell
irm https://raw.githubusercontent.com/samirhosninet/Hermes-Digital-Estate/refs/heads/main/scripts/bootstrap/install-windows.ps1 | iex
```

هذا الأمر يحمل حزمة bootstrap الخاصة بالدولة الرقمية إلى مجلد محلي، ثم يفتح واجهة **Install Digital State Stack**. البداية تكون بتثبيت Hermes Agent الرسمي أولا. مثبت Hermes الرسمي هو المسؤول عن توفير Python وNode.js 22 وPortableGit؛ لا تطلب من المستخدم تثبيت هذه الأدوات يدويا قبل Hermes.

المسار اليدوي البديل: حمل ZIP من GitHub، فك الضغط، ثم شغل:

```bat
START.bat
```

الواجهة تفحص وتثبت بالترتيب:

- Hermes Agent
- Hermes Workspace
- Digital State profile

إذا فشل أي جزء، لا يتم إخفاء الفشل. تظهر المشكلة، سببها، الأمر اليدوي البديل، ومسار log كامل.

تنبيه مهم: Hermes Native Windows مدعوم، لكن تبويب dashboard الطرفي المدمج `/chat` يحتاج WSL2 حسب وثائق Hermes. لا تعرض هذه الحزمة وعدا بأن هذا التبويب يعمل كاملا على Windows Native.

## 3. معالج الإعداد داخل الحزمة

إذا كان لديك نسخة محلية من حزمة الدولة الرقمية، يمكن تشغيل معالج الإعداد المحلي:

```bash
python wizard.py
```

على Windows يمكن استخدام:

```bat
START.bat
```

وعلى macOS أو Linux أو بيئة Bash صالحة:

```bash
bash START.sh
```

المعالج يفتح متصفحا محليا على `127.0.0.1`، ويبدأ عادة من المنفذ `8484` أو أول منفذ متاح بعده. هذا المعالج أداة onboarding وتشخيص فقط. لا يستبدل تثبيت Profile Distribution ولا يغير Hermes core.

## 4. إعداد الأسرار محليا

لا تضع مفاتيح API داخل Git أو داخل الوثائق. استخدم ملف `.env` محليا فقط، اعتمادا على `.env.EXAMPLE`.

أسماء المتغيرات المتوقعة:

```text
NVIDIA_API_KEY
OPENROUTER_API_KEY
ANTHROPIC_API_KEY
VOICE_TOOLS_OPENAI_KEY
```

لا تنشر ملف `.env`. لا تضف auth files أو sessions أو logs أو memory إلى أي release.

## 5. بناء Staging Distribution محلي

قبل النشر إلى GitHub، ابن نسخة staging صغيرة من الملفات المسموح بها فقط في `digital-state.manifest.json`.

مثال عام:

```bash
python scripts/governance/build_staging_distribution.py --output <STAGING_DIR> --json
```

اختر `<STAGING_DIR>` خارج مجلد المصدر، ويجب أن يكون فارغا. لا تستخدم مجلدا داخل المستودع.

بعد البناء، شغل الفحص من داخل حزمة staging:

```bash
python scripts/governance/bootstrap_digital_state.py --json
python scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening scripts/bootstrap scripts/governance wizard.py preflight START.bat START.sh
```

إذا كان Hermes CLI متاحا ومسموحا له بتعديل حالة Hermes المحلية، اختبر الحزمة كملف تعريف مؤقت:

```bash
hermes profile install <STAGING_DIR> --name digital-state-test -y
hermes profile show digital-state-test
hermes -p digital-state-test config check
hermes profile delete digital-state-test -y
```

إذا لم تكن الصلاحيات متاحة، وثق أن اختبار profile install مؤجل، ولا تعتبر ذلك نجاحا كاملا للنشر.

## 6. فحوصات الجودة قبل النشر

من مجلد المصدر المحلي للدولة الرقمية:

```bash
python -m unittest tests.scripts.test_staging_distribution tests.scripts.test_digital_state_distribution tests.scripts.test_preflight
python audit.py
python scripts/governance/bootstrap_digital_state.py --json
python scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening scripts/bootstrap scripts/governance wizard.py preflight START.bat START.sh tests/scripts tests/fixtures
```

لا تنشر إذا ظهر أي فشل في audit أو bootstrap أو portability.

## 7. التحديث والرجوع

تحديث Hermes Agent يتم عبر مسار Hermes الرسمي. تحديث الدولة الرقمية يتم عبر ملف التعريف:

```bash
hermes profile update digital-state
```

بعد أي تحديث:

```bash
hermes -p digital-state config check
python scripts/governance/bootstrap_digital_state.py --json
```

الرجوع لإصدار سابق يجب أن يستخدم tag معروفا في GitHub، لا تعديلا يدويا داخل Hermes core.

## 8. حدود مهمة

- لا تعدل Hermes core ضمن تشغيل الدولة الرقمية.
- لا تنشر مفاتيح API أو OAuth tokens أو auth stores أو sessions أو logs أو memory.
- لا تعتبر وجود الوثائق شهادة امتثال أو اعتمادا حكوميا أو جاهزية مهمة حرجة.
- Runtime governance يبقى مشروطا بموافقات واختبارات منفصلة، وليس مفعلا تلقائيا.
- مصدر الحقيقة التقني هو ملفات `digital-state.manifest.json` و`distribution.yaml` وSpec Kit، وهذا الدليل يشرح التشغيل فقط.

## 9. حكم التشغيل

النسخة الجاهزة للنشر هي التي تمر بهذه الشروط:

- staging distribution مبني من manifest فقط.
- bootstrap داخل staging ينجح.
- portability داخل staging ينجح.
- لا توجد أسرار أو مسارات جهاز داخل الحزمة.
- profile install المؤقت نجح، أو تم توثيق سبب عدم تنفيذه بوضوح.

غير ذلك ليس release جاهزا، حتى لو عمل محليا على جهاز المطور.
