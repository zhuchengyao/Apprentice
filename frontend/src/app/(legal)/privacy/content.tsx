"use client";

import { useLocale } from "next-intl";
import { LegalHero } from "@/components/legal/legal-hero";

const EFFECTIVE_DATE_EN = "April 15, 2026";
const EFFECTIVE_DATE_ZH = "2026年4月15日";

export function PrivacyContent() {
  const lang = useLocale();
  return lang === "zh" ? <PrivacyZh /> : <PrivacyEn />;
}

function PrivacyEn() {
  return (
    <>
      <LegalHero
        eyebrow="Legal · Privacy"
        title="Privacy Policy"
        effectiveDate={`Effective ${EFFECTIVE_DATE_EN}`}
        description="This Policy describes what data Apprentice collects, how we use it, who we share it with, and the controls you have over your information."
      />

      <p>
        This Privacy Policy explains how <strong>Apprentice, Inc.</strong>, a
        Delaware corporation (&ldquo;we&rdquo;, &ldquo;us&rdquo;), collects,
        uses, and shares personal data when you use Apprentice (the
        &ldquo;Service&rdquo;). If you do not agree with this Policy, do not
        use the Service.
      </p>

      <h2>1. Information we collect</h2>
      <h3>Information you provide</h3>
      <ul>
        <li>
          <strong>Account data:</strong> name, email address, password hash,
          and (if you use Google sign-in) profile information returned by
          Google OAuth.
        </li>
        <li>
          <strong>User Content:</strong> books, documents, or other files
          you upload; chat messages you send to the AI tutor; notes,
          progress, and annotations you create.
        </li>
        <li>
          <strong>Billing data:</strong> we use Stripe to process payments.
          We receive the last four digits of your card, brand, billing
          country, and transaction metadata, but{" "}
          <em>we never see your full card number</em>.
        </li>
        <li>
          <strong>Support communications:</strong> messages you send us via
          email or in-product support.
        </li>
      </ul>

      <h3>Information collected automatically</h3>
      <ul>
        <li>
          <strong>Usage data:</strong> pages viewed, features used, books
          opened, credits consumed, error logs, and performance telemetry.
        </li>
        <li>
          <strong>Device data:</strong> IP address, browser type, operating
          system, approximate location derived from IP, and session cookies.
        </li>
      </ul>

      <h2>2. How we use your data</h2>
      <p>We use personal data to:</p>
      <ul>
        <li>Provide, operate, and improve the Service;</li>
        <li>Parse and index the content you upload so the AI tutor can teach it to you;</li>
        <li>Authenticate your account and prevent fraud or abuse;</li>
        <li>Process payments and manage subscriptions and credits;</li>
        <li>Send transactional emails (receipts, security notices, product updates you have opted into);</li>
        <li>Debug, measure performance, and monitor for security incidents;</li>
        <li>Comply with legal obligations and enforce our Terms.</li>
      </ul>

      <h2>3. AI processing</h2>
      <p>
        To power tutoring, summarization, and quizzing, we send portions of
        your User Content and chat messages to third-party AI providers
        (currently <strong>Anthropic</strong>). These providers process the
        data on our behalf under contract and, based on their current
        terms, do <em>not</em> use that data to train their foundation
        models.
      </p>
      <p>
        <strong>We do not sell your data.</strong> We also do not use your
        User Content or chat history to train our own large language
        models. We may use de-identified or aggregated metrics (for example,
        &ldquo;average chapters per book&rdquo;) to improve the product.
      </p>

      <h2>4. Cookies and similar technologies</h2>
      <p>
        We use cookies and similar technologies for authentication, session
        management, and basic analytics. We do not use advertising cookies.
        You can disable cookies in your browser, but the Service will not
        function correctly without them.
      </p>

      <h2>5. How we share data</h2>
      <p>
        We share personal data only with the following categories of
        recipients, and only as needed:
      </p>
      <ul>
        <li>
          <strong>Processors / sub-processors</strong> acting on our behalf,
          currently including: Anthropic (AI inference), Stripe (payments),
          Google (OAuth sign-in), and our hosting, database, email, and
          monitoring providers.
        </li>
        <li>
          <strong>Legal and safety:</strong> when we believe disclosure is
          reasonably necessary to comply with a law, subpoena, or lawful
          request; to enforce our Terms; or to protect the rights, safety,
          or property of any person.
        </li>
        <li>
          <strong>Business transfers:</strong> if we are involved in a
          merger, acquisition, financing, or sale of assets, your data may
          be transferred as part of that transaction, subject to this
          Policy.
        </li>
      </ul>

      <h2>6. International transfers</h2>
      <p>
        We are based in the United States and process data there. If you
        access the Service from outside the United States, your data will
        be transferred to, stored, and processed in the United States.
        Where required by law (for example for transfers out of the EEA, UK,
        or Switzerland), we rely on appropriate safeguards such as the
        European Commission&rsquo;s Standard Contractual Clauses.
      </p>

      <h2>7. Data retention</h2>
      <p>
        We retain account data for as long as your account is active. User
        Content is retained until you delete it or close your account.
        After account closure, we delete or anonymize personal data within
        a reasonable period (typically 30 days), except where a longer
        retention is required for legal, tax, backup, or fraud-prevention
        purposes.
      </p>

      <h2>8. Your rights</h2>
      <p>Depending on where you live, you may have the right to:</p>
      <ul>
        <li>Access the personal data we hold about you;</li>
        <li>Correct inaccurate data;</li>
        <li>Delete your data (subject to certain legal exceptions);</li>
        <li>Export your data in a portable format;</li>
        <li>Object to or restrict certain processing;</li>
        <li>Withdraw consent where processing is based on consent;</li>
        <li>Lodge a complaint with your local data-protection authority.</li>
      </ul>
      <p>
        California residents have additional rights under the California
        Consumer Privacy Act (CCPA/CPRA), including the right to know what
        personal information we collect and the right to opt out of the
        &ldquo;sale&rdquo; or &ldquo;sharing&rdquo; of personal information.
        We do not sell or share personal information as those terms are
        defined under the CCPA/CPRA.
      </p>
      <p>
        You can exercise most of these rights from your account settings or
        by emailing{" "}
        <a href="mailto:privacy@apprentice.app">privacy@apprentice.app</a>.
        We may need to verify your identity before acting on the request.
      </p>

      <h2>9. Security</h2>
      <p>
        We use industry-standard security measures, including encryption in
        transit (TLS) and at rest for stored files, access controls, and
        audit logging. No system is perfectly secure; you use the Service
        at your own risk and are responsible for keeping your credentials
        safe.
      </p>

      <h2>10. Children</h2>
      <p>
        The Service is not directed to children under 13 (or the minimum
        digital-consent age in your jurisdiction). We do not knowingly
        collect personal data from children below that age. If you believe
        a child has provided us with personal data, please contact us so we
        can delete it.
      </p>

      <h2>11. Changes to this Policy</h2>
      <p>
        We may update this Policy from time to time. If the changes are
        material, we will notify you (for example by email or an in-product
        notice) before they take effect. The &ldquo;Effective date&rdquo;
        at the top always shows the latest revision.
      </p>

      <h2>12. Contact</h2>
      <p>
        Questions or requests about this Policy can be directed to{" "}
        <a href="mailto:privacy@apprentice.app">privacy@apprentice.app</a>.
      </p>
    </>
  );
}

