declare module "katex/contrib/auto-render" {
  interface RenderMathInElementOptions {
    delimiters?: Array<{ left: string; right: string; display: boolean }>;
    ignoredTags?: string[];
    ignoredClasses?: string[];
    errorCallback?: (msg: string, err: Error) => void;
    throwOnError?: boolean;
  }
  const renderMathInElement: (
    el: HTMLElement,
    options?: RenderMathInElementOptions,
  ) => void;
  export default renderMathInElement;
}
