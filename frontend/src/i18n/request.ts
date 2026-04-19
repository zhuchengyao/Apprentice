import { cookies, headers } from "next/headers";
import { getRequestConfig } from "next-intl/server";
import {
  defaultLocale,
  isLocale,
  LOCALE_COOKIE,
  type Locale,
} from "./config";

function negotiate(acceptLanguage: string | null): Locale {
  if (!acceptLanguage) return defaultLocale;
  const tags = acceptLanguage
    .toLowerCase()
    .split(",")
    .map((part) => part.split(";")[0].trim());
  for (const tag of tags) {
    if (tag.startsWith("zh")) return "zh";
    if (tag.startsWith("en")) return "en";
  }
  return defaultLocale;
}

export default getRequestConfig(async () => {
  const cookieStore = await cookies();
  const stored = cookieStore.get(LOCALE_COOKIE)?.value;

  let locale: Locale = defaultLocale;
  if (isLocale(stored)) {
    locale = stored;
  } else {
    const headerStore = await headers();
    locale = negotiate(headerStore.get("accept-language"));
  }

  const messages = (await import(`../../messages/${locale}.json`)).default;
  return { locale, messages };
});