function PrivacyZh() {
  return (
    <>
      <LegalHero
        eyebrow="法律 · 隐私"
        title="隐私政策"
        effectiveDate={`生效日期 ${EFFECTIVE_DATE_ZH}`}
        description="本政策说明 Apprentice 收集哪些数据、如何使用、与谁共享，以及您对自己信息所享有的控制权。"
      />

      <p>
        本《隐私政策》说明在美国特拉华州注册成立的 <strong>Apprentice, Inc.</strong>
        （以下简称&ldquo;我们&rdquo;）在您使用 Apprentice（以下简称&ldquo;本服务&rdquo;）时，
        如何收集、使用和共享您的个人数据。若您不同意本政策，请勿使用本服务。
      </p>

      <h2>1. 我们收集的信息</h2>
      <h3>您主动提供的信息</h3>
      <ul>
        <li>
          <strong>账号数据：</strong>姓名、电子邮箱、密码哈希；若您使用 Google 登录，
          还包括 Google OAuth 返回的个人资料信息。
        </li>
        <li>
          <strong>用户内容：</strong>您上传的书籍、文档或其他文件；您发送给 AI
          导师的聊天消息；您创建的笔记、进度与标注。
        </li>
        <li>
          <strong>账单数据：</strong>我们通过 Stripe 处理支付。我们仅接收您卡号的后四位、
          卡品牌、账单国家/地区以及交易元数据，<em>我们不会看到您完整的卡号</em>。
        </li>
        <li>
          <strong>支持通讯：</strong>您通过电子邮件或产品内支持发送给我们的消息。
        </li>
      </ul>

      <h3>自动收集的信息</h3>
      <ul>
        <li>
          <strong>使用数据：</strong>浏览页面、使用功能、打开书籍、消耗的积分、错误日志与性能遥测。
        </li>
        <li>
          <strong>设备数据：</strong>IP 地址、浏览器类型、操作系统、由 IP 推断的大致位置，以及会话 Cookie。
        </li>
      </ul>

      <h2>2. 我们如何使用您的数据</h2>
      <p>我们使用个人数据的目的包括：</p>
      <ul>
        <li>提供、运营与改进本服务；</li>
        <li>解析与索引您上传的内容，以便 AI 导师向您讲授；</li>
        <li>对您的账号进行身份验证，防范欺诈与滥用；</li>
        <li>处理支付并管理订阅与积分；</li>
        <li>发送事务性邮件（收据、安全通知，以及您选择接收的产品更新）；</li>
        <li>排查故障、衡量性能并监控安全事件；</li>
        <li>履行法律义务并执行我们的条款。</li>
      </ul>

      <h2>3. AI 处理</h2>
      <p>
        为支持教学、摘要与测验功能，我们会将您的部分&ldquo;用户内容&rdquo;和聊天消息发送给第三方 AI 提供商
        （目前为 <strong>Anthropic</strong>）。该等提供商根据合同代表我们处理数据，且按其现行条款，
        <em>不会</em>使用该等数据训练其基础模型。
      </p>
      <p>
        <strong>我们不会出售您的数据。</strong>我们也不会使用您的&ldquo;用户内容&rdquo;或聊天记录来训练我们自己的大型语言模型。
        我们可能使用经去标识化或聚合的统计指标（例如&ldquo;每本书的平均章节数&rdquo;）以改进产品。
      </p>

      <h2>4. Cookie 与类似技术</h2>
      <p>
        我们使用 Cookie 及类似技术用于身份验证、会话管理和基本分析。我们不使用广告类 Cookie。
        您可在浏览器中禁用 Cookie，但如此一来本服务将无法正常工作。
      </p>

      <h2>5. 我们如何共享数据</h2>
      <p>我们仅在必要时，向下列类别的接收方共享个人数据：</p>
      <ul>
        <li>
          <strong>处理者 / 次级处理者：</strong>代表我们行事，目前包括 Anthropic（AI 推理）、
          Stripe（支付）、Google（OAuth 登录），以及我们的托管、数据库、邮件与监控服务提供商。
        </li>
        <li>
          <strong>法律与安全：</strong>当我们合理认为必要时，为遵守法律、传票或合法请求；
          为执行我们的条款；或为保护任何人的权利、安全或财产。
        </li>
        <li>
          <strong>业务转让：</strong>如我们发生合并、收购、融资或资产出售，您的数据可能作为交易的一部分被转移，
          但仍受本政策约束。
        </li>
      </ul>

      <h2>6. 国际数据传输</h2>
      <p>
        我们位于美国并在美国处理数据。若您从美国境外访问本服务，您的数据将被传输至美国并在美国存储和处理。
        在法律要求时（例如从欧洲经济区、英国或瑞士向外传输），我们依赖适当的保障措施，
        如欧盟委员会发布的《标准合同条款》（SCC）。
      </p>

      <h2>7. 数据保留</h2>
      <p>
        账号处于活跃期间，我们将保留账号数据。&ldquo;用户内容&rdquo;将保留至您自行删除或注销账号为止。
        账号注销后，我们通常会在合理期限内（一般为 30 天）删除或匿名化个人数据；
        但法律、税务、备份或反欺诈目的要求更长保留期的除外。
      </p>

      <h2>8. 您的权利</h2>
      <p>根据您所在地区的不同，您可能享有以下权利：</p>
      <ul>
        <li>访问我们持有的您的个人数据；</li>
        <li>更正不准确的数据；</li>
        <li>删除您的数据（可能受某些法律例外限制）；</li>
        <li>以可移植格式导出您的数据；</li>
        <li>反对或限制某些处理活动；</li>
        <li>在我们基于同意进行处理时撤回同意；</li>
        <li>向您当地的数据保护机构提出申诉。</li>
      </ul>
      <p>
        加州居民根据《加州消费者隐私法案》（CCPA/CPRA）享有额外权利，包括知悉我们所收集的个人信息的权利，
        以及选择退出个人信息&ldquo;出售&rdquo;或&ldquo;共享&rdquo;的权利。按 CCPA/CPRA 的定义，
        我们不&ldquo;出售&rdquo;也不&ldquo;共享&rdquo;您的个人信息。
      </p>
      <p>
        您可在账号设置中或通过邮件
        <a href="mailto:privacy@apprentice.app"> privacy@apprentice.app</a>{" "}
        行使上述多数权利。我们可能需要在处理请求前核实您的身份。
      </p>

      <h2>9. 安全</h2>
      <p>
        我们采用行业标准的安全措施，包括传输中加密（TLS）与存储文件的静态加密、访问控制及审计日志。
        任何系统都并非绝对安全；您使用本服务的风险自负，并有责任妥善保管您的登录凭证。
      </p>

      <h2>10. 儿童</h2>
      <p>
        本服务并非面向 13 周岁以下（或您所在辖区规定的数字服务最低同意年龄以下）的儿童。
        我们不会明知而收集此年龄以下儿童的个人数据。若您认为某名儿童向我们提供了个人数据，
        请与我们联系以便删除。
      </p>

      <h2>11. 本政策的变更</h2>
      <p>
        我们可不时更新本政策。若变更属重大变更，我们将在生效前通知您（例如通过邮件或产品内通知）。
        页面顶部的&ldquo;生效日期&rdquo;始终反映最新修订版本。
      </p>

      <h2>12. 联系方式</h2>
      <p>
        如对本政策有任何疑问或请求，请发送邮件至
        <a href="mailto:privacy@apprentice.app"> privacy@apprentice.app</a>。
      </p>
    </>
  );
}
