"use client";

import { useLocale } from "next-intl";
import { LegalHero } from "@/components/legal/legal-hero";

const EFFECTIVE_DATE_EN = "April 15, 2026";
const EFFECTIVE_DATE_ZH = "2026年4月15日";

export function RefundContent() {
  const lang = useLocale();
  return lang === "zh" ? <RefundZh /> : <RefundEn />;
}

function RefundEn() {
  return (
    <>
      <LegalHero
        eyebrow="Legal · Refunds"
        title="Refund Policy"
        effectiveDate={`Effective ${EFFECTIVE_DATE_EN}`}
        description="When refunds are available for subscriptions and credit packs, when they are not, and how to request one."
      />

      <p>
        We want you to be happy with Apprentice. This Refund Policy
        explains when refunds are available for subscriptions and credit
        packs purchased from <strong>Apprentice, Inc.</strong>, and how to
        request one. This Policy forms part of our{" "}
        <a href="/terms">Terms of Service</a>. Where mandatory local law
        gives you stronger rights (for example, the 14-day right of
        withdrawal in the EU/UK), those rights apply in addition to this
        Policy.
      </p>

      <h2>1. Subscriptions</h2>
      <p>
        Subscription fees are billed in advance for each billing period
        (monthly or annual).
      </p>
      <ul>
        <li>
          <strong>7-day money-back guarantee (first purchase):</strong> If
          you subscribe for the first time and find the Service is not
          right for you, email us within <strong>7 days</strong> of the
          initial charge and we will issue a full refund. This applies
          only to your first-ever paid subscription.
        </li>
        <li>
          <strong>Renewals:</strong> Automatic renewal charges are
          generally non-refundable once billed. You can cancel at any time
          from your account settings; cancellation takes effect at the end
          of the current billing period, and you keep access until then.
        </li>
        <li>
          <strong>Annual plans, pro-rated:</strong> If you cancel an
          annual plan within <strong>14 days</strong> of renewal and have
          not used more than 20% of the bundled credits for that period,
          you may request a pro-rated refund for the unused remainder.
        </li>
      </ul>

      <h2>2. Credit packs</h2>
      <p>
        Credits are a prepaid unit of AI usage. Credit packs are generally{" "}
        <strong>non-refundable</strong> once used.
      </p>
      <ul>
        <li>
          <strong>Unused credits:</strong> If you have not consumed any
          credits from a pack, you may request a refund within{" "}
          <strong>14 days</strong> of purchase.
        </li>
        <li>
          <strong>Partially used credits:</strong> We may, at our
          discretion, refund the monetary value of the unused portion,
          minus any promotional bonus credits that were granted with the
          pack.
        </li>
        <li>
          Credits have no cash value, are not transferable, and expire 12
          months after purchase unless otherwise stated at checkout.
        </li>
      </ul>

      <h2>3. Service failures</h2>
      <p>
        If the Service is materially unavailable or malfunctioning in a
        way that prevents you from using the credits or subscription you
        paid for, contact us and we will, at our option, extend your
        access, restore the consumed credits, or issue a pro-rated refund
        covering the affected period.
      </p>

      <h2>4. When refunds are not available</h2>
      <p>We generally cannot issue refunds in the following cases:</p>
      <ul>
        <li>
          The account was terminated for breach of the{" "}
          <a href="/terms">Terms of Service</a> (for example, copyright
          infringement, abuse, or fraud);
        </li>
        <li>
          The charge is disputed more than 90 days after the transaction
          date;
        </li>
        <li>The credits have already been consumed to generate AI output;</li>
        <li>
          The request is based on dissatisfaction with AI output quality
          that is consistent with the disclaimers in our Terms (AI output
          can be inaccurate).
        </li>
      </ul>

      <h2>5. How to request a refund</h2>
      <p>
        Email us at{" "}
        <a href="mailto:billing@apprentice.app">billing@apprentice.app</a>{" "}
        with:
      </p>
      <ul>
        <li>The email address on your account;</li>
        <li>
          The transaction ID or invoice number (available in your account
          under Billing);
        </li>
        <li>A short description of why you are requesting a refund.</li>
      </ul>
      <p>
        We will acknowledge your request within 2 business days and aim to
        make a decision within 10 business days. Approved refunds are
        issued to the original payment method through Stripe; depending on
        your bank, it can take 5&ndash;10 additional business days for the
        funds to appear.
      </p>

      <h2>6. Chargebacks</h2>
      <p>
        Please contact us before disputing a charge with your bank or card
        issuer &mdash; we can almost always resolve billing questions
        faster than a chargeback. Accounts associated with fraudulent or
        abusive chargebacks may be suspended.
      </p>

      <h2>7. Changes</h2>
      <p>
        We may update this Refund Policy from time to time. The version in
        effect at the time of your purchase applies to that purchase.
      </p>

      <h2>8. Contact</h2>
      <p>
        Questions? Write to{" "}
        <a href="mailto:billing@apprentice.app">billing@apprentice.app</a>.
      </p>
    </>
  );
}

