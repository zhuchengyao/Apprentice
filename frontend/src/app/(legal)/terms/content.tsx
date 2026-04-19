"use client";

import { LegalHero } from "@/components/legal/legal-hero";
import { useLocale } from "next-intl";

const EFFECTIVE_DATE_EN = "April 15, 2026";
const EFFECTIVE_DATE_ZH = "2026年4月15日";

export function TermsContent() {
  const lang = useLocale();
  return lang === "zh" ? <TermsZh /> : <TermsEn />;
}

function TermsEn() {
  return (
    <>
      <LegalHero
        eyebrow="Legal · Terms"
        title="Terms of Service"
        effectiveDate={`Effective ${EFFECTIVE_DATE_EN}`}
        description="These Terms govern how you access and use Apprentice. Please read them carefully — they cover your account, your uploaded content, AI output, subscriptions, and our respective responsibilities."
      />

      <p>
        These Terms of Service (&ldquo;Terms&rdquo;) govern your access to and
        use of Apprentice (the &ldquo;Service&rdquo;), operated by{" "}
        <strong>Apprentice, Inc.</strong>, a Delaware corporation
        (&ldquo;we&rdquo;, &ldquo;us&rdquo;, or &ldquo;our&rdquo;). By
        creating an account or otherwise using the Service, you agree to be
        bound by these Terms. If you do not agree, do not use the Service.
      </p>

      <h2>1. Eligibility and accounts</h2>
      <p>
        You must be at least 13 years old (or the minimum digital-consent age
        in your jurisdiction, whichever is higher) to use the Service. If you
        are under 18, you represent that a parent or legal guardian has
        reviewed and accepted these Terms on your behalf.
      </p>
      <p>
        You are responsible for maintaining the confidentiality of your
        account credentials and for all activity under your account. You
        agree to provide accurate information and to keep it current. You may
        not share your account or resell access to it.
      </p>

      <h2>2. The Service</h2>
      <p>
        Apprentice is an AI-powered study companion. You may upload books or
        documents (&ldquo;User Content&rdquo;), and the Service will parse,
        index, summarize, quiz, and discuss their content with you through
        conversational AI. Features, pricing, and availability may change
        over time.
      </p>

      <h2>3. Your content and responsibilities</h2>
      <p>
        You retain all rights in the User Content you upload. By uploading,
        you grant us a worldwide, non-exclusive, royalty-free license to
        host, copy, process, transmit, analyze, create derivative works of,
        and display that content <em>solely</em> to operate and improve the
        Service for you. This license ends when you delete the content or
        your account, except where retention is required by law or for
        legitimate backup/audit purposes.
      </p>
      <p>You represent and warrant that, for every file you upload:</p>
      <ul>
        <li>
          You own it, or you have all rights and permissions necessary
          (including from copyright holders) to upload and process it through
          an automated tool that stores and transforms it.
        </li>
        <li>
          It does not infringe any third party&rsquo;s intellectual property,
          privacy, publicity, or other rights.
        </li>
        <li>
          It does not contain malware, illegal content, content sexually
          exploiting minors, or content that violates applicable law.
        </li>
      </ul>
      <p>
        <strong>
          Do not upload copyrighted books you do not own or are not otherwise
          licensed to process.
        </strong>{" "}
        We may remove content and terminate accounts that we reasonably
        believe violate this section, and we may respond to valid takedown
        notices (including DMCA notices) in accordance with applicable law.
      </p>

      <h2>4. Acceptable use</h2>
      <p>You agree not to:</p>
      <ul>
        <li>Reverse engineer, scrape, or probe the Service for vulnerabilities, except as expressly permitted by law;</li>
        <li>Use the Service to build a competing product, to train machine-learning models, or to extract our prompts, embeddings, or model outputs in bulk;</li>
        <li>Interfere with other users, impersonate anyone, or misrepresent your affiliation;</li>
        <li>Use the Service to generate unlawful, harassing, defamatory, or misleading content; or</li>
        <li>Circumvent usage limits, rate limits, credit accounting, or access controls.</li>
      </ul>

      <h2>5. AI output disclaimer</h2>
      <p>
        The Service uses large language models to generate explanations,
        summaries, quizzes, and conversational responses. AI output may be
        inaccurate, incomplete, outdated, or inappropriate for your
        circumstances. <strong>Do not rely on the Service as a substitute
        for professional advice</strong> (medical, legal, financial, safety,
        or otherwise), and verify anything important against authoritative
        sources. You are responsible for how you use AI output.
      </p>

      <h2>6. Subscriptions, credits, and payment</h2>
      <p>
        Paid plans and credit packs are billed through our payment processor
        (currently Stripe). By subscribing, you authorize us to charge your
        payment method on a recurring basis until you cancel. Prices are
        shown at the point of purchase and may change with notice for future
        billing periods.
      </p>
      <p>
        Credits are a prepaid, internal unit used to meter AI usage. Credits
        have no cash value, are not transferable, and expire 12 months after
        purchase unless otherwise stated at checkout. Refunds are governed
        by our <a href="/refund">Refund Policy</a>, which is incorporated
        into these Terms by reference.
      </p>

      <h2>7. Intellectual property</h2>
      <p>
        The Service, including its software, design, prompts, model
        orchestration, and original content, is owned by us or our licensors
        and is protected by intellectual-property laws. We grant you a
        limited, non-exclusive, non-transferable, revocable license to use
        the Service in accordance with these Terms. No other rights are
        granted.
      </p>

      <h2>8. Third-party services</h2>
      <p>
        The Service integrates third-party providers (for example Anthropic
        for AI inference, Stripe for payments, Google for OAuth sign-in).
        Your use of those features is also subject to those providers&rsquo;
        terms. We are not responsible for third-party services.
      </p>

      <h2>9. Termination</h2>
      <p>
        You may stop using the Service and delete your account at any time.
        We may suspend or terminate your access if you breach these Terms,
        create risk or legal exposure for us, or if your account is inactive
        for an extended period. On termination, your license to use the
        Service ends and we may delete your User Content after a reasonable
        grace period.
      </p>

      <h2>10. Disclaimers</h2>
      <p>
        <strong>
          THE SERVICE IS PROVIDED &ldquo;AS IS&rdquo; AND &ldquo;AS
          AVAILABLE,&rdquo; WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS,
          IMPLIED, OR STATUTORY,
        </strong>{" "}
        INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
        PURPOSE, NON-INFRINGEMENT, ACCURACY, OR UNINTERRUPTED AVAILABILITY,
        TO THE MAXIMUM EXTENT PERMITTED BY LAW.
      </p>

      <h2>11. Limitation of liability</h2>
      <p>
        TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT WILL WE BE LIABLE
        FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR
        PUNITIVE DAMAGES, OR FOR ANY LOSS OF PROFITS, REVENUE, DATA, OR
        GOODWILL, ARISING OUT OF OR IN CONNECTION WITH THE SERVICE. OUR
        AGGREGATE LIABILITY FOR ANY CLAIM ARISING OUT OF OR RELATING TO THE
        SERVICE WILL NOT EXCEED THE GREATER OF (A) THE AMOUNT YOU PAID US IN
        THE 12 MONTHS BEFORE THE EVENT GIVING RISE TO THE CLAIM, OR (B) USD
        100.
      </p>

      <h2>12. Indemnification</h2>
      <p>
        You agree to indemnify and hold harmless Apprentice, Inc. and its
        officers, employees, and agents from any claims, damages, or expenses
        (including reasonable attorneys&rsquo; fees) arising from your User
        Content, your use of the Service, or your breach of these Terms.
      </p>

      <h2>13. Changes</h2>
      <p>
        We may update these Terms from time to time. If the changes are
        material, we will give you reasonable notice (for example by email or
        an in-product notice) before they take effect. Continued use of the
        Service after the effective date of the updated Terms constitutes
        acceptance.
      </p>

      <h2>14. Governing law and disputes</h2>
      <p>
        These Terms are governed by the laws of the State of Delaware, USA,
        without regard to conflict-of-laws principles. Any dispute arising
        out of or relating to these Terms or the Service will be resolved
        exclusively in the state or federal courts located in Delaware, and
        you and we consent to personal jurisdiction and venue there, except
        where mandatory local law requires otherwise.
      </p>

      <h2>15. Contact</h2>
      <p>
        Questions about these Terms? Email us at{" "}
        <a href="mailto:support@apprentice.app">support@apprentice.app</a>.
      </p>
    </>
  );
}

function TermsZh() {
  return (
    <>
      <LegalHero
        eyebrow="法律 · 服务条款"
        title="服务条款"
        effectiveDate={`生效日期 ${EFFECTIVE_DATE_ZH}`}
        description="本条款规范您访问和使用 Apprentice 的方式，涉及您的账号、上传内容、AI 输出、订阅以及双方的责任，请仔细阅读。"
      />

      <p>
        本《服务条款》（以下简称&ldquo;本条款&rdquo;）规范您对 Apprentice
        （以下简称&ldquo;本服务&rdquo;）的访问与使用。本服务由在美国特拉华州注册成立的
        <strong> Apprentice, Inc.</strong>（以下简称&ldquo;我们&rdquo;）运营。
        您一旦注册账号或以任何方式使用本服务，即表示同意受本条款约束。
        若您不同意本条款，请勿使用本服务。
      </p>

      <h2>1. 资格与账号</h2>
      <p>
        您须年满 13 周岁（或您所在司法辖区规定的数字服务最低同意年龄，以较高者为准）方可使用本服务。
        若您未满 18 周岁，则视为您的父母或法定监护人已代您审阅并接受本条款。
      </p>
      <p>
        您应妥善保管账号凭证，并对账号项下的全部活动负责。您应提供真实、准确、最新的信息；
        不得与他人共享账号，亦不得转售本服务的访问权。
      </p>

      <h2>2. 本服务</h2>
      <p>
        Apprentice 是一款由人工智能驱动的学习助手。您可上传书籍或文档（以下简称&ldquo;用户内容&rdquo;），
        本服务将对其进行解析、索引、摘要、测验，并通过对话式 AI 与您讨论其中内容。
        本服务的功能、定价与可用性可能随时调整。
      </p>

      <h2>3. 您的内容与责任</h2>
      <p>
        您对所上传的&ldquo;用户内容&rdquo;保留全部权利。您上传即授予我们一项全球范围、非独家、免许可费的许可，
        允许我们托管、复制、处理、传输、分析、制作衍生作品并展示该等内容，<em>仅</em>用于为您运营和改进本服务。
        当您删除该内容或删除账号时，上述许可终止；但法律要求保留或出于合法备份/审计目的的除外。
      </p>
      <p>对于您上传的每一份文件，您陈述并保证：</p>
      <ul>
        <li>您拥有其全部权利，或已获得（包括版权人）授予的全部必要权利与许可，得以通过存储并转换该等内容的自动化工具上传和处理；</li>
        <li>该等内容不侵犯任何第三方的知识产权、隐私权、形象权或其他权利；</li>
        <li>该等内容不含恶意软件、非法内容、对未成年人进行性剥削的内容，或任何违反适用法律的内容。</li>
      </ul>
      <p>
        <strong>请勿上传您不拥有版权、亦未获得授权处理的受版权保护书籍。</strong>
        我们可在合理认为存在违反本节之行为时删除相关内容并终止账号，并将根据适用法律（包括 DMCA 通知程序）响应有效的下架通知。
      </p>

      <h2>4. 可接受使用规则</h2>
      <p>您同意不会：</p>
      <ul>
        <li>对本服务进行逆向工程、抓取或漏洞探测，但法律明确允许者除外；</li>
        <li>利用本服务构建竞争性产品、训练机器学习模型，或批量提取我们的提示词、嵌入向量或模型输出；</li>
        <li>干扰其他用户、假冒他人或虚假陈述您的关联关系；</li>
        <li>利用本服务生成违法、骚扰、诽谤或误导性内容；或</li>
        <li>规避使用限额、速率限制、积分（credits）计量或访问控制。</li>
      </ul>

      <h2>5. AI 输出免责</h2>
      <p>
        本服务使用大型语言模型生成讲解、摘要、测验与对话式回复。AI 输出可能不准确、不完整、过时，
        或不适合您的具体情形。<strong>请勿将本服务作为专业意见的替代</strong>（包括医疗、法律、财务、安全等），
        重要事项应自行通过权威来源核实。您应为自己对 AI 输出的使用承担全部责任。
      </p>

      <h2>6. 订阅、积分与付款</h2>
      <p>
        付费计划和积分包通过我们的支付处理商（目前为 Stripe）结算。您订阅即授权我们按周期自您的支付方式扣款，直至您取消为止。
        价格以购买时页面展示为准，且可在合理通知后就未来结算周期进行调整。
      </p>
      <p>
        &ldquo;积分&rdquo;（credits）是用于计量 AI 用量的内部预付单位。积分不具备现金价值、不可转让，
        且自购买之日起 12 个月后过期（除非购买时另有说明）。退款事宜适用我们的
        <a href="/refund">《退款政策》</a>，该政策以引用方式并入本条款。
      </p>

      <h2>7. 知识产权</h2>
      <p>
        本服务（包括其软件、设计、提示词、模型编排及原创内容）归我们或我们的许可方所有，受知识产权法保护。
        我们授予您一项有限、非独家、不可转让、可撤销的许可，以便您按照本条款使用本服务。除此之外不授予您任何其他权利。
      </p>

      <h2>8. 第三方服务</h2>
      <p>
        本服务集成了第三方提供商（例如由 Anthropic 提供 AI 推理、Stripe 提供支付、Google 提供 OAuth 登录）。
        您对这些功能的使用还须遵守相应第三方的条款。我们不对第三方服务承担责任。
      </p>

      <h2>9. 终止</h2>
      <p>
        您可随时停止使用本服务并删除账号。如您违反本条款、对我们造成风险或法律风险，或长期不活跃，
        我们可暂停或终止您的访问权限。终止后，您对本服务的使用许可即告终止；我们可在合理宽限期后删除您的&ldquo;用户内容&rdquo;。
      </p>

      <h2>10. 免责声明</h2>
      <p>
        在适用法律允许的最大范围内，<strong>本服务按&ldquo;现状&rdquo;和&ldquo;可获得&rdquo;状态提供，
        不附带任何明示、默示或法定的任何保证</strong>，包括但不限于适销性、特定用途适用性、不侵权、
        准确性或不间断可用性之保证。
      </p>

      <h2>11. 责任限制</h2>
      <p>
        在适用法律允许的最大范围内，我们在任何情况下均不对因本服务产生或与之相关的任何间接、偶然、特殊、
        后果性、警示性或惩罚性损害，或任何利润、收入、数据或商誉损失承担责任。对于因本服务引起或与之相关的任何索赔，
        我们的累计责任上限为下列较高者：(a) 引发索赔之事件发生前 12 个月内您向我们支付的费用；或 (b) 100 美元。
      </p>

      <h2>12. 赔偿</h2>
      <p>
        您同意就因您的&ldquo;用户内容&rdquo;、您对本服务的使用或您违反本条款所引起的任何索赔、
        损害或费用（包括合理的律师费），向 Apprentice, Inc. 及其管理人员、员工和代理人作出赔偿，并使之免受损害。
      </p>

      <h2>13. 变更</h2>
      <p>
        我们可不时更新本条款。若变更属重大变更，我们将在生效前通过合理方式（如邮件或产品内通知）
        告知您。更新条款生效后您继续使用本服务，即视为接受。
      </p>

      <h2>14. 适用法律与争议解决</h2>
      <p>
        本条款受美国特拉华州法律管辖并据其解释，不适用其冲突法规则。因本条款或本服务引起或与之相关的任何争议，
        应由特拉华州的州法院或联邦法院专属管辖；您与我们在此同意接受该等法院的属人管辖与地域管辖。
        但强制性地方法律另有规定者除外。
      </p>

      <h2>15. 联系方式</h2>
      <p>
        如您对本条款有任何疑问，欢迎发送邮件至
        <a href="mailto:support@apprentice.app"> support@apprentice.app</a>。
      </p>
    </>
  );
}