function RefundZh() {
  return (
    <>
      <LegalHero
        eyebrow="法律 · 退款"
        title="退款政策"
        effectiveDate={`生效日期 ${EFFECTIVE_DATE_ZH}`}
        description="订阅与积分包在何种情况下可以申请退款、哪些情形不予退款，以及具体的申请方式。"
      />

      <p>
        我们希望您满意 Apprentice 的体验。本《退款政策》说明您向
        <strong> Apprentice, Inc.</strong> 购买订阅与积分包时，何种情况下可以申请退款以及申请方式。
        本政策构成我们<a href="/terms">《服务条款》</a>的一部分。
        如果强制性的当地法律赋予您更强的权利（例如欧盟/英国的 14 天撤回权），该等权利在本政策之外同样适用。
      </p>

      <h2>1. 订阅</h2>
      <p>订阅费按结算周期（月度或年度）提前计费。</p>
      <ul>
        <li>
          <strong>首次购买 7 天内无理由退款：</strong>若您系首次订阅并认为本服务不适合您，
          请在初次扣费起<strong>7 天内</strong>发送邮件给我们，我们将全额退款。本条仅适用于您的首次付费订阅。
        </li>
        <li>
          <strong>自动续费：</strong>自动续费款项一经计费通常不予退款。您可随时在账户设置中取消订阅；
          取消将在当前结算周期结束时生效，期间您仍可继续使用本服务。
        </li>
        <li>
          <strong>年度计划按比例退款：</strong>若您在年度续费后的
          <strong>14 天内</strong>取消，且尚未使用超过该期间所含积分的 20%，
          您可就未使用部分申请按比例退款。
        </li>
      </ul>

      <h2>2. 积分包</h2>
      <p>
        积分是 AI 用量的预付单位。积分包一经使用通常<strong>不予退款</strong>。
      </p>
      <ul>
        <li>
          <strong>未使用的积分：</strong>如您尚未消耗某积分包中的任何积分，可在购买后
          <strong>14 天内</strong>申请退款。
        </li>
        <li>
          <strong>部分使用的积分：</strong>我们可酌情就未使用部分的等值金额予以退款，
          但将扣除随该积分包一并赠送的任何促销积分。
        </li>
        <li>
          积分不具备现金价值、不可转让；除非购买时另有说明，积分自购买之日起 12 个月后过期。
        </li>
      </ul>

      <h2>3. 服务故障</h2>
      <p>
        若本服务因重大不可用或故障导致您无法使用已付费的积分或订阅，请联系我们，我们将选择以下方式之一处理：
        延长您的访问期、恢复已消耗的积分，或就受影响期间按比例退款。
      </p>

      <h2>4. 不予退款的情形</h2>
      <p>在下列情形下，我们通常不予退款：</p>
      <ul>
        <li>
          账号因违反<a href="/terms">《服务条款》</a>而被终止（例如版权侵权、滥用或欺诈）；
        </li>
        <li>交易日起超过 90 天后才提出付款争议；</li>
        <li>积分已被消耗用于生成 AI 输出；</li>
        <li>
          请求仅基于对 AI 输出质量的不满，而该等表现与本条款的免责声明一致（AI 输出可能不准确）。
        </li>
      </ul>

      <h2>5. 如何申请退款</h2>
      <p>
        请发送邮件至
        <a href="mailto:billing@apprentice.app"> billing@apprentice.app</a>，并提供：
      </p>
      <ul>
        <li>您的账号邮箱；</li>
        <li>交易 ID 或发票编号（可在账号的 Billing 页面查看）；</li>
        <li>简要说明申请退款的原因。</li>
      </ul>
      <p>
        我们将在 2 个工作日内确认收到您的请求，并力争在 10 个工作日内作出决定。
        获准的退款将通过 Stripe 原路退回原支付方式；视您银行情况，款项到账可能还需额外 5–10 个工作日。
      </p>

      <h2>6. 付款争议（Chargeback）</h2>
      <p>
        在您向银行或发卡机构发起争议前，请先联系我们——账单问题通常可以比 chargeback 流程更快得到解决。
        与欺诈性或滥用性 chargeback 相关的账号可能被暂停。
      </p>

      <h2>7. 变更</h2>
      <p>
        我们可不时更新本退款政策。适用于每次购买的，以购买当时生效的版本为准。
      </p>

      <h2>8. 联系方式</h2>
      <p>
        如有疑问，请发送邮件至
        <a href="mailto:billing@apprentice.app"> billing@apprentice.app</a>。
      </p>
    </>
  );
}
